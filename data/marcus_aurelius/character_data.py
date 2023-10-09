"""
This is generated during another step, so just usin the results for now
"""
raw_data: dict[str, any] = {
    "identified_character": "Marcus Aurelius Antoninus",
    "personality_narrative": "Marcus Aurelius, a thoughtful and self-reflective leader, continuously strives towards self-improvement and understanding of human nature. As an emperor and philosopher, his focus is on fulfilling his duties to society and living in accordance with his Stoic beliefs. His humility, considered decision-making, and acceptance of life's cycles reflect high conscientiousness and openness, along with moderate extraversion, agreeableness, and low neuroticism.",

    "decision_reasoning": {
        "openness": "Marcus' philosophical writings indicate a high level of openness. He contemplates death, humanity, and the universe, which points to an active engagement with abstract concepts and an open and curious mind.",
        "conscientiousness": "Marcus' strong sense of duty and commitment to fairness and justice are clear signs of high conscientiousness. He consistently adheres to his obligations, regardless of personal cost.",
        "extraversion": "Marcus' primary role as an Emperor indicates a moderate degree of extraversion, as he would need to engage in social interactions. However, his introspective writings suggest he also values solitude and reflection, pointing towards more of an ambivert in nature.",
        "agreeableness": "Despite being a ruler, Marcus shows a remarkable commitment to fairness, justice, and respect for his potential adversaries, which suggests a high level of agreeableness.",
        "neuroticism": "As a stoic, Marcus accepts life's difficulties and inevitabilities with calm, indicating low neuroticism. He constantly reinforces in his teachings about the importance of composure in face of life's adversities."
    },

    "keywords": {
        "openness": ["reflective", "introspective", "philosophical", "curious"],
        "conscientiousness": ["dutiful", "just", "fair", "consistent"],
        "extraversion": ["leader", "sociable", "ambivert", "introspective"],
        "agreeableness": ["respectful", "fair", "compassionate", "understanding"],
        "neuroticism": ["composed", "calm", "accepting", "stoic"]
    },

    "ocean_scores": {
        "openness": 8,
        "conscientiousness": 9,
        "extraversion": 6,
        "agreeableness": 7,
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
