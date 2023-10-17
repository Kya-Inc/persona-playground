"""
This is generated during another step, so just usin the results for now
"""
raw_data: dict[str, any] = {
    "identified_character": "Krusty The Clown",
    "personality_narrative": "Krusty The Clown, a popular television figure in the town of Springfield, presents a unique personality that is a blend of various contrasting traits. At times, he displays an incredibly high level of extraversion but often this seems to be a front to mask significant neuroticism. His career demands a high level of openness, but he is not particularly conscientious, often engaging in reckless behavior. Although he can be gruff and self-centered, he has shown moments of agreeability.",
    "decision_reasoning": {
        "openness": "Krusty is quite open to new experiences. Being a television clown, he is creative and flexible in his performances. Krusty's many career ventures, often on a whim, also demonstrate a high level of openness. However, his openness appears to be more professional than personal - he seems less open to changing personal habits and behaviors.",
        "conscientiousness": "Despite his success, Krusty often shows low conscientiousness. He frequently engages in reckless and impulsive behavior, often neglecting responsibilities. His disorganized lifestyle and lack of discipline when it comes to his health and finances indicate a lower level of conscientiousness.",
        "extraversion": "Krusty's job heavily involves interaction and performance which suggest high extraversion. However, he is frequently shown to be quite lonely and detached in his personal life, indicating his extraversion might be more of a professional necessity than a natural disposition.",
        "agreeableness": "Krusty can be quite cynical, brash, and manipulative, suggesting low agreeableness. However, he often shows a soft spot for children, especially Bart Simpson, indicating some level of agreeability.",
        "neuroticism": "He exhibits high neuroticism. He is frequently depressed, anxious, and insecure, despite his public image of being a cheerful clown. He also seems to react poorly to stress, making impulsive decisions rather than carefully considering the possible outcomes."
    },
    "keywords": {
        "openness": ["creative", "flexible", "impulsive"],
        "conscientiousness": ["reckless", "irresponsible", "disorganized"],
        "extraversion": ["performative", "lonely", "detached"],
        "agreeableness": ["cynical", "brash", "soft-hearted"],
        "neuroticism": ["anxious", "insecure", "impulsive"]
    },
    "ocean_scores": {
        "openness": 7,
        "conscientiousness": 2,
        "extraversion": 7,
        "agreeableness": 3,
        "neuroticism": 8
    }
}

character_data = {
    "identified_character": raw_data["identified_character"],
    "personality_narrative": raw_data["personality_narrative"],
    "decision_reasoning": "\n".join([f"{k}: {v}" for k, v in raw_data["decision_reasoning"].items()]),
    "keywords": "\n".join([f"{k}: {', '.join(v)}" for k, v in raw_data["keywords"].items()]),
    "ocean_scores": "\n".join([f"{k}: {v}" for k, v in raw_data["ocean_scores"].items()])
}

if __name__ == "__main__":
    # make sure the root directory is in your python path
    from persona_ids import KRUSTY_THE_CLOWN_PERSONA_ID
    from embed import embed_character_dialogue
    import pandas as pd
    from pandas import DataFrame

    # prepare dataframe for the specific character by loading from source, handling dtypes if needed, sorting, whatever else might be needed
    dtypes = {
        "speaking_line": "boolean",
    }

    df: DataFrame = pd.read_csv(
        "shared/the_simpsons_lines.csv",
        low_memory=False,
        dtype=dtypes,
        index_col="id",
    ).sort_index().reset_index()

    df.fillna({
        'location_id': 0,
        'raw_location_text': 'Not Specified'
    }, inplace=True)

    # then we pass the data frame to the character/data agnostic function that creates the embeddings
    embed_character_dialogue(
        df=df,
        persona_id=KRUSTY_THE_CLOWN_PERSONA_ID,
        persona_name_in_data="Krusty the Clown",
        line_col="spoken_words",
        speaker_name_col="raw_character_text",
        is_spoken_line_col="speaking_line",
        dry_run=True
    )
