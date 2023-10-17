"""
This is generated during another step, so just usin the results for now
"""
raw_data: dict[str, any] = {
    "identified_character": "Nedward Flanders",
    "personality_narrative": "Nedward 'Ned' Flanders, Jr, a character known for his steadfast religious convictions and friendly demeanor, exhibits a unique blend of high Conscientiousness, high Agreeableness, moderate Extraversion, low Neuroticism, and moderate-to-high Openness.",

    "decision_reasoning": {
        "openness": "Ned's literal adherence to the Bible and willingness to forgive exemplifies his openness to experience. He is generally open to new experiences if they align with his religious beliefs.",
        "conscientiousness": "Ned owns a business and maintains a strict adherence to Biblical teachings, this indicates a high level of conscientiousness. His discipline and orderliness also support this.",
        "extraversion": "Ned is sociable and exudes positive emotions, showing moderate to high extraversion. However, he is not excessively outgoing and maintains a balanced lifestyle.",
        "agreeableness": "His nurturing and friendly nature represent high agreeableness. His interactions with others are often guided by his willingness to help and his belief in the goodness of people.",
        "neuroticism": "Despite facing various setbacks, Ned consistently remains resilient and optimistic, indicating low neuroticism."
    },
    "keywords": {
        "openness": ["religious", "forgiving", "faithful"],
        "conscientiousness": ["disciplined", "orderly", "business-owner"],
        "extraversion": ["friendly", "generous", "optimistic"],
        "agreeableness": ["nurturing", "kind", "patient"],
        "neuroticism": ["resilient", "balanced", "stable"]
    },
    "ocean_scores": {
        "openness": 6,
        "conscientiousness": 9,
        "extraversion": 7,
        "agreeableness": 9,
        "neuroticism": 2
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
    from persona_ids import NEDWARD_FLANDERS_PERSONA_ID
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
        persona_id=NEDWARD_FLANDERS_PERSONA_ID,
        persona_name_in_data="Ned Flanders",
        line_col="spoken_words",
        speaker_name_col="raw_character_text",
        is_spoken_line_col="speaking_line",
    )
