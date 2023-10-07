raw_data: dict[str, str] = {
  "identified_character": "Dwight Schrute",
  "personality_narrative": "Dwight Schrute, a character from The Office, is an individual who is highly organized and disciplined, always devoting himself thoroughly to each task and ensuring every job is done at its best, which distinguishes his conscientiousness. This can appear fanatical at times, as Dwight’s pursuit of detail can often proceed to the level of the absurd. Despite being socially awkward at times, he expresses a strong sense of loyalty and dependability towards his superiors and friends. He's less emotionally reactive, as he doesn't disturb easily and usually prefers to suppress his emotions rather than express them, indicating a low degree of neuroticism. Lastly, Dwight's lower score in openness is highlighted by his preference for tradition and lack of interest in exploring new experiences.",
  
  "decision_reasoning": {
    "openness": "Dwight, being quite traditionalist and conventional in his approach, does not exhibit a strong affinity for new experiences or novel ideas. He only seldom proves himself adaptable to unpredictable situations.",
    "conscientiousness": "Dwight's high sense of duty and responsibility, along with meticulous attention to detail, is embedded in his everyday work, perfectly showcasing his high conscientiousness score.",
    "extraversion": "Despite not being the most socially adept character, Dwight exhibits moderate extraversion, expressing strong assertiveness and energy, particularly in his role as Assistant (to the) Regional Manager.",
    "agreeableness": "Although he is generally not the most affable character, Dwight shows deep loyalty and strong protective instincts, underpinning noteworthy elements of agreeableness.",
    "neuroticism": "Dwight seems to handle stress relatively well and doesn't allow his emotions to influence his actions excessively. However, his occasionally explosive temper and deep-rooted fears speak to some degree of neuroticism."
  },
  
  "keywords": {
    "openness": ["traditionalist", "conventional"],
    "conscientiousness": ["diligent", "meticulous", "organized", "responsible"],
    "extraversion": ["assertive", "energetic", "strong-willed"],
    "agreeableness": ["loyal", "steadfast"],
    "neuroticism": ["steady", "unperturbed"]
  },
  
  "ocean_scores": {
    "openness": 2,
    "conscientiousness": 9,
    "extraversion": 5,
    "agreeableness": 4,
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

