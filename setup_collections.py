
# when you run this if you have errors set PYTHONPATH=../../../
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
import streamlit as st

qdrant = QdrantClient(url=st.secrets.qdrant_url,
                      api_key=st.secrets.qdrant_api_key)

semantic_model = SentenceTransformer("thenlper/gte-large")

qdrant.recreate_collection(
    collection_name="cues",
    vectors_config=models.VectorParams(
        size=semantic_model.get_sentence_embedding_dimension(),
        distance=models.Distance.COSINE,
    ),
)

qdrant.recreate_collection(
    collection_name="responses",
    vectors_config=models.VectorParams(
        size=semantic_model.get_sentence_embedding_dimension(),
        distance=models.Distance.COSINE,
    ),
)

qdrant.recreate_collection(
    collection_name="thoughts",
    vectors_config=models.VectorParams(
        size=semantic_model.get_sentence_embedding_dimension(),
        distance=models.Distance.COSINE,
    ),
)
