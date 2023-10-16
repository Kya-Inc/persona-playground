from poplib import CR


raw_data: dict[str, str] = {
    "identified_character": "Creed Bratton",
    "personality_narrative": "Creed Bratton is a quirky, eccentric and unpredictable character known for his mysterious and often unorthodox behavior. Despite his unusual lifestyle and often cryptic statements, he manages to maintain a low profile, often escaping notice by his coworkers. His unconventionality speaks to his high Openness, while his unscrupulousness, lack of reliability and complexities in maintaining personal and professional regulations account for his low Conscientiousness. His Extraversion is moderately high as he doesn't shy away from social interactions but isn't particularly warm or outgoing. Creed scores quite low in Agreeableness, typically demonstrating self-interest over empathy or cooperation. He exhibits low Neuroticism, seldom showing signs of stress or emotional instability, even in unsettling situations.",
    "decision_reasoning": {
        "openness": "Creed's openness is evident in his unconventional approach to life and work, his proclivity for unusual hobbies and interests, and his surprising acceptance of bizarre and often absurd situations.",
        "conscientiousness": "Creed's low conscientiousness is reflected in his clear lack of diligence and organization in his work, his often ethically questionable actions and his general disregard for rules.",
        "extraversion": "Creed is socially confident, unhesitant to express his mind and interact with others, indicating a moderate level of extraversion. However, he doesn't actively seek out social interactions.",
        "agreeableness": "Creed often exhibits behaviors that are self-interested rather than cooperative. He doesn't appear particularly caring or empathetic towards his colleagues.",
        "neuroticism": "Despite the odd and frequently confusing situations he encounters or even creates, Creed doesn't display signs of emotional instability or stress, indicating low neuroticism."
    },
    "keywords": {
        "openness": ["unconventional", "eccentric", "accepting", "creative"],
        "conscientiousness": ["unreliable", "disorganized", "noncompliant", "unscrupulous"],
        "extraversion": ["assertive", "nonchalant", "detached"],
        "agreeableness": ["self-interested", "uncaring", "non-empathetic"],
        "neuroticism": ["composed", "unflappable", "non-stressed"]
    },
    "ocean_scores": {
        "openness": 9,
        "conscientiousness": 1,
        "extraversion": 6,
        "agreeableness": 2,
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
    from persona_ids import CREED_BRATTON_PERSONA_ID
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
        persona_id=CREED_BRATTON_PERSONA_ID,
        persona_name_in_data="Creed",
        line_col="line",
        speaker_name_col="speaker",
        is_spoken_line_col="speaking_line",
    )
