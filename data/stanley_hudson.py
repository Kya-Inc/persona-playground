raw_data: dict[str, str] = {
    "identified_character": "Stanley Hudson",
    "personality_narrative": "Stanley Hudson, a character from the TV Show 'The Office', is a diligent, hard-working, and focused individual with a strong preference for routine and predictability. He is not readily open to new experiences, and he tends to be quite reserved, expressing more introverted qualities. Stanley can sometimes be seen as gruff or unenthusiastic, which could be perceived as disagreeableness. He also appears to have a lower level of neuroticism, remaining calm and composed in most situations.",
    "decision_reasoning": {
        "openness": "Stanley often resists changes at work, and he typically prefers routine and predictability, suggesting a lower degree of openness. He has a limited range of interest, focused mostly on his work and his puzzle book hobby.",
        "conscientiousness": "Stanley is consistently portrayed as a reliable and diligent worker, which indicates a high level of conscientiousness. Despite not being passionate about his job, he always meets his sales targets and adheres to his responsibilities.",
        "extraversion": "Stanley prefers to keep to himself and appears to be more comfortable working alone rather than in a group, indicating low extraversion. He doesn't participate in office banter or social events unless absolutely necessary.",
        "agreeableness": "Stanley's interactions with his colleagues are typically straightforward and sometimes abrupt, suggesting low agreeableness. However, his attitude seems more related to his direct nature and desire for efficiency rather than malice.",
        "neuroticism": "Despite the often chaotic environment of 'The Office', Stanley remains remarkably unfazed. His low stress levels and calm demeanor suggest low neuroticism."
    },
    "keywords": {
        "openness": ["closed-minded", "consistent", "routine-oriented", "conventional"],
        "conscientiousness": ["diligent", "dependable", "methodical", "responsible"],
        "extraversion": ["reserved", "independent", "quiet", "solitary"],
        "agreeableness": ["direct", "uncompromising", "straightforward", "efficient"],
        "neuroticism": ["calm", "composed", "nonchalant", "stress-resistant"]
    },
    "ocean_scores": {
        "openness": 2,
        "conscientiousness": 8,
        "extraversion": 2,
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
    from persona_ids import STANLEY_HUDSON_PERSONA_ID
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
        persona_id=STANLEY_HUDSON_PERSONA_ID,
        persona_name_in_data="Stanley",
        line_col="line",
        speaker_name_col="speaker",
        is_spoken_line_col="speaking_line",
    )
