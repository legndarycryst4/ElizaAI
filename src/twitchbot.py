from typing import List

from twitchio.ext import commands  # type: ignore

from .chat import gpt3_completion  # You may need to update this function to use Llama instead of OpenAI
from .chattypes import ChatCompletionMessage
from .credentials import BOT_NAME, TWITCH_CHANNEL, TWITCH_TOKEN, LLAMA_MODEL_PATH
from .filter_message import check_and_filter_user_message
from .texttospeech_evenlabs import get_speech_by_text
from .utils import open_file
from .websocket import open_websocket

CONVERSATION_LIMIT = 20


class Bot(commands.Bot):
    conversation: List[ChatCompletionMessage] = list()

    def __init__(self, speaker_bot=False, speaker_alias="Default"):
        Bot.conversation.append(
            {"role": "system", "content": open_file("prompt_chat.txt")}
        )
        self.speaker_bot = speaker_bot
        self.speaker_alias = speaker_alias
        super().__init__(
            token=TWITCH_TOKEN,
            prefix="!",
            initial_channels=[TWITCH_CHANNEL],
        )

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")

    async def event_message(self, message):
        if check_and_filter_user_message(message):
            return

        msg = message.content
        user = message.author.name
        user_question = msg.encode(encoding="ASCII", errors="ignore").decode()
        print("------------------------------------------------------")
        print(Bot.conversation)
        print(f"{user} say: {user_question}")

        Bot.conversation.append({"role": "user", "content": user_question})

        # Update this line to call Llama instead of OpenAI
        bot_response = gpt3_completion(Bot.conversation, model_path=LLAMA_MODEL_PATH)  
        print(f"{BOT_NAME}:", bot_response)

        conversation = {"role": "assistant", "content": bot_response}
        if Bot.conversation.count(conversation) == 0:
            Bot.conversation.append(conversation)

        if len(Bot.conversation) > CONVERSATION_LIMIT:
            Bot.conversation = Bot.conversation[1:]

        if self.speaker_bot:
            self.send_to_speaker_bot(bot_response)
            await self.handle_commands(message)
            return

        get_speech_by_text(user_question, bot_response)

        await self.handle_commands(message)

    @commands.command(name="hola", aliases=["op", "haupei", "alo", "buen día"])
    async def hello(self, ctx: commands.Context):
        await ctx.send(f"Hello {ctx.author.name}!")

    async def send_to_speaker_bot(self, message: str, verbose=False) -> None:
        await open_websocket(self.speaker_alias, message, verbose)
