raw_data: dict[str, str] = {
    "identified_character": "Patrick Bateman",
    "personality_narrative": "Patrick Bateman is a complex character who embodies extreme psychological paradoxes. While being highly conscientious and methodical in his routines, he demonstrates sadistic tendencies and shows a deep-seated struggle with his identity. He craves acceptance and recognition, yet he is controlled by his violent urges. Patrick's excessive attention to detail, superficial charm, and his ability to disassociate from his violent acts create a haunting portrayal of a character plagued by an almost overwhelming sense of neuroticism.",
    "decision_reasoning": {
        "openness": "Patrick Bateman displays traditional interests and predictable behaviors, particularly in his strict routine and love for consumer culture. He lacks deep emotional receptivity or imagination, often choosing to emulate what he perceives is admired by his society. His actions suggest a low level of openness.",
        "conscientiousness": "Bateman is an overachiever, meticulously maintaining a guise of the typical Wall Street elite. His carefully cultivated physical appearance and rigid routines demonstrate high conscientiousness. However, he is an organized individual led not by morals, but by his detached and ruthless persona.",
        "extraversion": "As he thrives off social status and recognition, Patrick Bateman can be seen as extroverted. He enjoys social interactions, however, it is more for validation and acknowledgment than for forming meaningful relationships.",
        "agreeableness": "Bateman's agreeableness could be characterized as low. He manages to maintain a veneer of charm and politeness, but underneath this surface, he plays out violent fantasies and shows little empathy for others' feelings or needs.",
        "neuroticism": "Despite his cold and calm surface, Patrick Bateman portrays high neuroticism. He is plagued with anxiety, violent impulses, and an unstable sense of self, symptoms that often manifest in his hallucinations and the regular crisis of his identity."
    },
    "keywords": {
        "openness": ["unimaginative", "traditional", "predictable"],
        "conscientiousness": ["meticulous", "organized", "persistent"],
        "extraversion": ["attention-seeking", "charismatic", "social"],
        "agreeableness": ["manipulative", "uncaring", "insensitive"],
        "neuroticism": ["anxious", "impulsive", "unstable"]
    },
    "ocean_scores": {
        "openness": 2,
        "conscientiousness": 8,
        "extraversion": 7,
        "agreeableness": 2,
        "neuroticism": 9
    }
}

character_data = {
    "ocean_scores": "\n".join([f"{k}: {v}" for k, v in raw_data["ocean_scores"].items()]),
    "keywords": "\n".join([f"{k}: {', '.join(v)}" for k, v in raw_data["keywords"].items()]),
    "identified_character": raw_data["identified_character"],
    "personality_narrative": raw_data["personality_narrative"],
    "decision_reasoning": "\n".join([f"{k}: {v}" for k, v in raw_data["decision_reasoning"].items()])
}

# UPDATE this below before embedding Patrick Bateman again

if __name__ == "__main__":
    import uuid
    import streamlit as st
    import pandas as pd
    from pandas import DataFrame
    from qdrant_client import models, QdrantClient
    from sentence_transformers import SentenceTransformer

    from persona_ids import PATRICK_BATEMAN_PERSONA_ID

    data: DataFrame = pd.read_csv(
        "../raw/american_psycho.csv", sep="‚"
    )  # this isn't a normal comma btw
    df = pd.DataFrame(data)

    bateman_df: DataFrame = df[df["character"].isin(
        ["BATEMAN", "BATEMAN (V.O.)"])]

    qdrant = QdrantClient(url=st.secrets.qdrant_url,
                          api_key=st.secrets.qdrant_api_key)

    semantic_model = SentenceTransformer("thenlper/gte-large")

    documents: list = []
    for i, row in bateman_df.iterrows():
        response: str = row["line"]

        # Not likely the best way to deal with this, but for the monologue lines I am going to save them as prommpt and response for now. Just so they come up when searching for a prompt  and will allow searching for similar lines when searching for a response.k
        if row["character"] == "BATEMAN (V.O.)":
            prompt: str = row["line"]

            metadata = {
                "prompt": prompt,
                "response": response,
                "persona_id": PATRICK_BATEMAN_PERSONA_ID
            }

        else:
            prev_row = df.loc[i - 1]
            prev_char: str = prev_row["character"]
            prompt: str = prev_row["line"]

            context: DataFrame = df.loc[max(
                0, i - 2): i + 2][["character", "line"]]
            clean: DataFrame = context.dropna()
            chunk = clean.values.tolist()

            metadata = {
                "precontext": clean[0:2].to_json(orient="records"),
                "prompting_character": prev_char,
                "prompt": prompt,
                "response": response,
                "postcontext": clean[2:].to_json(orient="records"),
                "persona_id": PATRICK_BATEMAN_PERSONA_ID
            }

        documents.append(metadata)

    print(documents)

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
    qdrant.upload_records(collection_name="responses",
                          records=response_records)
