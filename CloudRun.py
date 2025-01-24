from flask import Flask

from FileAutoBuyer import start_from_file
app = Flask(__name__)
app.run(host="0.0.0.0", port=5000)
start_from_file()