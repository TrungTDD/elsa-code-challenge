from fastapi import FastAPI, Depends, BackgroundTasks
from config.pika.mq_service import rabbitmq_client
from contextlib import asynccontextmanager
from dependencies import get_redis_client
from services import leadeboard_service as svc


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to RabbitMQ on startup
    await rabbitmq_client.connect()
    yield
    # Close the RabbitMQ connection on shutdown
    await rabbitmq_client.close()


app = FastAPI(lifespan=lifespan)


@app.post("/leaderboard/{quiz_id}")
async def publish_leaderboard_msg(
    quiz_id: str,
    redis = Depends(get_redis_client),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Publish the leaderboard data to the RabbitMQ queue.

    Args:
        quiz_id: The ID of the quiz.
        redis: The Redis client.
        background_tasks: The background tasks.

    Returns:
        The status of the message publication.
    """
    # Publish the message to the queue
    background_tasks.add_task(svc.publish_leaderboard_msg, quiz_id, redis)

    return {"status": "Message published"}
