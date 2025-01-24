from flask import Flask
from threading import Thread
from FileAutoBuyer import start_from_file

app = Flask(__name__)


# Define a function to run the background task
def run_background_task():
    start_from_file()


# Start the Flask app
if __name__ == "__main__":
    # Start the background task in a separate thread
    background_thread = Thread(target=run_background_task)
    background_thread.daemon = True  # Ensures the thread will close when the main program exits
    background_thread.start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=5000)