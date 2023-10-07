
from typing import Dict, List
from types import SimpleNamespace
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from langchain.prompts.example_selector.base import BaseExampleSelector
import streamlit as st
from pydantic import BaseModel

# qdrant = QdrantClient(path="db")
semantic_model = SentenceTransformer('thenlper/gte-large')

class PersonaExampleSelector(BaseExampleSelector, BaseModel):
    """Select examples for Homer Simpson."""
    persona_id: str
    def add_example(self, example: Dict[str, str]) -> None:
        """Add an example to the list of examples."""
        pass

    def select_examples(self, input_variables: Dict[str, str]) -> List[dict]:
        """Select which examples to use based on the inputs."""
        examples = []
         
        qdrant = QdrantClient(url=st.secrets.qdrant_url, api_key=st.secrets.qdrant_api_key)

        prompts  = qdrant.search(
          collection_name="prompts",
          query_filter=Filter(must=[FieldCondition(key="persona_id", match=MatchValue(value=self.persona_id))]),
          query_vector=semantic_model.encode(input_variables.get("human_input")).tolist(),
          limit=10,
          with_payload={"exclude": ["precontext", "postcontext"]},
          score_threshold=0.75
        )

        for prompt in prompts:
          payload = SimpleNamespace(**prompt.payload)

          examples.append(prompt.payload)

          responses = qdrant.search(
            collection_name="responses",
            query_filter=Filter(must=[FieldCondition(key="persona_id", match=MatchValue(value=self.persona_id))]),
            query_vector=semantic_model.encode(payload.response).tolist(),
            limit=3,
            with_payload={"exclude": ["precontext", "postcontext", "prompting_character"]},
            score_threshold=0.75
          )

          for response in responses:
              examples.append(response.payload)
  
        return examples
