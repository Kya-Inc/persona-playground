import json
import os
import pandas as pd
import uuid
from typing import Optional
from pandas import DataFrame
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from icecream import ic

load_dotenv()


def preprocess_dataframe(df, speaker_name_col: str = "speaker", line_col: str = "line"):
    # Ensure 'speaker_name_col' and 'line_col' exists in df to avoid KeyErrors
    if speaker_name_col not in df.columns or line_col not in df.columns:
        raise KeyError(
            f"Column names {speaker_name_col} or {line_col} not found in DataFrame")

    # Forward fill the 'speaker_name_col' column to associate lines with their speakers
    df[speaker_name_col] = df[speaker_name_col].ffill()

    # Drop rows where 'line_col' is NaN (non-speaking lines)
    df = df.dropna(subset=[line_col])

    # Create a grouping key that changes each time the 'speaker_name_col' changes
    df['group_key'] = (df[speaker_name_col] !=
                       df[speaker_name_col].shift(1)).cumsum()

    # Group by 'speaker_name_col' and 'group_key' and concatenate the 'line_col' values
    grouped_df = df.groupby(['group_key', speaker_name_col])[
        line_col].agg(' '.join).reset_index()

    # Remove the 'group_key' as it is no longer needed
    grouped_df.drop('group_key', axis=1, inplace=True)

    # All lines in the output DataFrame are speaking lines, so we can safely add a column with True values
    grouped_df['speaking_line'] = True

    return grouped_df


