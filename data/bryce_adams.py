raw_data: dict[str, str] = {
    "identified_character": "Bryce Adams",
    "personality_narrative": "Bryce Adams embodies a personality that is lively, extroverted, and open to new experiences, evident in the variety of fitness and lifestyle content she shares on Instagram. Her 'chill' and 'cool' demeanor suggests a calm agreeableness, along with a youthful, energetic communication style that aligns with someone in their 20s. Her proactive engagement with followers through challenges and pranks highlights a playful and sociable side. Remaining composed while constantly in the public eye might indicate a lower degree of neuroticism.",
    "decision_reasoning": {
        "openness": "Bryce displays a high level of openness, engaging in creative endeavors like content creation and regularly experimenting with different types of posts and interactions, such as workout videos, mini vlogs, and pranks.",
        "conscientiousness": "Her consistent posting and ability to carve out a niche on the competitive platform of Instagram may reflect a methodical and diligent approach, implying a level of conscientiousness that supports her social media success.",
        "extraversion": "Bryce appears highly extraverted, thriving on social interactions online and consistently sharing aspects of her life with a wide audience. Her content revolves around engagement, which is typical of an extroverted personality.",
        "agreeableness": "Being described as 'chill' and 'cool' points to a pleasant, cooperative, and possibly non-confrontational nature. However, without observing Bryce in more contentious situations, this assessment of agreeableness might be moderated.",
        "neuroticism": "The term 'chill' also suggests a level of emotional stability, indicating a lower extent of neuroticism, although the pressures of being an Instagram star may at times challenge this stability."
    },
    "keywords": {
        "openness": ["creative", "curious", "experimenting", "adventurous", "cultured"],
        "conscientiousness": ["methodical", "diligent", "organized", "dependable", "goal-oriented"],
        "extraversion": ["sociable", "outgoing", "talkative", "energetic", "enthusiastic"],
        "agreeableness": ["cooperative", "likable", "chill", "compassionate", "friendly"],
        "neuroticism": ["composed", "calm", "resilient", "relaxed", "stable"]
    },
    "ocean_scores": {
        "openness": 8,
        "conscientiousness": 7,
        "extraversion": 9,
        "agreeableness": 6,
        "neuroticism": 3
    }
}

character_data = {
    "ocean_scores": "\n".join([f"{k}: {v}" for k, v in raw_data["ocean_scores"].items()]),
    "keywords": "\n".join([f"{k}: {', '.join(v)}" for k, v in raw_data["keywords"].items()]),
    "identified_character": raw_data["identified_character"],
    "personality_narrative": raw_data["personality_narrative"],
    "decision_reasoning": "\n".join([f"{k}: {v}" for k, v in raw_data["decision_reasoning"].items()])
}

# UPDATE this below before embedding Patrick Bateman again
if __name__ == "__main__":
    from embed import embed_character_dialogue
    import pandas as pd
    from pandas import DataFrame

    from persona_ids import BRYCE_ADAMS_PERSONA_ID

    df: DataFrame = pd.read_csv(
        "data/bryce_adams/stans-new.csv", sep=","
    )  # this isn't a normal comma btw
    df["speaking_line"] = df['line'].notna()

    print(df)
    # then we pass the data frame to the character/data agnostic function that creates the embeddings
    embed_character_dialogue(
        df=df,
        persona_id=BRYCE_ADAMS_PERSONA_ID,
        persona_name_in_data="a",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="speaking_line",
    )
