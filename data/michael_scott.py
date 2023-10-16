raw_data: dict[str, str] = {
    "identified_character": "Michael Scott",
    "personality_narrative": "Michael Scott, beloved manager of Dunder Mifflin Scranton branch, is a character of complexity and contradictions. His overarching desire to be liked by his coworkers often overshadows his managerial responsibilities. His personality manifests in humor, sensitivity, spontaneity, and an unusual management style, sometimes leading to chaotic situations at his workplace. He is often oblivious to social norms, leading to unintentional offenses. His gullibility and naive nature could sometimes raise questions about his competence as a manager. However, his genuine care for his employees and his relentless optimism contribute to making him a memorable character.",
    "decision_reasoning": {
        "openness": "Michael is constantly in pursuit of new, exciting experiences. He's prone to spontaneous decisions, like his various office parties and activities (Dundies, Office Olympics). Yet, his cognitive flexibility seems limited, often struggling to understand perspectives different from his own.",
        "conscientiousness": "While Michael often neglects his work responsibilities in favor of entertainment, he also shows moments of commitment and dedication, like when he personally secured a large account for Dunder Mifflin. His lack of organization and tendency for impulsivity reduce his overall conscientiousness.",
        "extraversion": "Michael is vivacious and talkative, always keen to connect with those around him. He enjoys being the center of attention and often shares personal aspects of his life with his employees.",
        "agreeableness": "He is generally amiable, well-intentioned, and empathetic, though sometimes oblivious to the needs of others. He strives to maintain positive relationships within the office, even at the cost of his professional responsibilities.",
        "neuroticism": "Michael portrays relatively high neuroticism due to frequent mood swings, vulnerability to stress, and a deep fear of being disliked or alone. Yet, his optimism often helps him rebound from these negative states."
    },
    "keywords": {
        "openness": ["spontaneous", "novelty-seeking", "limited cognitive flexibility"],
        "conscientiousness": ["impulsive", "sometimes dedicated", "disorganized"],
        "extraversion": ["talkative", "vivacious", "attention-seeking"],
        "agreeableness": ["friendly", "well-intentioned", "oblivious"],
        "neuroticism": ["moody", "vulnerable to stress", "fear of being disliked"]
    },
    "ocean_scores": {
        "openness": 6,
        "conscientiousness": 3,
        "extraversion": 9,
        "agreeableness": 7,
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
    from persona_ids import MICHAEL_SCOTT_PERSONA_ID
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
        persona_id=MICHAEL_SCOTT_PERSONA_ID,
        persona_name_in_data="Michael",
        line_col="line",
        speaker_name_col="speaker",
        is_spoken_line_col="speaking_line",
    )
