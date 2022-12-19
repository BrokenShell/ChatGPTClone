import os
import openai
from gradio import Blocks, Markdown, Chatbot, State, Textbox
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


def openai_create(prompt: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0.01,
        presence_penalty=0.6,
    )
    result, *_ = response.choices
    return result.text


def chatgpt_clone(text_input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(text_input)
    output = openai_create(" ".join(s))
    history.append((text_input, output))
    return history, history


def init():
    with Blocks() as block:
        Markdown("# ChatBot")
        chatbot = Chatbot()
        state = State()
        message = Textbox()
        message.submit(
            chatgpt_clone,
            inputs=[message, state],
            outputs=[chatbot, state],
        )
    block.launch()


if __name__ == '__main__':
    init()
