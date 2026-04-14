from flask import Flask, jsonify
from flask_cors import CORS

from game_logic import get_game_status

app = Flask(__name__)
CORS(app)


@app.get("/")
def health_check():
    return jsonify({"message": "Backend Flask dang chay tren cong 5000"})


@app.get("/api/status")
def game_status():
    return jsonify(get_game_status())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
