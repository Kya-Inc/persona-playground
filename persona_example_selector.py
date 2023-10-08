from typing import Dict, List
from types import SimpleNamespace
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from langchain.prompts.example_selector.base import BaseExampleSelector
import streamlit as st
from pydantic import BaseModel
from icecream import ic

semantic_model = SentenceTransformer("thenlper/gte-large")


class PersonaExampleSelector(BaseExampleSelector, BaseModel):
    """Select examples from persona data"""

    persona_id: str

    def add_example(self, example: Dict[str, str]) -> None:
        """Add an example to the list of examples."""
        pass

    def select_examples(self, input_variables: Dict[str, str]) -> List[dict]:
        """Select which examples to use based on the inputs."""
        examples = []

        qdrant = QdrantClient(
            url=st.secrets.qdrant_url, api_key=st.secrets.qdrant_api_key
        )

        all_responses = []
        prompts = qdrant.search(
            collection_name="prompts",
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="persona_id", match=MatchValue(value=self.persona_id)
                    )
                ]
            ),
            query_vector=semantic_model.encode(
                input_variables.get("human_input")
            ).tolist(),
            limit=10,
            with_payload={"exclude": ["precontext", "postcontext"]},
            score_threshold=0.75,
        )

        for prompt in prompts:
            ic(prompt.payload)

            examples.append(prompt.payload)
            p_payload = SimpleNamespace(**prompt.payload) 

            responses = qdrant.search(
                collection_name="responses",
                query_filter=Filter(
                    must=[
                        FieldCondition(
                            key="persona_id", match=MatchValue(value=self.persona_id)
                        )
                    ]
                ),
                query_vector=semantic_model.encode(p_payload.response).tolist(),
                limit=2,
                with_payload={
                    "exclude": ["precontext", "postcontext", "prompting_character"]
                },
                score_threshold=0.75, # this definitely needs to be higher, just not sure how high yet
            )

       
            for response in responses:
                ic(response.payload) 
                # we only want responses that aren't included,  there will always be at least one exact match.
                if response.payload["response"] != p_payload.response:

                  response.payload["original_response_matched"] = p_payload.response
                  all_responses.append(response)

                  
                  examples.append(response.payload)

        debug_info = create_debug_info(input_variables["human_input"], prompts, all_responses)
        st.session_state.debug_info = debug_info
        return examples
    
def create_debug_info(human_input, prompts, responses):

  output = f"- human input: {human_input.strip()}\n" 
  output += "  examples matching cue:\n"

  for prompt in prompts:
    output += f"  - cue: {prompt.payload['prompt']}\n"
    output += f"    score: {prompt.score}\n"
    output += f"    response: {prompt.payload['response']}\n"
    output += "    similar responses:\n"
    
    for response in responses:
      if response.payload["original_response_matched"] == prompt.payload["response"]:
        output += f"      - response: {response.payload['response']}\n"
        output += f"        score: {response.score}\n"

  return output