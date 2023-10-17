raw_data: dict[str, str] = {
    "identified_character": "Satoshi Nakamoto",
    "personality_narrative": "Satoshi Nakamoto is known for the revolutionary invention of Bitcoin, displaying remarkable levels of curiosity, intellectual openness, and high conscientiousness. He is characterized by his consistent preference for solitude, hinting at a low level of extraversion. His relationships are primarily based on intellectual grounds rather than emotional connections, showcasing low agreeableness. Furthermore, his ability to withstand the uncertainty surrounding his invention signifies a low level of neuroticism.",
    "decision_reasoning": {
        "openness": "Satoshi displayed a high level of openness, considering his innovative development and the willingness to introduce a novel concept of cryptocurrency to the world. This shows his imaginative, creative, and pioneering flair.",
        "conscientiousness": "Without observable instances of impulsive behavior and given his achievement in creating Bitcoin, we infer he had a high level of conscientiousness. His meticulousness, ambition, and perseverance are evident.",
        "extraversion": "Satoshi Nakamoto's preference to remain anonymous and not to seek fame or attention indicates a very low level of extraversion. Also, he never identified himself to the general public, indicating introverted tendencies.",
        "agreeableness": "His decisions to remain anonymous and avoid personal relationships signal a low level of agreeableness. He seems to have prioritized his intellectual pursuits over building social connections.",
        "neuroticism": "Despite the controversy and volatility around Bitcoin, Satoshi maintained his composure, which suggests a low level of neuroticism. His ability to handle stress and remain secure in the face of criticism is notable.",
    },
    "keywords": {
        "openness": ["innovative", "creative", "intellectual", "curious", "visionary"],
        "conscientiousness": [
            "meticulous",
            "determined",
            "responsible",
            "ambitious",
            "persevering",
        ],
        "extraversion": [
            "introverted",
            "reserved",
            "solitary",
            "self-contained",
            "discreet",
        ],
        "agreeableness": [
            "independent",
            "unperturbed",
            "non-empathic",
            "reserved",
            "objective",
        ],
        "neuroticism": ["calm", "secure", "composed", "steady", "resilient"],
    },
    "ocean_scores": {
        "openness": 9,
        "conscientiousness": 9,
        "extraversion": 2,
        "agreeableness": 3,
        "neuroticism": 2,
    },
}


character_data = {
    "ocean_scores": "\n".join(
        [f"{k}: {v}" for k, v in raw_data["ocean_scores"].items()]
    ),
    "keywords": "\n".join(
        [f"{k}: {', '.join(v)}" for k, v in raw_data["keywords"].items()]
    ),
    "identified_character": raw_data["identified_character"],
    "personality_narrative": raw_data["personality_narrative"],
    "decision_reasoning": "\n".join(
        [f"{k}: {v}" for k, v in raw_data["decision_reasoning"].items()]
    ),
}

if __name__ == "__main__":
    # when you run this if you have errors set PYTHONPATH=../../../
    from urllib import response
    import uuid
    import streamlit as st  # yes I'm lazy and doing this for the global secrets
    import pandas as pd
    from pandas import DataFrame
    from qdrant_client import models, QdrantClient
    from sentence_transformers import SentenceTransformer
    from persona_ids import SATOSHI_NAKAMOTO_PERSONA_ID
    from dotenv import load_dotenv
    import os

    load_dotenv()

    qdrant = QdrantClient(url=os.environ.get("QDRANT_URL"),
                          api_key=os.environ.get("QDRANT_API_KEY"))

    semantic_model = SentenceTransformer("thenlper/gte-large")

    # cue and response pairs
    data: DataFrame = pd.read_json("satoshi_nakamoto/cue-response-pairs.json")
    df = pd.DataFrame(data)

    documents = []
    for i, row in df.iterrows():
        cue = row["q"]
        response = row["a"]
        metadata = {
            "cue": cue,
            "response": response,
            "data": row["date"],
            "src": row["src"],
            "persona_id": SATOSHI_NAKAMOTO_PERSONA_ID
        }

        documents.append(metadata)

    cue_records = []
    response_records = []

    for doc in documents:
        response_encoding = doc["response"]
        if isinstance(response_encoding, float):
            print("problem document: ", doc)
        if isinstance(response_encoding, str):

            id = uuid.uuid4().hex
            cue_record = models.Record(
                id=id,
                vector=semantic_model.encode(doc["cue"]).tolist(),
                payload=doc
            )

            response_record = models.Record(
                id=id,
                vector=semantic_model.encode(doc["response"]).tolist(),
                payload=doc
            )

        cue_records.append(cue_record)
        response_records.append(response_record)

    qdrant.upload_records(collection_name="cues", records=cue_records)
    qdrant.upload_records(collection_name="responses",
                          records=response_records)

    print("cues: ", len(cue_records))
    print("responses: ", len(response_records))
