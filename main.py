import os
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello(name=None):
    return render_template('base.html', name=name)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))