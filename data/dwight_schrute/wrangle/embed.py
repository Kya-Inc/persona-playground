# when you run this if you have errors set PYTHONPATH=../../../
import uuid
import streamlit as st  # yes I'm lazy and doing this for the global secrets
import pandas as pd
from pandas import DataFrame
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from persona_ids import DWIGHT_SCHRUTE_PERSONA_ID
data: DataFrame = pd.read_csv("../raw/the_office.csv")
df = pd.DataFrame(data)

dwight_df: DataFrame = df[df["speaker"] == "Dwight"]

qdrant = QdrantClient(url=st.secrets.qdrant_url,
                      api_key=st.secrets.qdrant_api_key)

semantic_model = SentenceTransformer("thenlper/gte-large")

documents: list = []
for i, row in dwight_df.iterrows():
    response: str = row["line"]

    prev_row = df.loc[i - 1]
    prev_char: str = prev_row["speaker"]
    prompt: str = prev_row["line"]

    context: DataFrame = df.loc[max(0, i - 2): i + 2][
        ["speaker", "line"]
    ]

    clean: DataFrame = context.dropna()
    chunk = clean.values.tolist()

    metadata = {
        "precontext": clean[0:2].to_json(orient="records"),
        "prompting_character": prev_char,
        "prompt": prompt,
        "response": response,
        "postcontext": clean[2:].to_json(orient="records"),
        "persona_id": DWIGHT_SCHRUTE_PERSONA_ID
    }

    documents.append(metadata)


prompt_records = []
response_records = []

for doc in documents:
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
