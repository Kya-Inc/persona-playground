raw_data: dict[str, str] = {
    "identified_character": "Sandy Cheeks",
    "personality_narrative": "Sandy Cheeks is an animated cartoon character from the television series 'SpongeBob SquarePants'. She is an adventurous and intelligent squirrel from Texas who lives under the sea in a glass dome. Sandy is known for her love for science, karate, and extreme sports. Her Southern American roots instill in her a sense of independence and a can-do attitude. She consistently demonstrates high levels of discipline, commitment to her goals as well as kindness and concern for her sea friends.",
    "decision_reasoning": {
        "openness": "Sandy Cheeks exhibits high openness. This is seen in her consistent eagerness to explore new territories and her love for knowledge and learning. She doesn't feel confined to traditional squirrel activities and openly engages in underwater life and constructs complex scientific equipment.",
        "conscientiousness": "Sandy is highly conscientious; it's exhibited in her discipline, structured way of life, and goal orientation. She maintains her treedome habitat, keeps up with her scientific research and shows a high consistent level of diligence and responsibility.",
        "extraversion": "Extraversion is significant in Sandy’s personality. She enjoys adventures, extreme sports and is generally enthusiastic and energetic. However, she also balances this with time spent alone working on her scientific projects, indicating that while she's sociable, she also values her solitude.",
        "agreeableness": "Sandy Cheeks is generally agreeable, although her high levels of assertiveness might sometimes come across as aggressive. She is usually kind, helpful, and willing to cooperate with her friends in Bikini Bottom.",
        "neuroticism": "Sandy shows relatively low levels of neuroticism. She usually maintains composure in stressful or threatening situations, often becoming the 'problem-solver' among her friends."
    },
    "keywords": {
        "openness": ["creative", "curious", "adventurous", "knowledge-loving", "inventive"],
        "conscientiousness": ["disciplined", "goal-oriented", "structured", "responsible", "diligent"],
        "extraversion": ["sociable", "enthusiastic", "energetic", "outgoing"],
        "agreeableness": ["kind", "helpful", "cooperative", "assertive"],
        "neuroticism": ["composed", "calm", "reflective", "problem-solver"]
    },
    "ocean_scores": {
        "openness": 8,
        "conscientiousness": 9,
        "extraversion": 7,
        "agreeableness": 6,
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
    from persona_ids import SANDY_CHEEKS_PERSONA_ID
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
        persona_id=SANDY_CHEEKS_PERSONA_ID,
        persona_name_in_data="Sandy",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="spoken_line",
    )
