raw_data: dict[str, str] = {
    "identified_character": "Peter Griffin",
    "personality_narrative": "Peter Griffin is an outgoing and impulsive individual with a carefree attitude towards life. He has a high level of extraversion and openness, often expressing his thoughts without reservation, regardless of their potential consequences. He shows a notable lack of conscientiousness, which is evident in his impulsive and often inappropriate behaviors. He is generally agreeable due to his outgoing nature and love for his family, but this trait is occasionally overshadowed by his poor judgment. Peter has a high level of neuroticism, as he can quickly become emotionally upset or excited over minor incidents.",
    "decision_reasoning": {
        "openness": "Peter's willingness to engage with different people and his readiness to express his thoughts, no matter how outrageous, suggest a high level of openness. He is not restrained by convention, which indicates high openness to experience.",
        "conscientiousness": "Peter's impulsiveness, carefree attitude, and often inappropriate actions indicate a low level of conscientiousness. He tends not to think things through or consider the potential negative consequences of his actions.",
        "extraversion": "Peter is highly extroverted. He is outgoing, sociable, and rarely shy in expressing his thoughts or engaging with different people.",
        "agreeableness": "Although Peter is generally agreeable due to his outgoing nature and love for his family, his trait is occasionally overshadowed by his poor judgment, leading to potential disagreements or conflicts.",
        "neuroticism": "Peter's emotional reactivity suggests high neuroticism. He can quickly become upset or excited over minor incidents."
    },
    "keywords": {
        "openness": ["outgoing", "expressive", "unconventional"],
        "conscientiousness": ["impulsive", "carefree", "inconsiderate"],
        "extraversion": ["outgoing", "sociable", "expressive"],
        "agreeableness": ["loving", "outgoing", "conflict-prone"],
        "neuroticism": ["emotionally reactive", "excitable", "easily upset"]
    },
    "ocean_scores": {
        "openness": 7,
        "conscientiousness": 2,
        "extraversion": 9,
        "agreeableness": 5,
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
