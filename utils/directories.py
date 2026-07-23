import requests

# Common sensitive or administrative paths to check
COMMON_PATHS = [
    "/admin",
    "/login",
    "/backup",
    "/config",
    "/uploads"
]

def check_exposed_directories(url):
    """
    Checks common endpoints to see if they return HTTP 200 OK.
    """
    base_url = url.rstrip("/")
    exposed = []

    for path in COMMON_PATHS:
        target_endpoint = f"{base_url}{path}"
        try:
            response = requests.get(target_endpoint, timeout=3, allow_redirects=True)
            if response.status_code == 200:
                exposed.append(path)
        except requests.RequestException:
            continue

    if exposed:
        return {
            "status": "Potentially Exposed",
            "exposed_paths": exposed,
            "details": f"Found {len(exposed)} accessible path(s): {', '.join(exposed)}"
        }
    else:
        return {
            "status": "Secure",
            "exposed_paths": [],
            "details": "None of the common directory paths returned an open 200 status."
        }