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
        styles = [ex for ex in examples if ex.type == "style"]
        # print("stylesare",styles)
        messages = []
        # if len(cues) > 0:
        #     messages.extend(self.system_prompt.format_messages(
        #         text="The following cues are similar to the user's last message and show the character's response and other semantically similar responses."))

        #     for cue in cues:
        #         messages.extend(
        #             self.example_prompt.format_messages(cue=cue.text, response=cue.pair.text))
        #         # cue=cue.text, response=cue.pair.text))

        #         if len(cue.pair.similar) > 0:
        #             messages.extend(self.system_prompt.format_messages(
        #                 text="The following responses, don't necessarily respond to the same cue, but are semantically similar to the response to the above cue."))
        #             for response in cue.pair.similar:
        #                 messages.extend(
        #                     self.single_prompt.format_messages(**response.dict()))

        if len(styles) > 0:
            messages.extend(self.system_prompt.format_messages(
            text =  "Please utilize the following example messages, including tweets or Reddit posts, to better grasp and replicate the writing style, punctuation, syntax, choice of words, and rhythm of the {identified_character}. Pay special attention to their use of language, informal vs. formal tones, emoji or slang usage, and overall communicative approach. These examples are essential for accurately capturing the authentic tone and typical online interaction style of the character."))

            for style in styles:
                messages.extend(
                    self.single_prompt.format_messages(**style.dict()))


        if len(thoughts) > 0:
            messages.extend(self.system_prompt.format_messages(
                text="Additional thoughts, including insights from blogs and YouTube transcripts, are provided below. These are aligned with the user's last message to enrich the conversation with relevant knowledge for the {identified_character}."))

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
