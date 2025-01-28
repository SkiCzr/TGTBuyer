from flask import Flask
from threading import Thread
from FileAutoBuyer import start_from_file

app = Flask(__name__)


# Define a dummy route
@app.route("/")
def keep_alive():
    return "The app is running!"


# Function to run your main application
def run_main_task():
    port = 5000  # Render usually expects this to be dynamic; use PORT if set
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":

    background_thread = Thread(target=run_main_task)
    background_thread.daemon = True
    background_thread.start()
    start_from_file()
    # Start your main task in a separate thread
    # Start the dummy Flask app to keep Render happy


