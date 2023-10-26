from re import I
from typing import Union
from langchain.prompts import FewShotChatMessagePromptTemplate
from langchain.prompts.chat import BaseChatPromptTemplate, BaseMessagePromptTemplate
from numpy import append


class CustomFewShotChatMessagePromptTemplate(FewShotChatMessagePromptTemplate):
    single_prompt: Union[BaseMessagePromptTemplate, BaseChatPromptTemplate]
    system_prompt: Union[BaseMessagePromptTemplate, BaseChatPromptTemplate]

    def format_messages(self, **kwargs):

        examples = self._get_examples(**kwargs)
        cues = [ex for ex in examples if ex.type == "cue"]
        thoughts = [ex for ex in examples if ex.type == "thought"]
        print("thoughts are",thoughts)
        messages = []
        if len(cues) > 0:
            messages.extend(self.system_prompt.format_messages(
                text="The following cues are similar to the user's last message and show the character's response and other semantically similar responses."))

            for cue in cues:
                messages.extend(
                    self.example_prompt.format_messages(cue=cue.text, response=cue.pair.text))
                # cue=cue.text, response=cue.pair.text))

                if len(cue.pair.similar) > 0:
                    messages.extend(self.system_prompt.format_messages(
                        text="The following responses, don't necessarily respond to the same cue, but are semantically similar to the response to the above cue."))
                    for response in cue.pair.similar:
                        messages.extend(
                            self.single_prompt.format_messages(**response.dict()))

        if len(thoughts) > 0:
            messages.extend(self.system_prompt.format_messages(
                text="The following example messages are independant thoughts semantically matching the user's last message."))

            for thought in thoughts:
                messages.extend(
                    self.single_prompt.format_messages(**thought.dict()))

        print(messages)
        return messages
        # Format remaining examples normally
        # examples = [{k: ex[k] for k in self.example_prompt.input_variables}
        #             for ex in examples]

        # messages.extend([
        #     msg
        #     for ex in examples
        #     for msg in (self.single_prompt.format_messages(**ex) if ex["prompt"] == ex["response"] else self.example_prompt.format_messages(**ex))
        # ])
