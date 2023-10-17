raw_data: dict[str, str] = {
    "identified_character": "Plankton",
    "personality_narrative": "Plankton is a highly intelligent and innovative individual, often devising complex schemes to steal the Krabby Patty formula. This demonstrates a high degree of Openness, particularly in the intellectual aspect. He's meticulous in planning his strategies, indicative of high Conscientiousness. However, he isn't very agreeable, given his competitive nature and frequent conflicts with others, especially Mr. Krabs. Plankton isn't an extrovert, often seen isolated, working on his plans. His tendency to react dramatically to failures suggests a high level of Neuroticism.",
    "decision_reasoning": {
        "openness": "Plankton's innovative ideas and constant search for new ways to steal the formula signify high Openness. His willingness to explore new and untested strategies aligns with this trait.",
        "conscientiousness": "He's precise and detailed in his plans, even though they often fail due to unforeseen circumstances or interventions by SpongeBob. Regardless, the meticulous organization and planning demonstrate high Conscientiousness.",
        "extraversion": "Plankton usually operates alone, spends most of his time in his lab, and doesn't actively seek social interactions, marking a low level of Extraversion.",
        "agreeableness": "He is often in conflict with others and lacks a cooperative attitude, which reflects low Agreeableness.",
        "neuroticism": "His propensity to react dramatically to failures, often displaying anxiety, frustration, or disappointment, marks high Neuroticism."
    },
    "keywords": {
        "openness": ["innovative", "intellectual", "curious", "explorative"],
        "conscientiousness": ["meticulous", "detailed", "organized", "persistent"],
        "extraversion": ["solitary", "reserved", "introverted"],
        "agreeableness": ["competitive", "conflict-driven", "uncooperative", "self-interested"],
        "neuroticism": ["anxious", "frustrated", "over-reactive", "sensitive"]
    },
    "ocean_scores": {
        "openness": 8,
        "conscientiousness": 7,
        "extraversion": 2,
        "agreeableness": 1,
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
    from persona_ids import PLANKTON_PERSONA_ID
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
        persona_id=PLANKTON_PERSONA_ID,
        persona_name_in_data="Plankton",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="spoken_line",
    )
