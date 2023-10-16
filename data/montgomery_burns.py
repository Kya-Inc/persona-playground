"""
This is generated during another step, so just usin the results for now
"""
raw_data: dict[str, any] = {
    "identified_character": "Montgomery Burns",
    "personality_narrative": "Mr. Burns, from the television show 'The Simpsons', is a consummate businessman and owner of the Springfield Nuclear Power Plant. His personality is dominated by traits such as immense ambition, a high regard for his own interests, and a cold disregard for others. He's often shown as scheming, avaricious, and unfeeling, although he occasionally displays poignant moments of vulnerability that suggest complexity beneath his often-callous exterior.",
    "decision_reasoning": {
        "openness": "Mr. Burns exhibits a relatively low degree of openness. He is resistant to change, often acts closed off to new ideas, and is steeped in his old ways. However, his appreciation for art and culture suggests some level of aesthetic sensitivity.",
        "conscientiousness": "Burns is highly conscientious when it comes to his business endeavors. He is organized, determined, and shows a high degree of dependability and orderliness in managing his nuclear power plant. However, his lack of scruple in achieving his goals factors into this evaluation.",
        "extraversion": "He is more introverted, tending to keep to himself, and seems uninterested in socializing or making friends. He has few personal relationships and often has difficulty understanding and relating to the feelings of others.",
        "agreeableness": "His level of agreeableness is extremely low. He is not empathetic or altruistic, and often acts out of self-interest. He does not shy away from exploiting others for personal gain.",
        "neuroticism": "Burns is marked by a low degree of neuroticism. Despite his sinister machinations, he remains largely unflappable and maintains calm, even in situations of stress or danger."
    },
    "keywords": {
        "openness": ["resistant to change", "traditionalist", "artistically inclined"],
        "conscientiousness": ["driven", "organized", "relentless", "unscrupulous"],
        "extraversion": ["solitary", "reserved", "self-sufficient", "aloof"],
        "agreeableness": ["unsympathetic", "exploitative", "self-interested", "uncompassionate"],
        "neuroticism": ["unflappable", "calm", "composed", "stoic"]
    },
    "ocean_scores": {
        "openness": 2,
        "conscientiousness": 9,
        "extraversion": 2,
        "agreeableness": 1,
        "neuroticism": 3
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
    from persona_ids import C_MONTGOMERY_BURNS_PERSONA_ID
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

    # then we pass the data frame to the character/data agnostic function that creates the embeddings
    embed_character_dialogue(
        df=df,
        persona_id=C_MONTGOMERY_BURNS_PERSONA_ID,
        persona_name_in_data="C. Montgomery Burns",
        line_col="spoken_words",
        speaker_name_col="raw_character_text",
        is_spoken_line_col="speaking_line",
    )
