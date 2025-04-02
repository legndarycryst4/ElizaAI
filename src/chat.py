from typing import Iterable, List
from llama_cpp import Llama

from .chattypes import ChatCompletionMessage
from .credentials import BOT_NAME, LLAMA_MODEL_PATH
from .logger import Logger

_default_stop = [f"{BOT_NAME}:", "CHATTER:"]

# Load Llama model
llama = Llama(model_path=LLAMA_MODEL_PATH)

def gpt3_completion(
    system_prompt: Iterable[ChatCompletionMessage],
    messages: Iterable[ChatCompletionMessage] = tuple(),
    logger: Logger | None = None,
    temp=0.9,
    tokens=150,
    freq_pen=2.0,
    pres_pen=2.0,
    stop: List[str] = _default_stop,
):
    msg: List[ChatCompletionMessage] = list(system_prompt) + list(messages)
    
    if logger is not None:
        logger.info(msg)

    prompt = "\n".join(f"{m.role}: {m.content}" for m in msg)
    
    response = llama(prompt, temperature=temp, max_tokens=tokens, stop=stop)
    
    content = response["choices"][0]["text"].strip() if response["choices"] else ""
    
    return content