def embed_character_dialogue(
    df: DataFrame,
    persona_id: str,
    persona_name_in_data: str,
    voice_over_name_in_data: Optional[str] = None,
    line_col: str = "line",
    line_raw_col: Optional[str] = None,
    speaker_name_col: str = "speaker",
    is_spoken_line_col: str = "speaking_line",
    dry_run: bool = False,
):
    # filter out non-speaking lines

    df = preprocess_dataframe(df, speaker_name_col, line_col)
    print(df)

    lines: DataFrame = df[df[is_spoken_line_col]]

    # filter out non-character lines (this includes lines that they say outloud and internally)
    character_df: DataFrame = lines[lines[speaker_name_col].isin(
        [persona_name_in_data, voice_over_name_in_data])].dropna(subset=[line_col])

    qdrant = QdrantClient(url=os.environ.get("QDRANT_URL"),
                          api_key=os.environ.get("QDRANT_API_KEY"))

    # semantic_model = SentenceTransformer("thenlper/gte-large")
    # semantic_model = SentenceTransformer("all-MiniLM-L6-v2")
    semantic_model = SentenceTransformer("BAAI/bge-base-en-v1.5")

    cue_records = []
    response_records = []
    thought_records = []

    concat_rows = []

    for i, row in character_df.iterrows():
        if i in concat_rows:
            continue

        response: str = row[line_col]

        prev_row = df.iloc[i - 1]
        next_row = df.iloc[i + 1] if i < len(df) - 1 else None
        prev_char: str = prev_row[speaker_name_col]
        id = uuid.uuid4().hex

        # concatenate next lines if they are by the same character
        if i < len(df) - 1:
            if (
                next_row[is_spoken_line_col]
                and row[speaker_name_col] == next_row[speaker_name_col]
            ):
                if pd.isna(row[line_col]):
                    response = next_row[line_col]
                elif pd.isna(next_row[line_col]):
                    response = row[line_col]
                else:
                    response = row[line_col] + \
                        " " + next_row[line_col]

                concat_rows.append(i + 1)

        # if this is the first line of a scene change or episode then treat it like a standalone thought
        if not prev_row[is_spoken_line_col] or row[speaker_name_col] == voice_over_name_in_data:
            if not dry_run:
                thought_vec = semantic_model.encode(response)

            payload = {
                "thought": response,
                "persona_id": persona_id,
                "meta": {**row},
            }

            try:
                thought_record = models.Record(
                    id=id,
                    vector=thought_vec.tolist() if not dry_run else None,
                    payload=payload,
                )
            except Exception as e:
                print(e)
                print("thought: ", response)
                continue

            thought_records.append(thought_record)

        else:  # the line before this response was the likely cue since it was a speaking line
            # check if the line before the cue line was the same speaker as the cue line, if so concatenate them
            row_before_cue = df.iloc[i - 2]
            if (
                row_before_cue[is_spoken_line_col]
                and prev_row[speaker_name_col]
                == row_before_cue[speaker_name_col]
            ):
                if pd.isna(row_before_cue[line_col]):
                    cue = prev_row[line_col]
                elif pd.isna(prev_row[line_col]):
                    cue = row_before_cue[line_col]
                else:
                    cue = row_before_cue[line_col] + \
                        " " + prev_row[line_col]
            else:
                cue: str = prev_row[line_col]

            if pd.isna(cue) and line_raw_col:
                cue = prev_row[line_raw_col]

            payload = {
                "cue": cue,
                "responding_to": prev_char,
                "response": response,
                "persona_id": persona_id,
                "meta": {k: v for k, v in row.items() if not pd.isna(v) or not pd.isnull(v)}
            }

            # if not dry_run:
            if True:
                try:
                    cue_vec = semantic_model.encode(cue)
                    response_vec = semantic_model.encode(response)
                except Exception as e:
                    print(e)
                    print("cue: ", cue)
                    print("response: ", response)
                    continue

            cue_record = models.Record(
                id=id,
                # vector=cue_vec.tolist() if not dry_run else None,
                vector=cue_vec.tolist(),
                payload=payload,
            )

            response_record = models.Record(
                id=id,
                # vector=response_vec.tolist() if not dry_run else None,
                vector=response_vec.tolist(),
                payload=payload,
            )

            cue_records.append(cue_record)
            response_records.append(response_record)

    # just info to make sure things are adding up

    if not dry_run:
        print("cue/response pairs: ", len(cue_records))
        print("thoughts", len(thought_records))

        print("total records: ", len(cue_records) + len(thought_records))

        print("merged lines: ", len(concat_rows))
        print("total lines: ", len(cue_records) +
              len(thought_records) + len(concat_rows))

        qdrant.upload_records(collection_name="cues-768", records=cue_records)
        qdrant.upload_records(collection_name="responses-768",
                              records=response_records)
        qdrant.upload_records(collection_name="thoughts-768",
                              records=thought_records)
    else:

        print(json.dumps({
            "cues": [x.dict() for x in cue_records],
            "responses": [x.dict() for x in response_records],
            "thoughts": [x.dict() for x in thought_records],
            "count": {
                "cues": len(cue_records),
                "responses": len(response_records),
                "thoughts": len(thought_records),
                "merged": len(concat_rows),
                "total": len(cue_records) + len(thought_records) + len(concat_rows)
            }
        }))


# if __name__ == "__main__":
    """Example usage"""
    # # from persona_ids import NEDWARD_FLANDERS_PERSONA_ID
    # from persona_ids import C_MONTGOMERY_BURNS_PERSONA_ID
    # # from persona_ids import HOMER_SIMPSON_PERSONA_ID

    # # prepare dataframe for the specific character by loading from source, handling dtypes if needed, sorting, whatever else might be needed
    # dtypes = {
    #     "speaking_line": "boolean",
    # }

    # df: DataFrame = pd.read_csv(
    #     "data/shared/the_simpsons_lines.csv",
    #     low_memory=False,
    #     dtype=dtypes,
    #     index_col="id",
    # ).sort_index().reset_index()

    # # then we pass the data frame to the character/data agnostic function that creates the embeddings
    # embed_character_dialogue(
    #     df=df,
    #     persona_id=C_MONTGOMERY_BURNS_PERSONA_ID,
    #     persona_name_in_data="C. Montgomery Burns",
    #     line_col="spoken_words",
    #     speaker_name_col="raw_character_text",
    #     is_spoken_line_col="speaking_line",
    # )
