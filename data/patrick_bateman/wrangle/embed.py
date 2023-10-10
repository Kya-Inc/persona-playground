# when you run this if you have errors set PYTHONPATH=../../../
import uuid
import streamlit as st
import pandas as pd
from pandas import DataFrame
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

from persona_ids import PATRICK_BATEMAN_PERSONA_ID

data: DataFrame = pd.read_csv(
    "../raw/american_psycho.csv", sep="‚"
)  # this isn't a normal comma btw
df = pd.DataFrame(data)

bateman_df: DataFrame = df[df["character"].isin(["BATEMAN", "BATEMAN (V.O.)"])]

qdrant = QdrantClient(url=st.secrets.qdrant_url,
                      api_key=st.secrets.qdrant_api_key)

semantic_model = SentenceTransformer("thenlper/gte-large")

documents: list = []
for i, row in bateman_df.iterrows():
    response: str = row["line"]

    # Not likely the best way to deal with this, but for the monologue lines I am going to save them as prommpt and response for now. Just so they come up when searching for a prompt  and will allow searching for similar lines when searching for a response.k
    if row["character"] == "BATEMAN (V.O.)":
        prompt: str = row["line"]

        metadata = {
            "prompt": prompt,
            "response": response,
            "persona_id": PATRICK_BATEMAN_PERSONA_ID
        }

    else:
        prev_row = df.loc[i - 1]
        prev_char: str = prev_row["character"]
        prompt: str = prev_row["line"]

        context: DataFrame = df.loc[max(
            0, i - 2): i + 2][["character", "line"]]
        clean: DataFrame = context.dropna()
        chunk = clean.values.tolist()

        metadata = {
            "precontext": clean[0:2].to_json(orient="records"),
            "prompting_character": prev_char,
            "prompt": prompt,
            "response": response,
            "postcontext": clean[2:].to_json(orient="records"),
            "persona_id": PATRICK_BATEMAN_PERSONA_ID
        }

    documents.append(metadata)

print(documents)

prompt_records = []
response_records = []


for doc in documents:
    response_encoding = doc["response"]
    if isinstance(response_encoding, float):
        print("problem document: ", doc)

    if isinstance(response_encoding, str):
        id = uuid.uuid4().hex
        prompt_record = models.Record(
            id=id, vector=semantic_model.encode(doc["prompt"]).tolist(), payload=doc
        )

        response_record = models.Record(
            id=id, vector=semantic_model.encode(doc["response"]).tolist(), payload=doc
        )

    prompt_records.append(prompt_record)
    response_records.append(response_record)


qdrant.upload_records(collection_name="prompts", records=prompt_records)
qdrant.upload_records(collection_name="responses", records=response_records)
