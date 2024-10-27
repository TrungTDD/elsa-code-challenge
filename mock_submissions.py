import threading
import requests
import time
import random
import argparse
from redis import Redis
import secrets
from pathlib import Path

# API endpoint URL
API_ENDPOINT = "http://localhost:8081/leaderboard/{quiz_id}"

# Number of threads to simulate
NUM_THREADS = 50

redis_client = Redis(host="localhost", port=6379)

quiz_id = secrets.token_hex(8)

list_users = []

def initialize_leaderboard(users):
    key = f"leaderboard:{quiz_id}"
    for i in range(users):
        list_users.append(f"user_{i}")
        redis_client.zadd(key, {f"user_{i}": 0})

def submit_request(index, users):
    """Function to submit a POST request to the API endpoint."""
    try:
        # Mocking the update score of a user.
        point = random.randint(1, 10)
        key = f"leaderboard:{quiz_id}"

        # Get random user from the list to increase the score.
        random_index = random.randint(0, len(list_users) - 1)
        user = list_users[random_index]
        redis_client.zincrby(key, point, user)

        # Send request to the API.
        endpoint_url = API_ENDPOINT.format(quiz_id=quiz_id)
        response = requests.post(endpoint_url)
        if response.status_code == 200:
            print(f"Thread {index}: Submission successful!")
        else:
            print(f"Thread {index}: Submission failed with status code {response.status_code}")
    except Exception as e:
        print(f"Thread {index}: An error occurred - {e}")

def main(num_threads, users):
    threads = []

    # Create and start threads
    for i in range(num_threads):
        # Generate a random delay between 0 and 2 seconds
        random_delay = random.uniform(0, 2)

        thread = threading.Thread(target=submit_request, args=(i, users))
        threads.append(thread)
        
        # Start each thread after a random delay
        thread.start()
        time.sleep(random_delay)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument("--num_threads", type=int, default=NUM_THREADS)
    argparse.add_argument("--users", type=int, default=10)
    args = argparse.parse_args()

    initialize_leaderboard(args.users)

    main(args.num_threads, args.users)
