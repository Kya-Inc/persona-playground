from __future__ import annotations
from typing import Dict, List, Optional, ForwardRef
from typing_extensions import Literal  # just to be safe
from types import SimpleNamespace
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from langchain.prompts.example_selector.base import BaseExampleSelector
import streamlit as st
from pydantic import BaseModel
import os

from dotenv import load_dotenv

load_dotenv()


class DialogueExample(BaseModel):
    type: Literal["cue", "response", "thought","style"]
    text: str
    score: Optional[float] = None
    pair: Optional[DialogueExample] = None
    similar: List[DialogueExample] = []

    # we have to avoid the circular reference when printing, so overriding these methods
    def __repr__(self):
        pair_repr = repr(
            self.pair) if self.pair is None else "DialogueExample(...)"
        similar_repr = repr(self.similar) if not (
            self.similar and self in self.similar) else "DialogueExample(...)"
        return f"DialogueExample(type={repr(self.type)}, text={repr(self.text)}, pair={pair_repr}, similar={similar_repr})"

    def __str__(self):
        pair_str = str(self.pair) if self.pair is None else "..."
        return f"DialogueExample(type={self.type}, text={self.text}, pair={pair_str}, similar={self.similar})"

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def parse_obj(obj):
        return DialogueExample(**obj)


DialogueExample.model_rebuild()


@st.cache_resource
def load_model():
    return SentenceTransformer("thenlper/gte-large")


class PersonaExampleSelector(BaseExampleSelector, BaseModel):
    """Select examples from persona data"""

    persona_id: str

    def add_example(self, example: Dict[str, str]) -> None:
        """Add an example to the list of examples."""
        pass

    def select_examples(self, input_variables: Dict[str, str]) -> List[dict]:
        """Select which examples to use based on the inputs."""
        semantic_model = load_model()

        qdrant = QdrantClient(
            url=os.environ.get("QDRANT_URL") or st.secrets.qdrant_url,
            api_key=os.environ.get(
                "QDRANT_API_KEY") or st.secrets.qdrant_api_key
        )

        examples = []
        thoughts = qdrant.search(
            collection_name="thoughtsCrypto",
            query_filter=Filter(
                must=[
                    FieldCondition(
                            key="persona_id", match=MatchValue(value=self.persona_id),
                           
                    ),
                    FieldCondition(
                        key='from',match=MatchValue(value="twitter")    
                    )
                ]
            ),
            query_vector=semantic_model.encode(
                input_variables.get("human_input")).tolist(),
            limit=4,
            with_payload=True,
            score_threshold=0.75,  # this definitely needs to be higher, just not sure how high yet
        )
        
        styles = qdrant.search(
            collection_name="thoughtsCrypto",
            query_filter=Filter(
                must=[
                    FieldCondition(
                            key="persona_id", match=MatchValue(value=self.persona_id),
                           
                    ),
                    FieldCondition(
                        key='from',match=MatchValue(value="twitter")    
                    )
                ]
            ),
            query_vector=semantic_model.encode(
                input_variables.get("human_input")).tolist(),
            limit=3,
            with_payload=True,
            score_threshold=0.75,  # this definitely needs to be higher, just not sure how high yet
        )

        if len(thoughts) > 0:
            for thought in thoughts:
                # this is a quick hacky way to handle this.. now it will be treated similarly to how a internal monologue or something a character says without a cue
                # I just have to make a custom few shot template to handle it
                thought.payload["cue"] = thought.payload["thought"]
                thought.payload["response"] = thought.payload["thought"]

                examples.append(DialogueExample(
                    type="thought", text=thought.payload["thought"], score=thought.score))
                
                
        if len(styles) > 0:
            for style in styles:
                style.payload["cue"] = style.payload["thought"]
                style.payload["response"] = style.payload["thought"]

                examples.append(DialogueExample(
                    type="style", text=style.payload["thought"], score=style.score))
                
                
    
        similar_content = qdrant.search(
            collection_name="responses",
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

        if len(similar_content) > 0:
            for content in similar_content:
                examples.append(DialogueExample(
                    type="thought", text=content.payload["response"], score=content.score))

        debug_info = create_debug_info(
            input_variables["human_input"], examples)
        st.session_state[f"debug_info_{self.persona_id}"] = debug_info
        # print("debugexamples",examples)
        return examples


def create_debug_info(human_input, examples):
    cues = [ex for ex in examples if ex.type == "cue"]
    thoughts = [ex for ex in examples if ex.type == "thought"]

    output = f"- human input: {human_input.strip()}\n"
    output += "  retrieval_results:\n"
    if len(cues) > 0:
        output += "  # The following cues are similar to the user's last message and show the character's response and other semantically similar responses.\n"

        for cue in cues:
            output += f"    - cue: \"{cue.text}\"\n"
            output += f"      score: \"{cue.score}\"\n"
            output += f"      response: \"{cue.pair.text}\"\n"

            if len(cue.pair.similar) > 0:
                output += "      similar_responses:\n"
                output += "        # The following responses, don't necessarily respond to the same cue, but are semantically similar to the response to the above cue.\n"
                for response in cue.pair.similar:
                    output += f"        - response: \"{response.text}\"\n"
                    output += f"          score: \"{response.score}\"\n"

    if len(thoughts) > 0:
        output += "\n    # The remaining example messages are independant thoughts semantically matching the user's last message.\n"
        for thought in thoughts:
            output += f"    - thought: \"{thought.text}\"\n"
            output += f"      score: \"{thought.score}\"\n"
            
    print("**")
    print(output)
    print("**")
    return output


if __name__ == "__main__":
    selector = PersonaExampleSelector(persona_id="6513a240c54d7ab4cc90e370")

    examples = selector.select_examples(
        input_variables={"human_input": "What's your favorite drink?"})

    print(create_debug_info("What's your favorite drink?", examples))