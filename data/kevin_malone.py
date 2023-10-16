raw_data: dict[str, str] = {
    "identified_character": "Kevin Malone",
    "personality_narrative": "Kevin Malone is a character marked by his simplicity and lack of pretentiousness. While he might not be the most diligent worker, he displays a certain charm through his straightforwardness and aversion to office politics. His passivity and agreeable nature, however, may be interpreted by some as a lack of social dynamism or assertiveness. Kevin often appears to be more focused on present gratification, such as his love for food, than considering long-term consequences, indicating low levels of Conscientiousness. Although he isn't a typical extravert, his openness to experience is evident in his passion for his band and his enjoyment of a good joke.",
    "decision_reasoning": {
        "openness": "Kevin is open to new experiences, as seen in his love for his band and enjoyment of humor. However, he does not show great interest in intellectual pursuits and is predominantly interested in tangible, easily understandable experiences.",
        "conscientiousness": "Kevin is not particularly conscientious. He’s been depicted as lazy and often procrastinates his tasks. His desk and life outside work both appear somewhat disorganized, and he doesn’t seem overly concerned with achieving high performance.",
        "extraversion": "Despite his quiet demeanor, Kevin enjoys social activities and is part of a band. He is not very assertive or dominant but does not shy away from group activities and enjoys attention when it involves his interests.",
        "agreeableness": "Kevin is a friendly and agreeable individual. He rarely engages in conflicts and is often the 'follower' rather than the 'leader'. His warmth and friendliness make him a pleasant companion, although his agreeableness might contribute to his lack of assertiveness.",
        "neuroticism": "Kevin is generally emotionally stable and handles stress well, rarely seen panicking or becoming overly anxious. His laid-back attitude may contribute to his low sense of urgency or motivation, but it also enables him to maintain emotional steadiness."
    },
    "keywords": {
        "openness": ["tangible-interests", "curious", "open-minded", "low-intellectual-interest"],
        "conscientiousness": ["impulsive", "disorganized", "procrastinator", "laid-back"],
        "extraversion": ["quiet", "social", "non-dominant", "congenial"],
        "agreeableness": ["friendly", "cooperative", "non-assertive", "compliant"],
        "neuroticism": ["emotionally-stable", "calm", "relaxed", "low-stress"]
    },
    "ocean_scores": {
        "openness": 6,
        "conscientiousness": 2,
        "extraversion": 5,
        "agreeableness": 7,
        "neuroticism": 2
    }
}

character_data = {
    "ocean_scores": "\n".join([f"{k}: {v}" for k, v in raw_data["ocean_scores"].items()]),
    "keywords": "\n".join([f"{k}: {', '.join(v)}" for k, v in raw_data["keywords"].items()]),
    "identified_character": raw_data["identified_character"],
    "personality_narrative": raw_data["personality_narrative"],
    "decision_reasoning": "\n".join([f"{k}: {v}" for k, v in raw_data["decision_reasoning"].items()])
}

if __name__ == "__main__":
    from persona_ids import KEVIN_MALONE_PERSONA_ID
    from embed import embed_character_dialogue
    import pandas as pd
    from pandas import DataFrame

    df: DataFrame = (
        pd.read_csv(
            "shared/the_office_lines.csv",
            low_memory=False,
        )
    )
    df = df.drop(df.columns[6], axis=1)
    df["speaking_line"] = 'line' in df.columns

    # # then we pass the data frame to the character/data agnostic function that creates the embeddings
    embed_character_dialogue(
        df=df,
        persona_id=KEVIN_MALONE_PERSONA_ID,
        persona_name_in_data="Kevin",
        line_col="line",
        speaker_name_col="speaker",
        is_spoken_line_col="speaking_line",
    )
