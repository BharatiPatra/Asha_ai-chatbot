import threading
import time

from utils.data_back_util import json_file_to_string, clear_json_file, JSON_FILE
from agent.agents import rag

def scheduled_task():
    """This is the task to be executed every hour."""
    json_text = json_file_to_string(JSON_FILE)
    if json_text is None:
        print("JSON file is empty")
        return
    clear_json_file(JSON_FILE)  # Clear the file before inserting new data
    rag.insert(json_text)
    print("Scheduled task executed!")
    # Add the logic you want to run here

def task_scheduler():
    """This function schedules the task to run every hour in a separate thread."""
    while True:
        # Wait for 1 hour (3600 seconds)
        time.sleep(10)  # 1 hour in seconds
        
        # Execute the scheduled task
        scheduled_task()

def start_scheduler():
    """Starts the scheduler in a separate thread."""
    scheduler_thread = threading.Thread(target=task_scheduler)
    scheduler_thread.daemon = True  # Set the thread as daemon to not block the main program
    scheduler_thread.start()

if __name__ == "__main__":
    # Start the task scheduler in a separate thread
    start_scheduler()
