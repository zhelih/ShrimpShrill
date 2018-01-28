#!flask/bin/python
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/')
@app.route('/ers/post_emergency', methods=['POST', 'GET'])
def main():
    print("Headers", request.headers)
    print("User Agent", request.headers.get('User-Agent', None))
    print("Content length", request.content_length)
    print("Content type", request.content_type)
    print("Data", request.get_data())
    print("JSON", request.get_json())
    return Response(), 201

if __name__ == '__main__':
    app.run()
