from flask import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/registro')
def registro():
    return render_template("registro.html")


if __name__ == "__main__":
    app.run(debug=True)
