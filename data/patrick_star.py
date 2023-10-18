raw_data: dict[str, str] = {
    "identified_character": "Patrick Star",
    "personality_narrative": "Patrick Star, the pink starfish from Spongebob Squarepants, is characterized by his simple-mindedness and eccentric lifestyle. He is a loyal and sweet-natured friend who enjoys engaging in fun activities, often without a sense of consequence or responsibility. His naiveness may sometimes cause trouble, but his intentions are always in the right place. His emotional stability varies, as he can easily become anxious in unfamiliar situations or when things don't go according to plan.",
    "decision_reasoning": {
        "openness": "Patrick Star shows an average level of openness. He is curious and imaginative in his fun-seeking behavior and comes up with creative solutions for problems, even if they aren't always effective. He doesn't have a broad range of interests and tends to stick to familiar and comfortable terrain.",
        "conscientiousness": "Patrick’s level of conscientiousness is extremely low. He is often impulsive, disorganized, and has a poor sense of duty or obligation. He lacks clear goals or aspirations and tends to live in the moment, often failing to understand the consequences of his actions.",
        "extraversion": "Patrick's high degree of extraversion is seen in his social nature and love for adventures. Even though his social skills are not always perfect, he is genuinely excited about social interactions and adventures with his best friend, SpongeBob.",
        "agreeableness": "Patrick's agreeableness is high. Despite his occasional selfishness and naiveness, he is usually friendly, compassionate, and willing to help his friends in times of need. He can, however, be easily influenced and manipulated due to his gullibility.",
        "neuroticism": "Patrick's neuroticism fluctuates depending on the situation. Generally, he appears emotionally stable, but he can get anxious and react dramatically when things do not go according to plan, or when he is faced with unfamiliar and threatening situations."
    },
    "keywords": {
        "openness": ["curious", "imaginative", "simple-minded"],
        "conscientiousness": ["impulsive", "disorganized", "lacking responsibility"],
        "extraversion": ["sociable", "adventure-loving", "gregarious"],
        "agreeableness": ["friendly", "helpful", "gullible"],
        "neuroticism": ["fluctuating emotional stability", "reactive", "anxious"]
    },
    "ocean_scores": {
        "openness": 5,
        "conscientiousness": 1,
        "extraversion": 8,
        "agreeableness": 7,
        "neuroticism": 4
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
    from persona_ids import PATRICK_STAR_PERSONA_ID
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
        persona_id=PATRICK_STAR_PERSONA_ID,
        persona_name_in_data="Patrick",
        line_col="line",
        line_raw_col="raw_text",
        speaker_name_col="character",
        is_spoken_line_col="spoken_line",
    )
