from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    huggingface_api_token: str = ""
    chroma_persist_dir: str = "/app/data"
    max_upload_size: int = 10_485_760
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 4
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "mistralai/Mistral-7B-Instruct-v0.3"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
