raw_data: dict[str, str] = {
  "identified_character": "Patrick Bateman",
  "personality_narrative": "Patrick Bateman is a complex character who embodies extreme psychological paradoxes. While being highly conscientious and methodical in his routines, he demonstrates sadistic tendencies and shows a deep-seated struggle with his identity. He craves acceptance and recognition, yet he is controlled by his violent urges. Patrick's excessive attention to detail, superficial charm, and his ability to disassociate from his violent acts create a haunting portrayal of a character plagued by an almost overwhelming sense of neuroticism.",
  "decision_reasoning": {
    "openness": "Patrick Bateman displays traditional interests and predictable behaviors, particularly in his strict routine and love for consumer culture. He lacks deep emotional receptivity or imagination, often choosing to emulate what he perceives is admired by his society. His actions suggest a low level of openness.",
    "conscientiousness": "Bateman is an overachiever, meticulously maintaining a guise of the typical Wall Street elite. His carefully cultivated physical appearance and rigid routines demonstrate high conscientiousness. However, he is an organized individual led not by morals, but by his detached and ruthless persona.",
    "extraversion": "As he thrives off social status and recognition, Patrick Bateman can be seen as extroverted. He enjoys social interactions, however, it is more for validation and acknowledgment than for forming meaningful relationships.",
    "agreeableness": "Bateman's agreeableness could be characterized as low. He manages to maintain a veneer of charm and politeness, but underneath this surface, he plays out violent fantasies and shows little empathy for others' feelings or needs.",
    "neuroticism": "Despite his cold and calm surface, Patrick Bateman portrays high neuroticism. He is plagued with anxiety, violent impulses, and an unstable sense of self, symptoms that often manifest in his hallucinations and the regular crisis of his identity."
  },
  "keywords": {
    "openness": ["unimaginative", "traditional", "predictable"],
    "conscientiousness": ["meticulous", "organized", "persistent"],
    "extraversion": ["attention-seeking", "charismatic", "social"],
    "agreeableness": ["manipulative", "uncaring", "insensitive"],
    "neuroticism": ["anxious", "impulsive", "unstable"]
  },
  "ocean_scores": {
    "openness": 2,
    "conscientiousness": 8,
    "extraversion": 7,
    "agreeableness": 2,
    "neuroticism": 9
  }
}

character_data = {
  "ocean_scores": "\n".join([f"{k}: {v}" for k, v in raw_data["ocean_scores"].items()]),
  "keywords": "\n".join([f"{k}: {', '.join(v)}" for k, v in raw_data["keywords"].items()]),
  "identified_character": raw_data["identified_character"],
  "personality_narrative": raw_data["personality_narrative"],
  "decision_reasoning": "\n".join([f"{k}: {v}" for k, v in raw_data["decision_reasoning"].items()])
}

