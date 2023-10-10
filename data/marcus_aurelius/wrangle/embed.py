# when you run this if you have errors set PYTHONPATH=../../../
import uuid
from bson import ObjectId
import streamlit as st  # yes I'm lazy and doing this for the global secrets
import pandas as pd
from pandas import DataFrame
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from persona_ids import MARCUS_AURELIUS_PERSONA_ID
from utils import cluster_text

semantic_model = SentenceTransformer("thenlper/gte-large")

qdrant = QdrantClient(url=st.secrets.qdrant_url,
                      api_key=st.secrets.qdrant_api_key)

qdrant.recreate_collection(
    collection_name="thoughts",
    vectors_config=models.VectorParams(
        # Vector size is defined by used model
        size=semantic_model.get_sentence_embedding_dimension(),
        distance=models.Distance.COSINE,
    ),
)


file = open("../raw/meditations.txt")
writing = file.read()
file.close()

clusters = cluster_text(writing)

records = []


for cluster in clusters:
    payload = {
        "persona_id": MARCUS_AURELIUS_PERSONA_ID,
        "thought": cluster
    }
    passage_record = models.Record(
        id=uuid.uuid4().hex, vector=semantic_model.encode(cluster).tolist(), payload=payload
    )

    records.append(passage_record)


qdrant.upload_records(collection_name="thoughts", records=records)
