raw_data: dict[str, str] = {
    "identified_character": "Stan Marsh",
    "personality_narrative": "Stan Marsh, a leading character from South Park, showcases a balanced personality. He's often the voice of reason among his friends and embodies a moral compass, showcasing high conscientiousness. He's somewhat extroverted, primarily when he's in his comfort zone with his close friends. However, his openness varies, as he can be a bit resistant to new experiences. His agreeableness is evident in his interactions, as he often seeks to mediate conflicts, but he deals with a certain level of neuroticism, facing anxiety in various situations.",
    "decision_reasoning": {
        "openness": "Stan normally prefers familiarity over novelty, showing a moderate reserve to new experiences. Nevertheless, he's capable of adapting when required, hinting at a level of flexibility. His level of openness can be understood as a bit low.",
        "conscientiousness": "Stan shows a high level of conscientiousness. He's dependable and likes to stick to a moral code, often coming across as the 'voice of reason' among his friends. He displays responsibility in his actions, making him a highly conscientious individual.",
        "extraversion": "Stan is somewhat extrovert. He's comfortable interacting with his small circle of friends, but he doesn’t appear to seek out high-intensity experiences or large social gatherings. His level of extraversion can be seen as a bit high.",
        "agreeableness": "His high level of agreeableness is undeniable. Stan's frequently seen making efforts to mediate conflicts, showing empathy and concern for others' welfare. He is cooperative, friendly, and values harmony.",
        "neuroticism": "Stan is prone to bouts of anxiety, showing a moderate level of neuroticism. He's seen struggling with the chaos around him, often falling into worry and distress."
    },
    "keywords": {
        "openness": ["reserved", "flexible", "familiarity-seeking"],
        "conscientiousness": ["responsible", "dependable", "moral"],
        "extraversion": ["sociable", "comfortable in small groups", "moderate intensity"],
        "agreeableness": ["mediator", "cooperative", "friendly", "empathetic"],
        "neuroticism": ["anxiety-prone", "worried", "distressed"]
    },
    "ocean_scores": {
        "openness": 4,
        "conscientiousness": 8,
        "extraversion": 6,
        "agreeableness": 8,
        "neuroticism": 6
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
    from persona_ids import STAN_MARSH_PERSONA_ID
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
        persona_id=STAN_MARSH_PERSONA_ID,
        persona_name_in_data="Stan",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="speaking_line",
    )
