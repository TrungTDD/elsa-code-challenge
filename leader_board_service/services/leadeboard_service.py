from redis.asyncio import Redis
from config.pika.mq_service import rabbitmq_client
from models.user_score import UserScoreDict  
from config.config import config


async def publish_leaderboard_msg(quiz_id: str, redis: Redis) -> None:
    """Publish the leaderboard data to the RabbitMQ queue.

    Args:
        quiz_id: The ID of the quiz.
        redis: The Redis client.
    """
    leaderboard_data = await _get_leaderboard_data(quiz_id, redis)

    await rabbitmq_client.publish_message(
        queue_name=config.RABBITMQ_QUEUE,
        message_body=leaderboard_data
    )


async def _get_leaderboard_data(
    quiz_id: str,
    redis: Redis
) -> list[UserScoreDict]:
    """Get the leaderboard data from the Redis database for the given quiz.

    Args:
        quiz_id: The ID of the quiz.
        redis: The Redis client.

    Returns:
        The leaderboard data of the quiz.
    """
    key = f"leaderboard:{quiz_id}"
    leaderboard_data = await redis.zrevrange(key, 0, -1, withscores=True)
    user_scores = [
        UserScoreDict(name=name, score=score) 
        for name, score in leaderboard_data
    ]
    return user_scores
