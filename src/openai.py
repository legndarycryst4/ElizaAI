from llama_cpp import Llama
from .credentials import LLAMA_MODEL_PATH  # Ensure this points to your model file

llama = Llama(model_path=LLAMA_MODEL_PATH)
