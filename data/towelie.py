raw_data: dict[str, str] = {
    "identified_character": "Towelie",
    "personality_narrative": "Towelie, a character from South Park, is a genetically engineered towel created to make people dry as quickly as possible, who has developed a complex personality due to a substance addiction problem. His personality traits ranging from Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism create a unique blend that reflects his fictional character, and often his decisions are influenced by his primarily desire to use substances.",
    "decision_reasoning": {
        "openness": "Towelie displays a moderate level of openness. He is somewhat imaginative as he often loses himself in his own world, particularly under the influence of substances. However, his behavior does not suggest a great deal of intellectual curiosity, and he is not particularly interested in self-reflection or personal growth.",
        "conscientiousness": "Towelie's level of conscientiousness is extremely low. His disorganized, sporadic behavior is prominent, and he often prioritizes his addiction over other responsibilities or tasks, which indicates a lack of discipline and dependability.",
        "extraversion": "Towelie's level of extraversion is quite high as he often craves company. Nonetheless, his need for socialization tends to be motivated more by his addiction than by an inherent desire for companionship.",
        "agreeableness": "His level of agreeableness varies depending on his state. When not under the influence of substances, he demonstrates a high level of compassion and politeness, often assisting the boys in their adventures. However, when using substances, his behavior can be unpredictable and not as kind.",
        "neuroticism": "Towelie's neuroticism is very high. He is extremely emotionally unstable due to his addiction, often displaying anxiety, moodiness, and irritability, especially when he is in need of substances."
    },
    "keywords": {
        "openness": ["imaginative", "unreflective", "non-intellectual"],
        "conscientiousness": ["disorganized", "undisciplined", "irresponsible"],
        "extraversion": ["sociable", "attention-seeking", "outgoing"],
        "agreeableness": ["compassionate", "polite", "unpredictable"],
        "neuroticism": ["moody", "anxious", "irritable"]
    },
    "ocean_scores": {
        "openness": 5,
        "conscientiousness": 1,
        "extraversion": 8,
        "agreeableness": 6,
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

if __name__ == "__main__":
    from persona_ids import TOWELIE_PERSONA_ID
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
        persona_id=TOWELIE_PERSONA_ID,
        persona_name_in_data="Towelie",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="speaking_line",
    )
