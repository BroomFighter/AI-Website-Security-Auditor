from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    website_url = request.form.get("url", "").strip()

    # Automatically add https:// if the user left it off
    if website_url and not (
        website_url.startswith("http://") or website_url.startswith("https://")
    ):
        website_url = "https://" + website_url

    # Render results back on index.html
    return render_template("index.html", website_url=website_url)


if __name__ == "__main__":
    app.run(debug=True)