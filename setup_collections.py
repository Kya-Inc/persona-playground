
# when you run this if you have errors set PYTHONPATH=../../../
import os
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv

load_dotenv()

qdrant = QdrantClient(url=os.environ.get("QDRANT_URL"),
                      api_key=os.environ.get("QDRANT_API_KEY")

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
