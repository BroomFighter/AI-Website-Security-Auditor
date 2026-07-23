from flask import Flask, render_template, request
from utils.ssl_checker import check_https
from utils.headers import check_security_headers
from utils.robots import check_robots_txt
from utils.sitemap import check_sitemap
from utils.directories import check_exposed_directories

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

    # Phase 12: Sitemap Check
    sitemap_result = check_sitemap(formatted_url)

    # Phase 13: Exposed Directories Check
    directories_result = check_exposed_directories(formatted_url)

    # Format security headers for rendering
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
    <hr>
    <h3>3. Robots.txt Analysis</h3>
    <p><strong>Status:</strong> {robots_result['status']}</p>
    <p><strong>Details:</strong> {robots_result['details']}</p>
    <hr>
    <h3>4. Sitemap Analysis</h3>
    <p><strong>Status:</strong> {sitemap_result['status']}</p>
    <p><strong>Details:</strong> {sitemap_result['details']}</p>
    <hr>
    <h3>5. Exposed Directories Check</h3>
    <p><strong>Status:</strong> {directories_result['status']}</p>
    <p><strong>Details:</strong> {directories_result['details']}</p>
    <br>
    <a href="/">Scan Another Website</a>
    """

if __name__ == "__main__":
    app.run(debug=True)