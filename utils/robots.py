import requests

def check_robots_txt(url):
    """
    Checks if a website has a publicly accessible robots.txt file.
    """
    # Ensure standard formatting for the target URL
    base_url = url.rstrip("/")
    robots_url = f"{base_url}/robots.txt"

    try:
        response = requests.get(robots_url, timeout=5)
        
        if response.status_code == 200:
            return {
                "status": "Present",
                "url": robots_url,
                "details": "robots.txt is publicly accessible."
            }
        else:
            return {
                "status": "Missing",
                "url": robots_url,
                "details": f"Server returned status code {response.status_code}."
            }

    except requests.RequestException as e:
        return {
            "status": "Error",
            "url": robots_url,
            "details": f"Could not connect: {str(e)}"
        }