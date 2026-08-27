# main.py: Entry point for the URL fetcher application.

from url_fetcher import url_queue, populate_queue

def main():
    """
    Main function to start the URL fetching process.
    """
    # Initialize the queue
    url_queue = Queue(maxsize=QUEUE_SIZE)

    # Populate the queue with URLs
    populate_queue(url_queue)

    # Process the queue (for demonstration purposes, we just print the URLs)
    while not url_queue.empty():
        url = url_queue.get()
        print(f"Fetched URL: {url}")
        url_queue.task_done()

if __name__ == "__main__":
    main()