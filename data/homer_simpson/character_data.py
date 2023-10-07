"""
This is generated during another step, so just usin the results for now
"""
raw_data: dict[str, any] = {
  "identified_character": "Homer Simpson",
  "personality_narrative": "Homer Simpson, the iconic character from the animated sitcom 'The Simpsons', is a complex individual with a unique blend of personality traits. He is known for his love of food, particularly donuts and beer, and his often lazy and careless attitude. Despite his flaws, Homer is also shown to be a loving father and husband, demonstrating a deep, albeit often misguided, care for his family. His personality is characterized by low conscientiousness, high extraversion, moderate agreeableness, high neuroticism, and low openness.",
  "decision_reasoning": {
    "openness": "Homer Simpson is not particularly open to new experiences. He tends to stick to his routines and is often resistant to change. This is evident in his long-standing job at the power plant and his predictable daily routines.",
    "conscientiousness": "Homer's level of conscientiousness is quite low. He is often seen neglecting his duties at work and at home, and he tends to make decisions without considering the consequences. His impulsivity and lack of organization are key indicators of this trait.",
    "extraversion": "Homer is quite extraverted. He enjoys socializing, particularly at Moe's Tavern, and he often seeks out the company of others. He is also quite talkative and assertive, further demonstrating his high level of extraversion.",
    "agreeableness": "Homer's level of agreeableness is moderate. While he can be selfish and insensitive at times, he also shows a deep care for his family and friends. He is often willing to go to great lengths to help those he cares about, indicating a certain level of agreeableness.",
    "neuroticism": "Homer exhibits a high level of neuroticism. He is often seen reacting impulsively and emotionally to situations, and he tends to experience a wide range of negative emotions, including anger, anxiety, and frustration."
  },
  "keywords": {
    "openness": ["resistant to change", "routine-oriented", "unadventurous"],
    "conscientiousness": ["impulsive", "disorganized", "neglectful"],
    "extraversion": ["social", "talkative", "assertive"],
    "agreeableness": ["caring", "helpful", "insensitive at times"],
    "neuroticism": ["impulsive", "emotional", "anxious"]
  },
  "ocean_scores": {
    "openness": 2,
    "conscientiousness": 2,
    "extraversion": 8,
    "agreeableness": 5,
    "neuroticism": 8
  }
}


character_data = {
  "identified_character": raw_data["identified_character"],
  "personality_narrative": raw_data["personality_narrative"],
  "decision_reasoning": "\n".join([f"{k}: {v}" for k, v in raw_data["decision_reasoning"].items()]),
  "keywords": "\n".join([f"{k}: {', '.join(v)}" for k, v in raw_data["keywords"].items()]),
  "ocean_scores": "\n".join([f"{k}: {v}" for k, v in raw_data["ocean_scores"].items()])
}

