raw_data: dict[str, str] = {
    "identified_character": "Butters Stotch",
    "personality_narrative": "Butters is an innocent and naive character, often exploited by his friends due to his trustworthy nature. His personality is a mix of extreme levels of agreeableness, conscientiousness, and openness, along with minimal extraversion and neuroticism levels. His naivety, optimism, and imaginative nature characterizes his high openness, while his meticulousness, dependability, and rule-abiding behavior highlights his conscientiousness. His willingness to help his friends despite their frequent manipulation portrays his extreme agreeableness. Butters' low levels of extraversion emerge from his tendency to be in the background, coupled with his reserved and timid nature. Lastly, his low neuroticism is signified by his ability to remain cheerful and optimistic, regardless of the circumstances.",
    "decision_reasoning": {
        "openness": "Butters' innocence results in him being highly open-minded and imaginative, lacking skepticism even when it would be warranted. This makes him extremely gullible and susceptible to manipulation, highlighting his high openness.",
        "conscientiousness": "In spite of the frequent manipulation and harsh treatment he experiences from his friends, Butters is a dutiful and rule-abiding character, often working diligently in the background to assist in tasks or schemes. He prefers structure and organized environments, demonstrating his high conscientiousness.",
        "extraversion": "Although he is friendly and amicable, Butters is frequently overshadowed by more forceful personalities, resulting in his lower level of extraversion. He does not thrive in the center of attention and often becomes extremely uneasy when he's put on the spot.",
        "agreeableness": "Butters is very compliant, non-confrontational, and willing to assist, even when taken advantage of. He shows an extreme level of altruism and willingness to believe in the good in people, demonstrating his very high agreeableness.",
        "neuroticism": "Despite enduring various unfortunate events, Butters exhibits a remarkable level of emotional stability. He consistently displays an upbeat and cheerful disposition, underscoring his low neuroticism."
    },
    "keywords": {
        "openness": ["naive", "trustworthy", "imaginative", "open-minded", "gullible"],
        "conscientiousness": ["dutiful", "rule-abiding", "organized", "dependable", "meticulous"],
        "extraversion": ["reserved", "timid", "friendly", "amiable", "subdued"],
        "agreeableness": ["compliant", "non-confrontational", "altruistic", "helpful"],
        "neuroticism": ["emotionally stable", "cheerful", "optimistic", "resilient"]
    },
    "ocean_scores": {
        "openness": 8,
        "conscientiousness": 8,
        "extraversion": 3,
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
    from persona_ids import BUTTERS_STOTCH_PERSONA_ID
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
        persona_id=BUTTERS_STOTCH_PERSONA_ID,
        persona_name_in_data="Butters",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="speaking_line",
    )
