from collections.abc import Iterator

from huggingface_hub import InferenceClient


class LLMService:
    def __init__(self, api_token: str, model: str):
        self._client = InferenceClient(model=model, token=api_token)
        self._model = model

    def generate_stream(self, prompt: str) -> Iterator[str]:
        stream = self._client.text_generation(
            prompt,
            max_new_tokens=1024,
            stream=True,
            details=False,
        )
        for token in stream:
            yield token
