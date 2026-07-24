from flask import Flask, render_template, request
from utils.ssl_checker import check_https
from utils.headers import check_security_headers
from utils.robots import check_robots_txt
from utils.sitemap import check_sitemap
from utils.directories import check_exposed_directories
from utils.scanner import run_owasp_checks
from utils.ai_explainer import explain_findings  # Import AI explainer

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    website_url = request.form.get("url", "").strip()
    
    if not website_url:
        return "Please provide a valid URL.", 400

    if not website_url.startswith("http://") and not website_url.startswith("https://"):
        formatted_url = "https://" + website_url
    else:
        formatted_url = website_url

    # Gather scan findings
    https_result = check_https(website_url)
    header_results = check_security_headers(formatted_url)
    robots_result = check_robots_txt(formatted_url)
    sitemap_result = check_sitemap(formatted_url)
    directories_result = check_exposed_directories(formatted_url)
    owasp_results = run_owasp_checks(formatted_url)

    # Combine findings into a single dictionary for the AI
    all_findings = {
        "HTTPS": https_result.get('details', 'N/A'),
        "Security Headers": header_results,
        "Robots.txt": robots_result.get('details', 'N/A'),
        "Sitemap": sitemap_result.get('details', 'N/A'),
        "Exposed Directories": directories_result.get('details', 'N/A'),
        "OWASP Checks": owasp_results
    }

    # Generate AI Explanation
    ai_summary = explain_findings(all_findings)

    header_html = "".join([f"<li><strong>{header}:</strong> {status}</li>" for header, status in header_results.items()])
    owasp_html = "".join([f"<li><strong>{f['check']}:</strong> [{f['status']}] {f['details']}</li>" for f in owasp_results])

    return f"""
    <h1>Security Audit Results</h1>
    <p><strong>Target URL:</strong> {website_url}</p>
    <hr>
    <h3>🤖 AI Security Analysis Summary</h3>
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff; white-space: pre-wrap;">
        {ai_summary}
    </div>
    <hr>
    <h3>1. HTTPS & SSL Analysis</h3>
    <p><strong>Status:</strong> {https_result.get('status', 'N/A')}</p>
    <p><strong>Details:</strong> {https_result.get('details', 'N/A')}</p>
    <hr>
    <h3>2. Security Headers</h3>
    <ul>{header_html}</ul>
    <hr>
    <h3>3. Robots.txt Analysis</h3>
    <p><strong>Status:</strong> {robots_result.get('status', 'N/A')}</p>
    <p><strong>Details:</strong> {robots_result.get('details', 'N/A')}</p>
    <hr>
    <h3>4. Sitemap Analysis</h3>
    <p><strong>Status:</strong> {sitemap_result.get('status', 'N/A')}</p>
    <p><strong>Details:</strong> {sitemap_result.get('details', 'N/A')}</p>
    <hr>
    <h3>5. Exposed Directories Check</h3>
    <p><strong>Status:</strong> {directories_result.get('status', 'N/A')}</p>
    <p><strong>Details:</strong> {directories_result.get('details', 'N/A')}</p>
    <hr>
    <h3>6. OWASP Misconfiguration Checks</h3>
    <ul>{owasp_html}</ul>
    <br>
    <a href="/">Scan Another Website</a>
    """

if __name__ == "__main__":
    app.run(debug=True)