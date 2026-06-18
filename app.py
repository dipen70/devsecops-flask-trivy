from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello from DevSecOps Flask App!"})

@app.route('/fetch')
def fetch():
    url = request.args.get('url', 'https://example.com')
    response = requests.get(url)
    return jsonify({"status": response.status_code})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)