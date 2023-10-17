raw_data: dict[str, str] = {
    "identified_character": "Squidward Tentacles",
    "personality_narrative": "Squidward Tentacles, the ornery neighbor from the show Spongebob Squarepants, has a personality marked by a high degree of Neuroticism and lower levels of Extraversion, Agreeableness, Conscientiousness, and Openness. Squidward's somewhat curmudgeonly demeanor and frequent irritation at his more buoyant neighbors speak volumes to his reclusive nature, hinting at a deep-seated dissatisfaction or perhaps a yearning for a reality different from the one he is currently inhabiting. It is interesting to note his complex personality, shaped by his solitary enjoyment of music and fine arts, juxtaposed with his general distaste for the lively shenanigans of the world around him.",
    "decision_reasoning": {
        "openness": "Squidward's interest in art and music suggests an above-average level of Openness. However, his resistance to the spontaneous antics of SpongeBob and Patrick suggests that he generally prefers routine and predictable environments.",
        "conscientiousness": "Although he is responsible and dutiful in his job at the Krusty Krab, his lack of ambition and general disgruntlement suggest lower levels of Conscientiousness.",
        "extraversion": "Squidward is unmistakably introverted. He prefers solitude, gets easily drained by social interactions, and often reacts negatively to the high-energy antics of his neighbors, SpongeBob and Patrick.",
        "agreeableness": "Squidward's frequent irritable and sarcastic responses to others suggest a low level of Agreeableness. He often seems dismissive of others' feelings or concerns and can be perceived as insensitive.",
        "neuroticism": "His frequent feelings of annoyance, impatience, anxiety, and often irrational approach towards SpongeBob and Patrick's antics show that Squidward's level of Neuroticism is quite high."
    },
    "keywords": {
        "openness": ["inquisitive in arts", "routine-lover", "resistant to change", "predictable"],
        "conscientiousness": ["dutiful", "unambitious", "disgruntled", "impatient"],
        "extraversion": ["introverted", "solitary", "drained by social interactions", "reclusive"],
        "agreeableness": ["irritable", "sarcastic", "dismissive", "insensitive"],
        "neuroticism": ["annoyed", "impatient", "anxious", "irrational"]
    },
    "ocean_scores": {
        "openness": 4,
        "conscientiousness": 3,
        "extraversion": 2,
        "agreeableness": 2,
        "neuroticism": 8
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
    from persona_ids import SQUIDWARD_TENTACLES_PERSONA_ID
    from embed import embed_character_dialogue
    import pandas as pd
    from pandas import DataFrame

    df: DataFrame = (
        pd.read_csv(
            "shared/spongebob_lines.csv",
            low_memory=False,
        )
    )
    df["speaking_line"] = 'line' in df.columns

    # then we pass the data frame to the character/data agnostic function that creates the embeddings
    embed_character_dialogue(
        df=df,
        persona_id=SQUIDWARD_TENTACLES_PERSONA_ID,
        persona_name_in_data="Squidward",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="spoken_line",
    )
