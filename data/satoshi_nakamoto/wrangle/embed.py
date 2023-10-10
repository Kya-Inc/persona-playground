# when you run this if you have errors set PYTHONPATH=../../../
from urllib import response
import uuid
import streamlit as st  # yes I'm lazy and doing this for the global secrets
import pandas as pd
from pandas import DataFrame
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from persona_ids import SATOSHI_NAKAMOTO_PERSONA_ID


qdrant = QdrantClient(url=st.secrets.qdrant_url,
                      api_key=st.secrets.qdrant_api_key)

semantic_model = SentenceTransformer("thenlper/gte-large")


# prompt and response pairs
data: DataFrame = pd.read_json("../raw/cue-response-pairs.json")
df = pd.DataFrame(data)

documents = []
for i, row in df.iterrows():
    prompt = row["q"]
    response = row["a"]
    metadata = {
        "prompt": prompt,
        "response": response,
        "data": row["date"],
        "src": row["src"],
        "persona_id": SATOSHI_NAKAMOTO_PERSONA_ID
    }

    documents.append(metadata)


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
