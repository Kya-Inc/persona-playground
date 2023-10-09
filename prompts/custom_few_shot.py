from typing import Union
from langchain.prompts import FewShotChatMessagePromptTemplate
from langchain.prompts.chat import BaseChatPromptTemplate, BaseMessagePromptTemplate


class CustomFewShotChatMessagePromptTemplate(FewShotChatMessagePromptTemplate):
    single_prompt: Union[BaseMessagePromptTemplate, BaseChatPromptTemplate]

    def format_messages(self, **kwargs):

        examples = self._get_examples(**kwargs)

        examples = [{k: e[k] for k in self.example_prompt.input_variables}
                    for e in examples]

        # Use regular prompt
        messages = [
            msg
            for ex in examples
            for msg in (self.single_prompt.format_messages(**ex) if ex["prompt"] == ex["response"] else self.example_prompt.format_messages(**ex))

        ]

        return messages
