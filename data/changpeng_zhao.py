
import uuid
from bson import ObjectId
import pandas as pd
from pandas import DataFrame
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from utils import cluster_text
from dotenv import load_dotenv
from persona_ids import CHANGPENG_ZHAO_ID
import os
import logging
import uuid

raw_data: dict[str, any] = {
  "identified_character": "Changpeng Zhao",
  "personality_narrative": "Changpeng Zhao is a highly driven and dynamic individual, characterized by his openness to new ideas and willingness to take risks. He displays a strong sense of conscientiousness, ensuring that tasks are completed efficiently and effectively. Despite his reserved nature, Zhao demonstrates extraverted tendencies when in social or professional settings. He is known for his agreeable nature and ability to build strong relationships with others. However, his high neuroticism suggests that he may experience frequent emotional fluctuations and anxiety.",
  "decision_reasoning": {
    "openness": "Changpeng Zhao exhibits a high level of openness based on his willingness to embrace new ideas and undertake new ventures. This is evident in his role as the founder and CEO of Binance, where he has revolutionized the cryptocurrency industry with innovative solutions and a global perspective. His decision to explore blockchain technology and create a decentralized exchange demonstrates his curiosity and desire to challenge traditional norms.",
    "conscientiousness": "Changpeng Zhao's conscientiousness is apparent in his meticulous attention to detail and strong work ethic. He is known for his ability to execute tasks efficiently and effectively, ensuring that projects are completed to the highest standard. His dedication to accuracy and precision is reflected in the success of Binance, which has become one of the largest cryptocurrency exchanges in the world under his leadership.",
    "extraversion": "While Changpeng Zhao may appear reserved in certain situations, he demonstrates extraverted traits when interacting with others in social or professional settings. He is comfortable leading large teams and engaging in public speaking engagements, showcasing his ability to connect with individuals on a personal level. His charisma and ability to energize those around him contribute to his success as a leader in the cryptocurrency industry.",
    "agreeableness": "Changpeng Zhao is highly agreeable and values harmonious relationships with others. He is known for his collaborative approach and ability to work well in team environments. His empathetic nature allows him to understand and appreciate the perspectives of others, facilitating effective communication and cooperation. This agreeableness is reflected in his dedication to creating a supportive and inclusive work culture at Binance.",
    "neuroticism": "Changpeng Zhao exhibits a high level of neuroticism, characterized by frequent emotional fluctuations and anxiety. This may be attributed to the immense pressure and responsibility associated with leading a global cryptocurrency exchange. Despite these challenges, Zhao has developed strong coping mechanisms and resilience, allowing him to navigate stressful situations and make well-informed decisions."
  },
  "keywords": {
    "openness": ["innovative", "curious", "global perspective"],
    "conscientiousness": ["meticulous", "strong work ethic", "attention to detail"],
    "extraversion": ["charismatic", "energetic", "comfortable in social settings"],
    "agreeableness": ["collaborative", "empathetic", "inclusive"],
    "neuroticism": ["emotional fluctuations", "anxiety", "resilience"]
  },
  "ocean_scores": {
    "openness": 7,
    "conscientiousness": 8,
    "extraversion": 6,
    "agreeableness": 7,
    "neuroticism": 7
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
    create_upload_clusters(data_dir='data/cz/tweets',
                           persona_id=CHANGPENG_ZHAO_ID,
                           semantic_model=semantic_model,
                           type='twitter')