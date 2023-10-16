raw_data: dict[str, str] = {
    "identified_character": "Eric Cartman",
    "personality_narrative": "Eric Cartman, a prominent character from South Park, is a character that showcases a complex personality that often oscillates drastically. He displays high levels of openness towards new experiences, mostly if they serve his self-interest. His conscientiousness level is a bit low, with a lack of regard for rules and a twisted sense of responsibility. He is high on the extraversion scale as he is typically very assertive, loves attention, and exhibits dominant behavior. In terms of agreeableness, Cartman is extremely low; he is generally unkind, manipulative, and self-centered. Lastly, his neuroticism is slightly high, as he can be prone to mood swings and resentment.",
    "decision_reasoning": {
        "openness": "Cartman shows an unceasing curiosity and willingness to engage in novel situations, especially when such situations can potentially benefit him. His unconventional ideas and schemes, as well as his readiness to break rules, demonstrate his high openness.",

        "conscientiousness": "Cartman's recklessness and disregard for rules make him score low on conscientiousness. He lacks dependability and a strong work ethic, often seeking the easiest path to his goals, even if it means cheating or manipulating others.",

        "extraversion": "Cartman is continually seeking attention and is quite assertive, even to the point of being aggressive. He loves being in the spotlight and is quite talkative, which leads to his high score in extraversion.",

        "agreeableness": "He is very low on agreeableness. From his actions throughout the South Park series, Cartman exhibits traits of manipulation, unkindness, and a noticeable lack of empathy, often prioritizing his needs over others.",

        "neuroticism": "Cartman's mood swings, exhibited especially when his whims are not gratified, and his resulting resentment, amplify his neuroticism score."
    },
    "keywords": {
        "openness": ["curious", "unconventional", "rule-breaker", "imaginative", "ideas-driven"],
        "conscientiousness": ["reckless", "rule-breaker", "manipulative", "lacks dependability"],
        "extraversion": ["assertive", "attention-seeking", "dominant", "talkative"],
        "agreeableness": ["manipulative", "unkind", "self-centered", "lacks empathy"],
        "neuroticism": ["mood swings", "resentful", "impulsive", "irritable"]
    },
    "ocean_scores": {
        "openness": 8,
        "conscientiousness": 3,
        "extraversion": 9,
        "agreeableness": 1,
        "neuroticism": 7
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
    from persona_ids import ERIC_CARTMAN_PERSONA_ID
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
        persona_id=ERIC_CARTMAN_PERSONA_ID,
        persona_name_in_data="Cartman",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="speaking_line",
    )
