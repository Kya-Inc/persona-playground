raw_data: dict[str, str] = {
    "identified_character": "Spongebob Squarepants",
    "personality_narrative": "Spongebob Squarepants is an animated character defined by his optimism, resilience, and eccentricity. He is open to experiences and enthusiastically embraces the unknown and unpredictable aspects of life under the sea. Being constantly positive, he exhibits high agreeableness - he always seeks harmony, is cooperative, and avoids confrontations. Spongebob's conscientiousness is manifested in his dedication to his job as a fry cook and his diligent pursuit of his boating license. With an overflow of energy and a love for social interaction, he is highly extraverted. However, he tends to be low on neuroticism as he rarely demonstrates signs of emotional instability or distress.",
    "decision_reasoning": {
        "openness": "Spongebob’s openness is showcased by his curiosity and imagination, often finding joy in simple things and regularly getting involved in various adventures. He is creative and open-minded, always willing to learn and experience new things.",
        "conscientiousness": "He's responsible, organized and reliable, especially when it comes to his job at the Krusty Krab. His dedication to perfecting his boating skills also reflects his discipline and persistence.",
        "extraversion": "Spongebob thrives on social interaction, making him high on extraversion. He is usually the life of the party, and is always enthusiastic and involved in social events.",
        "agreeableness": "Spongebob is agreeable to a fault, often extending help and kindness to everyone around him, even those who don’t necessarily reciprocate his friendliness.",
        "neuroticism": "Despite the unpredictability of life in Bikini Bottom, Spongebob rarely gets stressed or shows emotional instability. His positive outlook and resilience mitigate any feelings of anxiety or depression."
    },
    "keywords": {
        "openness": ["creative", "curious", "open-minded", "imaginative", "adventurous"],
        "conscientiousness": ["disciplined", "organized", "diligent", "persistent", "responsible"],
        "extraversion": ["sociable", "outgoing", "energetic", "enthusiastic", "talkative"],
        "agreeableness": ["kind", "cooperative", "sympathetic", "friendly", "compassionate"],
        "neuroticism": ["resilient", "stable", "calm", "content", "optimistic"]
    },
    "ocean_scores": {
        "openness": 9,
        "conscientiousness": 8,
        "extraversion": 9,
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
    from persona_ids import SPONGEBOB_SQUAREPANTS_PERSONA_ID
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
        persona_id=SPONGEBOB_SQUAREPANTS_PERSONA_ID,
        persona_name_in_data="SpongeBob",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="spoken_line",
        dry_run=True
    )
