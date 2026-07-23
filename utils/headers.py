import requests
SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "Referrer-Policu",
    "Permissions-Policy",
    "X-Content-Type-Options",
]

def check_security_headers(url):
    """Fetches reponse headers for a URL and checks  for standard security headers."""

    try:
        response = requests.get(url, timeout=5)

        results = {}
        for header in SECURITY_HEADERS:
            if header in response.headers:
                results[header] = "Present"
            else:
                results[header] = "Missing"

        return results

    except requests.RequestException as e:
        return {"error": f"Failed to connect to {url}: {str(e)}"}