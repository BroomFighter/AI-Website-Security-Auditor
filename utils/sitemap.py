import requests

def check_sitemap(url):
    """
    Checks if /sitemap.xml is publicly accessible.
    """
    base_url = url.rstrip("/")
    sitemap_url = f"{base_url}/sitemap.xml"

    try:
        response = requests.get(sitemap_url, timeout=5)
        if response.status_code == 200:
            return {
                "status": "Present",
                "url": sitemap_url,
                "details": "sitemap.xml was found."
            }
        else:
            return {
                "status": "Missing",
                "url": sitemap_url,
                "details": f"Server returned status code {response.status_code}."
            }
    except requests.RequestException as e:
        return {
            "status": "Error",
            "url": sitemap_url,
            "details": f"Could not connect: {str(e)}"
        }