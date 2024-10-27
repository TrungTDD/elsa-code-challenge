from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

root_dir = Path(__file__).parent.parent
env_folder = root_dir.joinpath("")
ENV_FILE_PATH = str(env_folder.joinpath(".env"))

class Config(BaseSettings):
    RABBITMQ_HOST: str = Field(default="localhost")
    RABBITMQ_PORT: int = Field(default=5672)
    RABBITMQ_USER: str = Field(...)
    RABBITMQ_PASSWORD: str = Field(...)
    RABBITMQ_QUEUE: str = Field(default="leaderboard_queue")

    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)

    model_config = SettingsConfigDict(
        env_prefix="",
        case_sensitive=False,
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def rabbitmq_url(self) -> str:
        return (
            f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@"
            f"{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"
        )
    
    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

config = Config()