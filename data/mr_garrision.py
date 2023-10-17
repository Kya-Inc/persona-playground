raw_data: dict[str, str] = {
    "identified_character": "Mr. Garrison",
    "personality_narrative": "Mr. Garrison is a complicated character. He is often portrayed as eccentric, conflicted, and unpredictable. His openness to experience is quite high as he often explores unconventional ideas and even changed his own gender identity at one point. However, he also exhibits low conscientiousness, as shown by his erratic and sometimes irresponsible behavior. His level of extraversion is quite high, as he is rarely shy about expressing his often controversial opinions and feelings, even in inappropriate contexts. He is low on agreeableness due to his tendency to be critical, harsh, and confrontational. Lastly, his neuroticism is high, as his emotional stability varies greatly from one moment to another, often leading to dramatic displays of emotion.",
    "decision_reasoning": {
        "openness": "Mr. Garrison's high openness is displayed through his constant engagement with unconventional ideas and experiences. His willingness to alter his own gender identity is a clear testament to this trait.",
        "conscientiousness": "His low conscientiousness is evident in his erratic behavior, lack of dependability, and a general indifference to the consequence of his actions. He often neglects his duties, is impulsive, and lacks organization, which aligns with low conscientiousness.",
        "extraversion": "Mr. Garrison is a highly extraverted individual evident from his tendency to assert himself, his willingness to speak out, and his preference for being the center of attention.",
        "agreeableness": "His low level of agreeableness comes from his tendency to be combative, cynical, and insensitive towards others' feelings and needs. He is not hesitant to express harsh judgments and is often seen taking pleasure in others' discomfort.",
        "neuroticism": "Mr. Garrison exhibits high neuroticism through his frequent displays of various intense emotions. His emotional responses are often unpredictable and exaggerated, indicating a lack of emotional stability."
    },
    "keywords": {
        "openness": ["creative", "curious", "adventurous", "unconventional", "flexible"],
        "conscientiousness": ["impulsive", "disorganized", "irresponsible", "lacks dependability", "neglectful"],
        "extraversion": ["talkative", "assertive", "active", "social", "outgoing"],
        "agreeableness": ["cynical", "critical", "harsh", "insensitive", "combative"],
        "neuroticism": ["moody", "irritable", "impulsive", "volatile", "unpredictable"]
    },
    "ocean_scores": {
        "openness": 9,
        "conscientiousness": 2,
        "extraversion": 8,
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
    from persona_ids import MR_GARRISON_PERSONA_ID
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
        persona_id=MR_GARRISON_PERSONA_ID,
        persona_name_in_data="Mr. Garrison",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="speaking_line",
    )
