from typing import TypeAlias

ChatCompletionMessage: TypeAlias = dict  # Llama 3.1 8B doesn't have predefined types like OpenAI

class CustomMessage:
    author: str
    content: str
    plattform: str
    answer: bool

    def __init__(self, author: str, content: str, plattform: str) -> None:
        self.author = author
        self.content = content
        self.plattform = plattform
        self.answer = False
