from functools import wraps
from flask import Flask, request
app = Flask(__name__)
key = "ya29.bwLu0ruxXdXe_RMOSYgfiCPORNMHLkf9rCDmV1rKtWu90TuF1d8B2SmdUlrjeOWNYThkgMM"

def secure(f):
    @wraps(f)
    def check_authorization(*args, **kwargs):
        if request.headers.get("Authorization") == key:
            return f()
        else:
            return "lol no"
    
    return check_authorization

@app.route("/")
@secure
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug=True)

