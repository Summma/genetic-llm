from time import time

import grequests

endpoint = "http://localhost:11434/api/generate"

reqs = [
    grequests.post(
        endpoint,
        json={"model": "deepseek-coder-v2:16b", "prompt": "Make a program in Rust that reverse a linked list.", "stream": False}
    )
    for _ in range(40)
]

start = time()
try:
    for index, response in grequests.imap_enumerated(reqs, size=10):
        print(response.json()["response"])
        print(f"Iteration {index}")
finally:
    print(f"Time taken: {time() - start} seconds")
