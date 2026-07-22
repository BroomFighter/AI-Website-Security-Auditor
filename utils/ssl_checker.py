import requests

def check_https(url: str) -> dict:
    """
    Checks whether a URL supports HTTPS and has a valid SSL certificate.
    """
    # Ensure URL has a protocol scheme
    if not url.startswith("http://") and not url.startswith("https://"):
        target_url = "https://" + url
    elif url.startswith("http://"):
        target_url = url.replace("http://", "https://", 1)
    else:
        target_url = url

    result = {
        "https_enabled": False,
        "ssl_valid": False,
        "status": "",
        "details": ""
    }

    try:
        # verify=True ensures requests validates the SSL certificate chain
        response = requests.get(target_url, timeout=5, verify=True)
        
        result["https_enabled"] = True
        result["ssl_valid"] = True
        result["status"] = "✔ HTTPS Enabled & Valid SSL Certificate"
        result["details"] = f"Successfully connected over HTTPS (HTTP status code {response.status_code})."

    except requests.exceptions.SSLError as ssl_err:
        # HTTPS endpoint responded, but the SSL certificate failed verification
        result["https_enabled"] = True
        result["ssl_valid"] = False
        result["status"] = "✘ SSL Certificate Error"
        result["details"] = "The server supports HTTPS, but the SSL certificate is invalid, expired, or untrusted."

    except requests.exceptions.ConnectionError:
        result["https_enabled"] = False
        result["ssl_valid"] = False
        result["status"] = "✘ HTTPS Connection Failed"
        result["details"] = "Could not establish an HTTPS connection to the host."

    except requests.exceptions.Timeout:
        result["https_enabled"] = False
        result["ssl_valid"] = False
        result["status"] = "✘ Connection Timed Out"
        result["details"] = "The HTTPS request timed out after 5 seconds."

    except Exception as e:
        result["https_enabled"] = False
        result["ssl_valid"] = False
        result["status"] = "✘ Request Error"
        result["details"] = str(e)

    return result