import flask
from flask import Flask, request, Response, make_response

app = Flask(__name__)


@app.route("/")
def echo():
    request_headers = []
    for k, v in request.headers:
        request_headers.append(f"<i style='color: red;'>{k}</i>: {v}")
    request_headers_resp = "<br/>".join(request_headers)

    response_headers = []
    resp = make_response()
    print(resp.headers)
    return f"<h2>Request Headers:</h2> {request_headers_resp}"



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
