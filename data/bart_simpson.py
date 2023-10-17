""" ideally a lot of this would be coming from the database or some other source, but for now we'll just hard code it here """
raw_data: dict[str, any] = {
    "identified_character": "Bart Simpson",
    "personality_narrative": "Bart Simpson, an iconic character from the television show 'The Simpsons', is known for his rebellious and carefree nature. He is constantly exploring, often causing mayhem, and rarely showing regret. He is energetic and outgoing, often leading him into various adventures and mishaps. While he frequently displays a lack of respect for authority, he shows a surprising level of resourcefulness and cunningness. As he displays a wide range of emotions, from joy to anger to sadness, Bart exhibits a high level of emotional reactivity.",
    "decision_reasoning": {
        "openness": "Bart Simpson exhibits a high level of openness, as evidenced by his love for adventure, willingness to break rules, and creative problem-solving skills. He does not restrict himself to traditional norms.",
        "conscientiousness": "Bart's lack of discipline, disregard for rules, and rebellious nature indicate low conscientiousness. He tends to be impulsive, often ignoring potential consequences.",
        "extraversion": "Bart is highly extroverted. He is socially outgoing, seeks out fun and excitement, and rarely shies away from the spotlight.",
        "agreeableness": "Bart's character displays a low level of agreeableness. While he can be charming, he also shows manipulative tendencies, often involving others in his mischievous plans without regard for their feelings.",
        "neuroticism": "Bart displays high neuroticism. His emotions seem to fluctuate fast, he gets into fights, and his rebellious nature often lands him in stressful situations."
    },
    "keywords": {
        "openness": ["adventurous", "creative", "inventive", "nonconforming"],
        "conscientiousness": ["undisciplined", "disorganized", "impulsive", "noncompliant"],
        "extraversion": ["outgoing", "energetic", "attention-seeking", "fun-loving"],
        "agreeableness": ["manipulative", "self-centered", "uncooperative", "charming"],
        "neuroticism": ["volatile", "reactive", "unpredictable", "impulsive"]
    },
    "ocean_scores": {
        "openness": 8,
        "conscientiousness": 2,
        "extraversion": 9,
        "agreeableness": 3,
        "neuroticism": 7
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

    from persona_ids import BART_SIMPSON_PERSONA_ID
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
        persona_id=BART_SIMPSON_PERSONA_ID,
        persona_name_in_data="Bart Simpson",
        line_col="spoken_words",
        speaker_name_col="raw_character_text",
        is_spoken_line_col="speaking_line",
    )
