from typing import Dict, List
from types import SimpleNamespace
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from langchain.prompts.example_selector.base import BaseExampleSelector
import streamlit as st
from pydantic import BaseModel
from sympy import DeferredVector

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
        deferred = []
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

            if prompt.payload["prompt"] == prompt.payload["response"]:
                deferred.append(prompt)
            else:
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
                    query_vector=semantic_model.encode(
                        p_payload.response).tolist(),
                    limit=2,
                    with_payload={
                        "exclude": ["precontext", "postcontext", "prompting_character"]
                    },
                    score_threshold=0.75,  # this definitely needs to be higher, just not sure how high yet
                )

                for response in responses:
                    # we only want responses that aren't included,  there will always be at least one exact match.
                    if response.payload["response"] != p_payload.response:

                        response.payload["original_response_matched"] = p_payload.response
                        all_responses.append(response)
                        examples.append(response.payload)

        toughts = qdrant.search(
            collection_name="thoughts",
            query_filter=Filter(
                must=[
                    FieldCondition(
                            key="persona_id", match=MatchValue(value=self.persona_id)
                    )
                ]
            ),
            query_vector=semantic_model.encode(
                input_variables.get("human_input")).tolist(),
            limit=5,
            with_payload=True,
            score_threshold=0.75,  # this definitely needs to be higher, just not sure how high yet
        )

        # now let's move internal dialogue, monologues, etc to the end
        for solo in deferred:
            examples.append(solo.payload)

        # followed by actual chunks from the passages collection
        if len(toughts) > 0:
            for thought in thoughts:
                # this is a quick hacky way to handle this.. now it will be treated similarly to how a internal monologue or something a character says without a cue
                # I just have to make a custom few shot template to handle it
                thought.payload["prompt"] = thought.payload["thought"]
                thought.payload["response"] = thought.payload["thought"]
                examples.append(thought.payload)

        # combine them so we have info about both in the debug_info
        combined = [*deferred, *passages]

        debug_info = create_debug_info(
            input_variables["human_input"], prompts, all_responses, combined)
        st.session_state[f"debug_info_{self.persona_id}"] = debug_info
        return examples


def create_debug_info(human_input, prompts, responses, solos):

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

    output += "  passages matching cue:\n"
    for solo in solos:
        output += f"  - passage: {solo.payload['response']}"
        output += f"    score: {solo.score}\n"

    return output
