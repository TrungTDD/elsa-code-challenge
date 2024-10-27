from config.config import config
import redis.asyncio as redis


async def get_redis_client():
    redis_client = await redis.from_url(config.redis_url, decode_responses=True)
    try:
        yield redis_client
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        await redis_client.close()
