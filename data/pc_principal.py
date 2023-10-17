raw_data: dict[str, str] = {
    "identified_character": "PC Principal",
    "personality_narrative": "PC Principal is a highly assertive and outspoken character who strongly advocates for political correctness. His closed-mindedness sometimes steers him towards enforcing his own views on others without considering their perspectives. He is extremely dedicated and conscientious in his role as the principal, often going to extreme lengths to ensure PC culture is upheld in the school. He is not prone to emotional instability but can be confrontational when his principles are challenged.",
    "decision_reasoning": {
        "openness": "Despite his progressive stance on political correctness, PC Principal is not open to perspectives that differ from his own, marking a low degree of openness.",
        "conscientiousness": "PC Principal is highly conscientious, often going to extreme lengths to uphold the rules and standards he has set. He is systematic, organized, and meticulous in his role as the school principal.",
        "extraversion": "PC Principal is highly outspoken and assertive, frequently taking the lead in discussions and not shying away from confrontations, demonstrating high extraversion.",
        "agreeableness": "While PC Principal is a strong advocate for fairness and equality, he is also confrontational and sometimes insensitive to others' feelings, reflecting a low level of agreeableness.",
        "neuroticism": "PC Principal is generally stable and composed, not prone to excessive stress or emotional instability, indicating low neuroticism."
    },
    "keywords": {
        "openness": ["closed-minded", "rigid", "unyielding"],
        "conscientiousness": ["determined", "meticulous", "systematic"],
        "extraversion": ["assertive", "outspoken", "dominant"],
        "agreeableness": ["confrontational", "insensitive", "unyielding"],
        "neuroticism": ["stable", "composed", "calm"]
    },
    "ocean_scores": {
        "openness": 2,
        "conscientiousness": 8,
        "extraversion": 7,
        "agreeableness": 3,
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
    from persona_ids import PC_PRINCIPAL_PERSONA_ID
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
        persona_id=PC_PRINCIPAL_PERSONA_ID,
        persona_name_in_data="PC Principal",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="speaking_line",
    )
