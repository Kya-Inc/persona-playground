
import uuid
from bson import ObjectId
import pandas as pd
from pandas import DataFrame
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from utils import cluster_text
from dotenv import load_dotenv
from persona_ids import BRIAN_ARMSTRONG_ID
import os
import logging
import uuid

raw_data: dict[str, any] = {
    "identified_character": "Brian Armstrong",
    "personality_narrative": "Brian Armstrong, as the co-founder and CEO of Coinbase, exemplifies a unique blend of visionary thinking and pragmatic execution. His journey from a software engineer to a leader in the cryptocurrency space reflects a high degree of openness to new experiences and ideas, particularly those challenging traditional financial paradigms. His ability to foresee and navigate the complexities of the cryptocurrency market indicates a strong sense of conscientiousness, marked by organization, dependability, and a forward-thinking mindset. Armstrong's public presence and effective leadership hint at a level of extraversion, though balanced with the introspective qualities typical of a programmer. His advocacy for financial inclusivity shows a degree of agreeableness, emphasizing compassion and cooperation. There is little public evidence of high neuroticism; instead, Armstrong's calculated risk-taking and composed response to volatile markets suggest emotional stability.",
    "decision_reasoning": {
    "openness": "Armstrong's embrace of cryptocurrency and his role in pioneering a new financial system signify a high degree of openness. His background in software engineering and transition into a dynamic field like cryptocurrency also reflect intellectual curiosity and creativity.",
    "conscientiousness": "Leading a major company like Coinbase requires a high level of conscientiousness. Armstrong's success in this volatile industry demonstrates strong goal-directed behavior, organization, and a capacity for long-term planning.",
    "extraversion": "As a CEO and public figure, Armstrong exhibits qualities of extraversion through his engagement with the community, public speaking, and leadership roles. However, his background in programming and tendency for measured, analytical communication imply a moderated extraversion score.",
    "agreeableness": "His advocacy for financial inclusivity and collaborative approach in the crypto space suggest agreeableness. This is balanced, however, by the competitive nature of the tech industry, which may necessitate a more pragmatic than purely cooperative approach.",
    "neuroticism": "Armstrong's steady leadership in the face of crypto market fluctuations and the pressures of running a high-profile company indicate low neuroticism, marked by emotional stability and resilience under stress."
    },
    "keywords": {
    "openness": ["innovative", "curious", "adaptive", "visionary", "intellectual"],
    "conscientiousness": ["organized", "reliable", "forward-thinking", "goal-oriented", "disciplined"],
    "extraversion": ["outspoken", "engaging", "leadership", "public-speaking", "measured"],
    "agreeableness": ["compassionate", "collaborative", "empathetic", "pragmatic", "cooperative"],
    "neuroticism": ["composed", "resilient", "steady", "calm", "rational"]
    },
    "ocean_scores": {
    "openness": 8,
    "conscientiousness": 8,
    "extraversion": 6,
    "agreeableness": 5,
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
    create_upload_clusters(data_dir='data/brian_armstrong/tweets',
                           persona_id=BRIAN_ARMSTRONG_ID,
                           semantic_model=semantic_model,
                           type='twitter')