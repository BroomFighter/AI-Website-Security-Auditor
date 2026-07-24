import requests

def run_owasp_checks(target_url):
    findings = []

    try:
        response = requests.get(target_url, timeout=5, allow_redirects=True)
        headers = response.headers

        # Check 1: Server Header Exposure
        server_header = headers.get("Server")
        if server_header:
            findings.append({
                "check": "Server Banner Exposure",
                "status": "Warning",
                "details": f"Server header reveals technology stack: '{server_header}'"
            })
        else:
            findings.append({
                "check": "Server Banner Exposure",
                "status": "Pass",
                "details": "Server header is hidden or sanitized."
            })

        # Check 2: X-Powered-By Header Exposure
        powered_by = headers.get("X-Powered-By")
        if powered_by:
            findings.append({
                "check": "X-Powered-By Exposure",
                "status": "Warning",
                "details": f"Reveals internal framework/version: '{powered_by}'"
            })

        # Check 3: Cookie Security Flags
        cookies = response.cookies
        if cookies:
            for cookie in cookies:
                missing_flags = []
                
                # Check Secure flag
                if not cookie.secure:
                    missing_flags.append("Secure")
                
                # Check HttpOnly flag safely without accessing non-existent `.rest`
                rest_keys = [k.lower() for k in getattr(cookie, "_rest", {}).keys()]
                has_http_only = cookie.has_nonstandard_attr("HttpOnly") or "httponly" in rest_keys
                
                if not has_http_only:
                    missing_flags.append("HttpOnly")
                
                if missing_flags:
                    findings.append({
                        "check": f"Cookie Flag ({cookie.name})",
                        "status": "Warning",
                        "details": f"Missing flag(s): {', '.join(missing_flags)}"
                    })
                else:
                    findings.append({
                        "check": f"Cookie Flag ({cookie.name})",
                        "status": "Pass",
                        "details": "Cookie includes Secure and HttpOnly flags."
                    })
        else:
            findings.append({
                "check": "Cookie Security Flags",
                "status": "Info",
                "details": "No cookies detected on initial HTTP response."
            })

    except requests.RequestException as e:
        findings.append({
            "check": "OWASP Checks Execution",
            "status": "Error",
            "details": f"Could not reach target URL: {str(e)}"
        })

    return findings