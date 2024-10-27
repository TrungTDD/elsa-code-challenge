from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
import aio_pika
import asyncio

app = FastAPI()

RABBITMQ_URL = "amqp://quiz:quiz@localhost:5672/"
QUEUE_NAME = "leaderboard_queue"
clients = set()  # To store connected WebSocket clients

@app.on_event("startup")
async def startup_event():
    # Create a RabbitMQ connection and channel on startup
    app.state.connection = await aio_pika.connect_robust(RABBITMQ_URL)
    app.state.channel = await app.state.connection.channel()
    app.state.queue = await app.state.channel.declare_queue(QUEUE_NAME, durable=True)
    
    # Start consuming RabbitMQ messages in a background task
    asyncio.create_task(consume_rabbitmq())

@app.on_event("shutdown")
async def shutdown_event():
    # Close the RabbitMQ connection on shutdown
    await app.state.channel.close()
    await app.state.connection.close()

async def consume_rabbitmq():
    async with app.state.queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                # Decode the message and broadcast it to all connected clients
                data = message.body.decode()
                print("Data received from leaderboard service:", data)
                await broadcast(data)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            # Maintain the WebSocket connection (listening for messages from clients if needed)
            await websocket.receive_text()
    except WebSocketDisconnect:
        clients.remove(websocket)

async def broadcast(message: str):
    # Create a list of tasks to send messages concurrently to all clients
    send_tasks = []
    for client in clients.copy():
        send_tasks.append(send_message(client, message))
    
    # Run all send tasks concurrently
    await asyncio.gather(*send_tasks)

async def send_message(client: WebSocket, message: str):
    try:
        await client.send_text(message)
    except Exception as e:
        print(f"Error sending message to client: {e}")
        clients.remove(client)


