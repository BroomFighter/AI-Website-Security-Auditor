from flask import Flask, render_template, request
from utils.ssl_checker import check_https

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    website_url = request.form.get("url", "").strip()
    
    if not website_url:
        return "Please provide a valid URL.", 400

    # Run Phase 9 check
    https_result = check_https(website_url)

    return f"""
    <h1>Security Audit Results</h1>
    <p><strong>Target URL:</strong> {website_url}</p>
    <hr>
    <h3>HTTPS & SSL Analysis</h3>
    <p><strong>Status:</strong> {https_result['status']}</p>
    <p><strong>Details:</strong> {https_result['details']}</p>
    <br>
    <a href="/">Scan Another Website</a>
    """

if __name__ == "__main__":
    app.run(debug=True)