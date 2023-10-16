raw_data: dict[str, str] = {
    "identified_character": "Jim Halpert",
    "personality_narrative": "Jim Halpert from the television show 'The Office' is an overall easygoing and friendly individual. Known for his wit and playful attitude, Jim also shows a strong passion for his relationships, showcasing his emotional openness. He can be diligent and responsible when necessary, revealing a reasonable level of conscientiousness. Jim is generally sociable and comfortable in social situations, displaying a good deal of extraversion. He is agreeable, often displaying cooperative, compassionate, and friendly behavior. He has a low level of neuroticism, and handles stress well, viewed in his ability to manage in the chaotic and spontaneous environment of 'The Office'.",
    "decision_reasoning": {
        "openness": "Jim has been seen to be imaginative and inventive, as seen in his elaborate pranks on Dwight. He is also willing to experience and experiment with his emotion, as seen in his relationship with Pam.",
        "conscientiousness": "Jim's level of conscientiousness is influenced by context. At work, he is often seen as casual and nonchalant, not taking his job at Dunder Mifflin too seriously. However, he shows his responsible and organized side in his relationship with Pam and in his role as a father.",
        "extraversion": "Jim enjoys his social interactions, has a broad range of friends and acquaintances at the office, and is assertive in his humor and interaction, leading to his high rating in extraversion.",
        "agreeableness": "Jim's agreeableness is evident in his friendly and compassionate behaviors. He is often seen helping his co-workers and responsive to their needs. He is also good-natured and forgiving, even with Dwight's awkward or antagonistic behavior.",
        "neuroticism": "Jim tends to handle stress and crises with humor and calm, indicating a low level of neuroticism. He remains collected even in difficult situations, demonstrating emotional stability."
    },
    "keywords": {
        "openness": ["imaginative", "creative", "emotionally open", "adventurous"],
        "conscientiousness": ["responsible", "organized", "casual", "nonchalant"],
        "extraversion": ["sociable", "assertive", "friendly", "humorous"],
        "agreeableness": ["cooperative", "compassionate", "tolerant", "good-natured"],
        "neuroticism": ["composed", "calm under pressure", "emotionally stable", "low-stress"]
    },
    "ocean_scores": {
        "openness": 7,
        "conscientiousness": 5,
        "extraversion": 8,
        "agreeableness": 9,
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
    from persona_ids import JIM_HALPERT_PERSONA_ID
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
        persona_id=JIM_HALPERT_PERSONA_ID,
        persona_name_in_data="Jim",
        line_col="line",
        speaker_name_col="speaker",
        is_spoken_line_col="speaking_line",
    )
