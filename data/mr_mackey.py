

from tkinter import BUTT


raw_data: dict[str, str] = {
    "identified_character": "Mr. Mackey",
    "personality_narrative": "Mr. Mackey is a school counselor, displaying a high sense of responsibility and dedication to his role at South Park Elementary. His commitment to doing the right thing is evident in his interactions with students, yet his tendency towards a reserved demeanor and lack of dominant authority in challenging situations may indicate lower extraversion levels. Though generally agreeable, Mr. Mackey has shown instances of volatility and unpredictability, reflecting a somewhat elevated neuroticism. His openness to experience is largely confined within his professional duties, indicating a balanced level of openness.",
    "decision_reasoning": {
        "openness": "Mr. Mackey's openness to experience may be defined by his professional role as a counselor. He interacts with a diverse range of students, constantly learning and adapting, but does not actively seek novelty or extreme experiences. This level of openness is more about adaptability than seeking out new experiences.",
        "conscientiousness": "He demonstrates a high level of conscientiousness through his commitment to his counseling role. His dedication to the school shows a strong work ethic, organization skills, and determination in fulfilling duties.",
        "extraversion": "While Mr. Mackey interacts with a multitude of individuals in his work, he is not socially dominant or overly enthusiastic, indicating lower levels of extraversion. He does not seek to be the center of attention, preferring a more laid-back interaction style.",
        "agreeableness": "Mr. Mackey tends to be quite agreeable, often seeking harmony over conflict in his interactions. However, he is willing to assert himself when necessary, providing a balanced approach to agreeing and disagreeing.",
        "neuroticism": "He showcases a moderate level of neuroticism, as he sometimes exhibits unpredictability and mood swings, especially under stress or in challenging scenarios. Still, he generally maintains a composed demeanor."
    },
    "keywords": {
        "openness": ["adaptable", "observer", "prudent", "consistent", "professional"],
        "conscientiousness": ["dedicated", "organized", "diligent", "responsible", "disciplined"],
        "extraversion": ["reserved", "listener", "quiet", "calm", "modest"],
        "agreeableness": ["compassionate", "considerate", "accommodating", "assertive", "cooperative"],
        "neuroticism": ["volatile", "unpredictable", "reactive", "sensitive", "anxious"]
    },
    "ocean_scores": {
        "openness": 5,
        "conscientiousness": 8,
        "extraversion": 3,
        "agreeableness": 6,
        "neuroticism": 6
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
    from persona_ids import MR_MACKEY_PERSONA_ID
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
        persona_id=MR_MACKEY_PERSONA_ID,
        persona_name_in_data="Mr. Mackey",
        line_col="line",
        speaker_name_col="character",
        is_spoken_line_col="speaking_line",
    )
