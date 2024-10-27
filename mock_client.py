import asyncio
import websockets
from time import sleep
import argparse

# WebSocket server URL
WEBSOCKET_URL = "ws://localhost:8080/ws"

# Number of connections to simulate
DEFAULT_NUM_CONNECTIONS = 5

# List to store all tasks for connections
tasks = []

async def mock_websocket_connection(index):
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print(f"Connection {index} established.")

            # Keep the connection open
            while True:
                try:
                    message = await websocket.recv()
                    print(f"Connection {index} received: {message}")
                except websockets.ConnectionClosed:
                    print(f"Connection {index} closed.")
                    break
                await asyncio.sleep(1)  # Keep the connection alive
    except Exception as e:
        print(f"Error on connection {index}: {e}")

async def main(num_connections):
    for i in range(num_connections):
        # Schedule each connection as a coroutine
        tasks.append(mock_websocket_connection(i))
    
    # Run all tasks concurrently
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument("--num_connections", type=int, default=DEFAULT_NUM_CONNECTIONS)
    args = argparse.parse_args()

    asyncio.run(main(args.num_connections))
