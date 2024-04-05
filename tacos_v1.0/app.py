from flask import *

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template("index.html")


@app.route('/index')
def x():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/registro')
def registro():
    return render_template("registro.html")

@app.route('/products')
def products():
    return render_template("products.html")


if __name__ == "__main__":
    app.run(debug=True)
