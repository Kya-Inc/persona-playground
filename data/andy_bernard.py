raw_data: dict[str, str] = {
    "identified_character": "Andy Bernard from The Office",
    "personality_narrative": "Andy Bernard, a character from The Office, is known for his dramatic shifts in mood and his constant need for external validation. He is also easily moved by his emotions, which can often cloud his decisions. His frequent breaks in discipline demonstrate his difficulty with self-regulation. Andy is also seen as open and conscientious to a certain degree, as he navigates through his workplace and social interactions. Although he may appear outwardly friendly and cordial, his agreeableness may be motivated by his desire to be accepted rather than genuine interest or affinity for others. His level of neuroticism is notable, impacting his relationships and professional life.",
    "decision_reasoning": {
        "openness": "Andy's character displays a degree of openness, reflected in his ability to embrace change, such as when he steps up to take charge as the regional manager. He also has a wide array of interests, ranging from a cappella music to golf, indicative of an openness to experience.",
        "conscientiousness": "Andy's conscientiousness is variable. Although he has shown a desire to do well and be responsible, such as when he obtained his MBA, his impulsive behavior and lack of discipline, as evidenced by his sudden departure on a boat trip, indicate low levels of conscientiousness.",
        "extraversion": "Andy is highly extroverted, consistently seeking social interaction, validation, and being the center of attention - such as his constant singing and performing. His energetic and talkative nature, and his need for affirmation, denote his high extraversion levels.",
        "agreeableness": "While Andy is often friendly and tries to maintain positive relations with colleagues, these interactions are often driven by his need for approval, suggesting that his agreeableness might be more strategic than genuine.",
        "neuroticism": "Andy's high neuroticism is underscored by his mood volatility and emotional instability. His anger issues, insecurity, and propensity to stress further highlight his high level of neuroticism."
    },
    "keywords": {
        "openness": ["Change-embracing", "Wide-ranging interests", "Adaptable"],
        "conscientiousness": ["Variable", "Impulsive", "Lack of Discipline"],
        "extraversion": ["Talkative", "Attention-seeking", "Outgoing"],
        "agreeableness": ["Friendly", "Approval-seeking", "Strategic"],
        "neuroticism": ["Mood Volatility", "Insecure", "Stress-prone"]
    },
    "ocean_scores": {
        "openness": 6,
        "conscientiousness": 3,
        "extraversion": 8,
        "agreeableness": 5,
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
    from persona_ids import ANDY_BERNARD_PERSONA_ID
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
        persona_id=ANDY_BERNARD_PERSONA_ID,
        persona_name_in_data="Andy",
        line_col="line",
        speaker_name_col="speaker",
        is_spoken_line_col="speaking_line",
    )
