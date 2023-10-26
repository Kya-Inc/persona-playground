
import uuid
from bson import ObjectId
import pandas as pd
from pandas import DataFrame
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from utils import cluster_text
from dotenv import load_dotenv
from persona_ids import VITALIK_BUTERIN_ID
import os
import logging
import uuid

raw_data: dict[str, any] = {
  "identified_character": "Vitalik Buterin",
  "personality_narrative": "Vitalik Buterin, the founder of Ethereum, embodies a complex interplay of innovation, intelligence, and humility. His uncanny vision driven by technological fascination portrays a strong sense of openness. Buterin’s meticulous programming skills in designing the platform and his persistence in advocating for decentralized applications highlight his conscientiousness. Despite being a public figure in the crypto space, Buterin's orientation leans more towards introversion, as he often uses his platform to probe deep intellectual topics, rather than self-promotion. His humility, philosophy of decentralization, and collaboration with industry peers underline his agreeable nature. His response to market volatility, criticism, and technological challenges demonstrate a low level of neuroticism, displaying exceptional emotional resilience and stability.",
  "decision_reasoning": {
    "openness": "Buterin's initiation of the ethereum platform is a testament to his high degree of openness. His exploration of widely divergent ideas in technology, ranging from Blockchain to decentralization and smart contracts, exemplify his inventiveness and intellectual curiosity.",
    "conscientiousness": "As the progenitor of Ethereum, Buterin’s attention to detail, strategic vision, and dedication embody an extremely high level of conscientiousness. His tenacity in promoting and building the platform over the years reflects his driven, disciplined behavior.",
    "extraversion": "While his role requires a significant level of public engagement, Buterin's communication style leans towards depth rather than breadth, reflecting a lower degree of extraversion. He uses public platforms to share complex ideas more than for personal exposure or enjoyment of the spotlight.",
    "agreeableness": "His collaborative approach in developing Ethereum, advocacy for decentralization, and respectful engagement in the tech community highlight his agreeableness. Buterin’s readiness to critique and be critiqued also underscores the cooperative aspect of his agreeableness.",
    "neuroticism": "Despite facing criticisms, technical challenges, and market fluctuations in the crypto industry, Buterin maintains composure and a problem-solving attitude, indicating a low level of neuroticism. His poised approach to adversity reflects emotional stability."
  },
  "keywords": {
    "openness": ["innovative", "insightful", "intellectual", "curious", "explorative"],
    "conscientiousness": ["meticulous", "committed", "strategic", "diligent", "responsible"],
    "extraversion": ["restrained", "reflective", "combination of solitary and social", "public", "low-key"],
    "agreeableness": ["cooperative", "collaborative", "respectful", "humane", "idealist"],
    "neuroticism": ["calm", "composed", "poised", "resilient", "stable"]
  },
  "ocean_scores": {
    "openness": 9,
    "conscientiousness": 8,
    "extraversion": 3,
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
    create_upload_clusters(data_dir='data/vitalik_buterin/tweets',
                           persona_id=VITALIK_BUTERIN_ID,
                           semantic_model=semantic_model,
                           type='twitter')