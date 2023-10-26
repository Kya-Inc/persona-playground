
import uuid
from bson import ObjectId
import pandas as pd
from pandas import DataFrame
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from utils import cluster_text
from dotenv import load_dotenv
from persona_ids import SBF_ID
import os
import logging
import uuid

raw_data: dict[str, any] = {
  "identified_character": "Sam Bankman Fried",
  "personality_narrative": "Sam Bankman Fried, the young dynamo CEO of FTX, is a unique blend of innovative thinking, diligent work ethic, and humanitarian spirit. His remarkable ascent in the fickle world of cryptocurrency trading epitomizes his openness toward novel ideas and willingness to take calculated risks. His meticulous attention to detail, disciplined schedule, and the capacity to make sense of complex situations manifest an outstanding degree of conscientiousness. His reserved demeanor suggests a relatively low extraversion score, balanced by his eloquent proactivity in niche discussions. Sam's philanthropic endeavors highlight a robust agreeableness trait, while his composure amidst business volatility attests to a low neuroticism score.",
  "decision_reasoning": {
    "openness": "Sam's early adoption and mastery of cryptocurrency trading, combined with his willingness to innovate from the ground up, clearly demonstrate a very high degree of Openness. His venture into the largely-uncharted domain of cryptocurrencies signifies intellectual curiosity and a generous receptivity towards novel experiences.",
    "conscientiousness": "Sam's notorious work ethic, knack for operational complexity, and tireless devotion to navigating the evolving cryptocurrency markets support an extremely high Conscientiousness score. His diligent, disciplined conduct implies a strong orientation towards duty and achievement.",
    "extraversion": "Despite being an articulate communicator, Sam tends to maintain a small, selective social circle and comes across reserved which suggests a lower score on Extraversion. However, his public-speaking engagements increase this score somewhat.",
    "agreeableness": "Sam's commitment to philanthropy illustrates a high degree of Agreeableness. His mutually beneficial approach to business partnerships and collaborative attitude also enhance this score.",
    "neuroticism": "Sam's operational steadiness, even amidst the notorious volatility of cryptocurrency markets, displays a low level of Neuroticism. His resilience and composed demeanor are suggestive of substantial emotional stability."
  },
  "keywords": {
    "openness": ["innovative", "risk-taker", "creative", "visionary", "intellectual curiosity"],
    "conscientiousness": ["meticulous", "disciplined", "workaholic", "dutiful", "achievement-oriented"],
    "extraversion": ["eloquent", "reserved", "proactive", "selective", "moderate"],
    "agreeableness": ["philanthropic", "compassionate", "collaborative", "mutual benefit", "cooperative"],
    "neuroticism": ["composure", "resilient", "emotionally steady", "low volatility","calm"]
  },
  "ocean_scores": {
    "openness": 9,
    "conscientiousness": 9,
    "extraversion": 4,
    "agreeableness": 7,
    "neuroticism": 2
  }
}
character_data = {
    "identified_character": raw_data["identified_character"],
    "personality_narrative": raw_data["personality_narrative"],
    "decision_reasoning": "\n".join([f"{k}: {v}" for k, v in raw_data["decision_reasoning"].items()]),
    "keywords": "\n".join([f"{k}: {', '.join(v)}" for k, v in raw_data["keywords"].items()]),
    "ocean_scores": "\n".join([f"{k}: {v}" for k, v in raw_data["ocean_scores"].items()])
}


def ensure_collection_exists(collection_name, qdrant,embed_size=1):
    existing_collections = [col.name for col in qdrant.get_collections().collections]
    print("Existing collections: ", existing_collections)

    if collection_name not in existing_collections:
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=embed_size,
                distance=models.Distance.COSINE,
            ),
        )


# print(character_data)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_upload_clusters(data_dir, persona_id, semantic_model, collection='thoughtsCrypto', type=None):
    logging.info("Initializing cluster creation and upload process.")
    qdrant = QdrantClient(url=os.environ.get("QDRANT_URL"), api_key=os.environ.get("QDRANT_API_KEY"))

    try:
        ensure_collection_exists(collection_name=collection, qdrant=qdrant, embed_size=semantic_model.get_sentence_embedding_dimension())
    except Exception as e:
        logging.error(f"Error ensuring collection exists: {e}")
        return

    data_clusters = []
    for file_name in os.listdir(data_dir):
        path = os.path.join(data_dir, file_name)
        try:
            with open(path, 'r') as file:
                writing = file.read()
            clusters = cluster_text(writing)
            data_clusters.append(clusters)
            logging.info(f"Processed and clustered file: {path}")
        except Exception as e:
            logging.error(f"Error reading or clustering file {path}: {e}")
            continue

    total_records = 0
    for clusters in data_clusters:
        records = []
        for cluster in clusters:
            payload = {"persona_id": persona_id, "from": type, "thought": cluster}
            
            passage_record = models.Record(
                id=uuid.uuid4().hex,
                vector=semantic_model.encode(cluster).tolist(),
                payload=payload
            )
            records.append(passage_record)
            total_records += 1

        if records:
            try:
                qdrant.upload_records(collection_name=collection, records=records)
                logging.info(f"Uploaded {len(records)} records to collection '{collection}'.")
            except Exception as e:
                logging.error(f"Error uploading records to collection '{collection}': {e}")
    
    logging.info(f"Total records inserted for type '{type}': {total_records} in collection '{collection}'.")
    return clusters  # Returning the last set of clusters; adjust if necessary

    

if __name__ == "__main__":

    load_dotenv()
    # print(uuid.uuid1())
    
    semantic_model = SentenceTransformer("thenlper/gte-large")

    # create_upload_clusters(data_dir='data/brian_armstrong/blogs',
    #                        persona_id=brian_id,
    #                        semantic_model=semantic_model,
    #                        type='blogs')
    
    # Twitter
    create_upload_clusters(data_dir='data/sbf/tweets',
                           persona_id=SBF_ID,
                           semantic_model=semantic_model,
                           type='twitter')