import os
import streamlit as st  # yes I'm lazy and doing this for the global secrets
import pandas as pd
import uuid
from pandas import DataFrame
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()


def embed_character_dialogue(
    df: DataFrame,
    persona_id: str,
    persona_name_in_data: str,
    line_col: str = "line",
    speaker_name_col: str = "speaker",
    is_spoken_line_col: str = "speaking_line",
    dry_run: bool = False,
):
    # filter out non-speaking lines
    lines: DataFrame = df[df[is_spoken_line_col]]

    # filter out non-character lines
    character_df: DataFrame = lines[
        lines[speaker_name_col] == persona_name_in_data
    ].dropna(subset=[line_col])

    qdrant = QdrantClient(url=os.environ.get("QDRANT_URL"),
                          api_key=os.environ.get("QDRANT_API_KEY"))

    semantic_model = SentenceTransformer("thenlper/gte-large")

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
        if not prev_row[is_spoken_line_col]:
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
            row_before_cue = df.iloc[prev_row - 1]
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

            payload = {
                "cue": cue,
                "responding_to": prev_char,
                "response": response,
                "persona_id": persona_id,
                "meta": {**row},
            }

            if not dry_run:
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
                vector=cue_vec.tolist() if not dry_run else None,
                payload=payload,
            )

            response_record = models.Record(
                id=id,
                vector=response_vec.tolist() if not dry_run else None,
                payload=payload,
            )

            cue_records.append(cue_record)
            response_records.append(response_record)

    # just info to make sure things are adding up
    print("cue/response pairs: ", len(cue_records))
    print("thoughts", len(thought_records))

    print("total records: ", len(cue_records) + len(thought_records))

    print("merged lines: ", len(concat_rows))
    print("total lines: ", len(cue_records) +
          len(thought_records) + len(concat_rows))

    if not dry_run:
        qdrant.upload_records(collection_name="cues", records=cue_records)
        qdrant.upload_records(collection_name="responses",
                              records=response_records)
        qdrant.upload_records(collection_name="thoughts",
                              records=thought_records)
    # else:
        # print({
        #     "cues": cue_records,
        #     "responses": response_records,
        #     "thoughts": thought_records
        # })


# if __name__ == "__main__":
"""Example usage ... this part won't be in this file"""
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
