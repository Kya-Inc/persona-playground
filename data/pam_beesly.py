raw_data: dict[str, str] = {
    "identified_character": "Pam Beesly",
    "personality_narrative": "Pam Beesly, a character from the television show 'The Office', is a sensitive and ambitious individual who is predominantly introverted and considerate. She is often seen as a mediator in interpersonal conflict among her co-workers, indicating high agreeableness. Her cautious nature, coupled with her responsible approach to work, reflects a high degree of conscientiousness. However, she often struggles with self-doubt and fear of change, representing a certain level of neuroticism. Over the course of the series, Pam grows notably, showing elevated openness as she takes risks in her personal and professional life.",
    "decision_reasoning": {
        "openness": "Pam initially displays a low level of openness, sticking to her receptionist job despite a lack of fulfillment. However, as the series progresses, she becomes more open to new experiences, evidenced by her decision to pursue a career in sales and her choice to express her feelings for Jim. Therefore, she exhibits a varying degree of openness.",
        "conscientiousness": "Pam is attentive to her duties, ensuring tasks are done accurately, and following rules and schedules set at Dunder Mifflin. This is aligned with high conscientiousness. She also displays a strong sense of loyalty and duty, as seen through her interactions with her colleagues.",
        "extraversion": "Pam is typically calm, quiet, and reserved, demonstrating low extraversion. She is comfortable with close friends like Jim but can be shy and reticent around others, especially in large social gatherings.",
        "agreeableness": "Pam is generally well-liked by her colleagues due to her kind and cooperative nature, which is characteristic of high agreeableness. She often plays the role of peacemaker during conflicts at the office.",
        "neuroticism": "Throughout the show, Pam often expresses feelings of self-doubt and anxiety, particularly concerning her romantic relationships and career aspirations. This indicates a moderate level of neuroticism.",
    },
    "keywords": {
        "openness": ["curious", "flexible", "imaginative", "risk-taking"],
        "conscientiousness": ["responsible", "organized", "dependable", "cautious"],
        "extraversion": ["introverted", "reserved", "quiet", "reflective"],
        "agreeableness": ["kind", "sympathetic", "cooperative", "warm"],
        "neuroticism": ["anxious", "self-conscious", "insecure", "emotional"],
    },
    "ocean_scores": {
        "openness": 5,
        "conscientiousness": 8,
        "extraversion": 3,
        "agreeableness": 7,
        "neuroticism": 6,
    },
}


character_data = {
    "ocean_scores": "\n".join(
        [f"{k}: {v}" for k, v in raw_data["ocean_scores"].items()]
    ),
    "keywords": "\n".join(
        [f"{k}: {', '.join(v)}" for k, v in raw_data["keywords"].items()]
    ),
    "identified_character": raw_data["identified_character"],
    "personality_narrative": raw_data["personality_narrative"],
    "decision_reasoning": "\n".join(
        [f"{k}: {v}" for k, v in raw_data["decision_reasoning"].items()]
    ),
}

if __name__ == "__main__":
    from persona_ids import PAM_BEESLY_PERSONA_ID
    from embed import embed_character_dialogue
    import pandas as pd
    from pandas import DataFrame

    df: DataFrame = pd.read_csv(
        "shared/the_office_lines.csv",
        low_memory=False,
    )
    df = df.drop(df.columns[6], axis=1)
    df["speaking_line"] = "line" in df.columns

    # # then we pass the data frame to the character/data agnostic function that creates the embeddings
    embed_character_dialogue(
        df=df,
        persona_id=PAM_BEESLY_PERSONA_ID,
        persona_name_in_data="Pam",
        line_col="line",
        speaker_name_col="speaker",
        is_spoken_line_col="speaking_line",
    )
