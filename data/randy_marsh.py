raw_data: dict[str, str] = {
    "identified_character": "Randy Marsh",
    "personality_narrative": "Randy Marsh is an easily excitable, somewhat impulsive, and zestful character. He possesses a high degree of openness with his penchant for trying new experiences and his creative, somewhat less conventional thought process. He has a relatively low degree of conscientiousness, often throwing himself into new experiences without much planning or consideration for possible consequences. Despite his eccentricities, Randy is very extroverted, enjoying the company of others and often being the life of the party. He is also quite agreeable, despite often finding himself in conflict due to his impulsive decisions, but this may be partly due to his low level of control over his emotions, hinting towards a higher level of neuroticism.",
    "decision_reasoning": {
        "openness": "Randy shows a high degree of openness with his tendency towards novel experiences, creative thinking, and personal eccentricity. He is not afraid to go against the grain when he believes in something.",
        "conscientiousness": "Randy's impulsive decisions and disregard for rules or regulations suggest a lower degree of conscientiousness. He is unstructured and prefers to go with the flow, even if it leads to chaos.",
        "extraversion": "Randy enjoys being in the company of others and often finds himself at the center of attention, indicating a high degree of extraversion. He thrives in social situations and is receptive to the energy of those around him.",
        "agreeableness": "Despite his impulsive actions, Randy is generally an agreeable person. He has a friendly, cooperative nature, though he may find himself in conflict due to his lack of forethought.",
        "neuroticism": "Randy often shows a lack of emotional stability, as he can be impulsive and somewhat unpredictable, suggesting a higher degree of neuroticism. He tends to experience a range of emotions and can sometimes struggle to manage his feelings."
    },
    "keywords": {
        "openness": ["creative", "imaginative", "adventurous", "unconventional"],
        "conscientiousness": ["impulsive", "disregard for rules", "unstructured", "spontaneous"],
        "extraversion": ["sociable", "gregarious", "outgoing", "attention-seeking"],
        "agreeableness": ["friendly", "cooperative", "compassionate", "conflict-prone"],
        "neuroticism": ["over-reactive", "emotional", "anxious", "impulsive"]
    },
    "ocean_scores": {
        "openness": 8,
        "conscientiousness": 3,
        "extraversion": 8,
        "agreeableness": 6,
        "neuroticism": 7
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
    from persona_ids import RANDY_MARSH_PERSONA_ID
    from embed import embed_character_dialogue
    import pandas as pd
    from pandas import DataFrame

    df: DataFrame = (
        pd.read_csv(
            "shared/south_park_lines.csv",
            low_memory=False,
        )
    )
    df["speaking_line"] = 'line' in df.columns

    # then we pass the data frame to the character/data agnostic function that creates the embeddings
    embed_character_dialogue(
        df=df,
        persona_id=RANDY_MARSH_PERSONA_ID,
        persona_name_in_data="Randy",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="speaking_line",
    )
