raw_data: dict[str, any] = {
    "identified_character": "Brian Armstrong",
    "personality_narrative": "Brian Armstrong, as the co-founder and CEO of Coinbase, exemplifies a unique blend of visionary thinking and pragmatic execution. His journey from a software engineer to a leader in the cryptocurrency space reflects a high degree of openness to new experiences and ideas, particularly those challenging traditional financial paradigms. His ability to foresee and navigate the complexities of the cryptocurrency market indicates a strong sense of conscientiousness, marked by organization, dependability, and a forward-thinking mindset. Armstrong's public presence and effective leadership hint at a level of extraversion, though balanced with the introspective qualities typical of a programmer. His advocacy for financial inclusivity shows a degree of agreeableness, emphasizing compassion and cooperation. There is little public evidence of high neuroticism; instead, Armstrong's calculated risk-taking and composed response to volatile markets suggest emotional stability.",
    "decision_reasoning": {
    "openness": "Armstrong's embrace of cryptocurrency and his role in pioneering a new financial system signify a high degree of openness. His background in software engineering and transition into a dynamic field like cryptocurrency also reflect intellectual curiosity and creativity.",
    "conscientiousness": "Leading a major company like Coinbase requires a high level of conscientiousness. Armstrong's success in this volatile industry demonstrates strong goal-directed behavior, organization, and a capacity for long-term planning.",
    "extraversion": "As a CEO and public figure, Armstrong exhibits qualities of extraversion through his engagement with the community, public speaking, and leadership roles. However, his background in programming and tendency for measured, analytical communication imply a moderated extraversion score.",
    "agreeableness": "His advocacy for financial inclusivity and collaborative approach in the crypto space suggest agreeableness. This is balanced, however, by the competitive nature of the tech industry, which may necessitate a more pragmatic than purely cooperative approach.",
    "neuroticism": "Armstrong's steady leadership in the face of crypto market fluctuations and the pressures of running a high-profile company indicate low neuroticism, marked by emotional stability and resilience under stress."
    },
    "keywords": {
    "openness": ["innovative", "curious", "adaptive", "visionary", "intellectual"],
    "conscientiousness": ["organized", "reliable", "forward-thinking", "goal-oriented", "disciplined"],
    "extraversion": ["outspoken", "engaging", "leadership", "public-speaking", "measured"],
    "agreeableness": ["compassionate", "collaborative", "empathetic", "pragmatic", "cooperative"],
    "neuroticism": ["composed", "resilient", "steady", "calm", "rational"]
    },
    "ocean_scores": {
    "openness": 8,
    "conscientiousness": 8,
    "extraversion": 6,
    "agreeableness": 5,
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



print(character_data)


if __name__ == "__main__":
    from persona_ids import BUTTERS_STOTCH_PERSONA_ID
    from embed import embed_character_dialogue
    import pandas as pd
    from pandas import DataFrame

   