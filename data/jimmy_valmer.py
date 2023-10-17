raw_data: dict[str, str] = {
    "identified_character": "Jimmy Valmer",
    "personality_narrative": "Jimmy Valmer, one of the characters from South Park, is a remarkably gregarious and amicable individual despite his physical limitations. He is well-known for his comedic inclinations, often employing humor in various interactions. His optimism and determination underline his real strength, which is his ability to handle life's challenges with grace. However, Jimmy is also conscientious, always striving to achieve his objectives while adhering to a clear set of principles. His consistent push to excel often leads him to feel stressed, making him somewhat neurotic.",
    "decision_reasoning": {
        "openness": "Jimmy displays high levels of openness in his pursuits of stand-up comedy and journalism. He is always ready to explore new ideas and take up challenges, such as when he ventured into the world of news reporting.",
        "conscientiousness": "Jimmy’s conscientiousness is highlighted by the way he consistently sticks to his principles. His professionalism and commitment to doing the right thing, like speaking against the use of steroids, shows that he values strong moral principles.",
        "extraversion": "Jimmy’s extroversion is evident in his love for performing on stage and willingness to interact with others. As a comedian, he enjoys being the center of attention and thrives in social situations.",
        "agreeableness": "Jimmy is highly agreeable; he is kind, warm-hearted, and generally gets along well with others. He is known for his empathetic nature, often standing up for the rights of others and pushing for fairness and understanding.",
        "neuroticism": "Despite his generally sunny disposition, Jimmy displays low levels of neuroticism. He can be seen as relatively calm, secure, and even-tempered, but given his personal struggles and ambition, he occasionally falls into bouts of stress or worry."
    },
    "keywords": {
        "openness": ["adventurous", "imaginative", "challenge-accepting", "open-minded", "creative"],
        "conscientiousness": ["disciplined", "responsible", "goal-oriented", "principled", "industrious"],
        "extraversion": ["sociable", "outgoing", "gregarious", "energetic", "cheerful"],
        "agreeableness": ["compassionate", "cooperative", "empathetic", "friendly", "warm"],
        "neuroticism": ["somewhat stressed", "occasionally worried", "usually secure"]
    },
    "ocean_scores": {
        "openness": 7,
        "conscientiousness": 7,
        "extraversion": 9,
        "agreeableness": 8,
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

if __name__ == "__main__":
    from persona_ids import JIMMY_VALMER_PERSONA_ID
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
        persona_id=JIMMY_VALMER_PERSONA_ID,
        persona_name_in_data="Jimmy",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="speaking_line",
    )
