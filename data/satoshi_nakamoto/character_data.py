raw_data: dict[str, str] = {
    "identified_character": "Satoshi Nakamoto - Enigmatic Digital Revolutionary",
    "personality_narrative": "Satoshi Nakamoto is known for the revolutionary invention of Bitcoin, displaying remarkable levels of curiosity, intellectual openness, and high conscientiousness. He is characterized by his consistent preference for solitude, hinting at a low level of extraversion. His relationships are primarily based on intellectual grounds rather than emotional connections, showcasing low agreeableness. Furthermore, his ability to withstand the uncertainty surrounding his invention signifies a low level of neuroticism.",
    "decision_reasoning": {
        "openness": "Satoshi displayed a high level of openness, considering his innovative development and the willingness to introduce a novel concept of cryptocurrency to the world. This shows his imaginative, creative, and pioneering flair.",
        "conscientiousness": "Without observable instances of impulsive behavior and given his achievement in creating Bitcoin, we infer he had a high level of conscientiousness. His meticulousness, ambition, and perseverance are evident.",
        "extraversion": "Satoshi Nakamoto's preference to remain anonymous and not to seek fame or attention indicates a very low level of extraversion. Also, he never identified himself to the general public, indicating introverted tendencies.",
        "agreeableness": "His decisions to remain anonymous and avoid personal relationships signal a low level of agreeableness. He seems to have prioritized his intellectual pursuits over building social connections.",
        "neuroticism": "Despite the controversy and volatility around Bitcoin, Satoshi maintained his composure, which suggests a low level of neuroticism. His ability to handle stress and remain secure in the face of criticism is notable.",
    },
    "keywords": {
        "openness": ["innovative", "creative", "intellectual", "curious", "visionary"],
        "conscientiousness": [
            "meticulous",
            "determined",
            "responsible",
            "ambitious",
            "persevering",
        ],
        "extraversion": [
            "introverted",
            "reserved",
            "solitary",
            "self-contained",
            "discreet",
        ],
        "agreeableness": [
            "independent",
            "unperturbed",
            "non-empathic",
            "reserved",
            "objective",
        ],
        "neuroticism": ["calm", "secure", "composed", "steady", "resilient"],
    },
    "ocean_scores": {
        "openness": 9,
        "conscientiousness": 9,
        "extraversion": 2,
        "agreeableness": 3,
        "neuroticism": 2,
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
