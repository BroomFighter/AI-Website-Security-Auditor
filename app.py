from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    website_url = request.form["url"]

    return f"""
    <h1>Website Scan Started</h1>
    <p>Target Website:</p>
    <p>{website_url}</p>
    <br>
    <a href="/">Go Back</a>
    """


if __name__ == "__main__":
    app.run(debug=True)