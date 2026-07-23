from flask import Flask, render_template, request
from utils.ssl_checker import check_https
from utils.headers import check_security_headers
from utils.robots import check_robots_txt

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    website_url = request.form.get("url", "").strip()
    
    if not website_url:
        return "Please provide a valid URL.", 400

    # Ensure proper scheme formatting for requests
    if not website_url.startswith("http://") and not website_url.startswith("https://"):
        formatted_url = "https://" + website_url
    else:
        formatted_url = website_url

    # Phase 9: HTTPS/SSL Check
    https_result = check_https(website_url)

    # Phase 10: Security Headers Check
    header_results = check_security_headers(formatted_url)

    # Phase 11: Robots.txt Check
    robots_result = check_robots_txt(formatted_url)

    # Format header output for rendering
    header_html = "".join([f"<li><strong>{header}:</strong> {status}</li>" for header, status in header_results.items()])

    return f"""
    <h1>Security Audit Results</h1>
    <p><strong>Target URL:</strong> {website_url}</p>
    <hr>
    <h3>1. HTTPS & SSL Analysis</h3>
    <p><strong>Status:</strong> {https_result.get('status', 'N/A')}</p>
    <p><strong>Details:</strong> {https_result.get('details', 'N/A')}</p>
    <hr>
    <h3>2. Security Headers</h3>
    <ul>
        {header_html}
    </ul>
    <br>
    <a href="/">Scan Another Website</a>
    """

if __name__ == "__main__":
    app.run(debug=True)