# rv_geocode.py
# Edit only: Set the POSITIONSTACK_KEY environment variable before running.

import os
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

api_key = os.getenv("POSITIONSTACK_KEY")
if not api_key:
    sys.stderr.write("Error: POSITIONSTACK_KEY not set.\n")
    sys.exit(1)

LAT, LON = 6.6778, 3.1654

def make_session():
    s = requests.Session()
    s.mount(
        "https://",
        HTTPAdapter(
            max_retries=Retry(
                total=3,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"],
                raise_on_status=False,
            )
        ),
    )
    return s

def reverse_geocode(lat: float, lon: float) -> str:
    url = "https://api.positionstack.com/v1/reverse"
    params = {
        "access_key": api_key,
        "query": f"{lat},{lon}",
        "limit": 1,
        "output": "json"
    }
    res = make_session().get(url, params=params, timeout=10)
    res.raise_for_status()
    data = res.json().get("data", [])
    if not data:
        raise RuntimeError("No geocoding results returned.")
    return data[0].get("label", "")

if __name__ == "__main__":
    try:
        print(reverse_geocode(LAT, LON))
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
