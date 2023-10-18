raw_data: dict[str, str] = {
    "identified_character": "Mr. Krabs",
    "personality_narrative": "Mr. Krabs, also known as Eugene H. Krabs, is the owner of the Krusty Krab restaurant in the animated series 'SpongeBob SquarePants'. His character is defined primarily by his frugality and love of money, which often leads him to take drastic action to protect his wealth. Despite these seemingly negative traits, Mr. Krabs has a softer side, showing paternal care towards his daughter, Pearl, and occasionally towards Spongebob and Squidward, his employees. He's notably wary of innovation and prefers traditional, tried-and-tested ways of doing things.",

    "decision_reasoning": {
        "openness": "Mr. Krabs scores low on openness. He's generally resistant to change and prefers sticking with what works from a business perspective. He resists innovation and new ideas, particularly if they come with a financial risk.",
        "conscientiousness": "Mr. Krabs' conscientiousness is notably high, especially in terms of his carefulness, vigilance, and reliability as a business owner. He takes his responsibilities seriously, even when they relate to his obsession with money.",
        "extraversion": "His extraversion is relatively high. Mr. Krabs is outspoken, assertive, and enjoys social interaction - especially when it can lead to profit.",
        "agreeableness": "In terms of agreeableness, Mr. Krabs scores rather low. While he can show affection to those close to him, he usually prioritizes his own interests, especially monetary ones, over the needs of others.",
        "neuroticism": "Mr. Krabs is high in neuroticism. His constant worry about losing his money and the security of his business displays a high level of anxiety, and he tends to react strongly when things go wrong."
    },

    "keywords": {
        "openness": ["traditionalist", "risk-averse", "unadventurous", "stick-in-the-mud"],
        "conscientiousness": ["responsible", "disciplined", "organized", "dutiful"],
        "extraversion": ["assertive", "outspoken", "energetic", "dominant"],
        "agreeableness": ["self-interested", "mercenary", "ruthless", "competitive"],
        "neuroticism": ["anxious", "worrier", "reactive", "emotional"]
    },

    "ocean_scores": {
        "openness": 2,
        "conscientiousness": 8,
        "extraversion": 7,
        "agreeableness": 3,
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
    from persona_ids import MR_KRABS_PERSONA_ID
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
        persona_id=MR_KRABS_PERSONA_ID,
        persona_name_in_data="Mr. Krabs",
        line_col="line",
        line_raw_col="raw_text",
        speaker_name_col="character",
        is_spoken_line_col="spoken_line",
    )
