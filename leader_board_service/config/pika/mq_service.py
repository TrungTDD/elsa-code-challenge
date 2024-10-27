import aio_pika
import json
from config.config import config

class RabbitMQClient:
    def __init__(self):
        self.rabbitmq_url = config.rabbitmq_url
        self.connection = None
        self.channel = None

    async def connect(self):
        """Establish the connection and channel."""
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()

    async def close(self):
        """Close the channel and connection."""
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()

    async def publish_message(self, queue_name: str, message_body: dict):
        """Publish a message to the specified queue.

        Args:
            queue_name: The name of the queue.
            message_body: The body of the message.
        """
        message = aio_pika.Message(body=json.dumps(message_body).encode())
        await self.channel.default_exchange.publish(
            message,
            routing_key=queue_name
        )

rabbitmq_client = RabbitMQClient()