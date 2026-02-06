import requests
from config import OKAPI_BASE_URL, OKAPI_TENANT
from services.auth import get_okapi_token, FolioAuthError


class FolioSearchError(Exception):
    pass


def search_instances_by_subject(subject: str, offset: int = 0, limit: int = 10):
    # Keep inputs honest so we don't send broken queries to FOLIO.
    if not subject:
        raise FolioSearchError("Subject is required.")

    # Auth token for Okapi requests.
    token = get_okapi_token()

    # FOLIO search endpoint + Okapi headers.
    url = f"{OKAPI_BASE_URL}/search/instances"
    headers = {
        "x-okapi-tenant": OKAPI_TENANT,
        "x-okapi-token": token,
        "Accept": "application/json",
    }

    # Build a subject query; expandAll pulls related fields for display.
    params = {
        "expandAll": "true",
        "limit": limit,
        "offset": offset,
        "query": f'subjects.value=="{subject}"'
    }

    resp = requests.get(url, headers=headers, params=params, timeout=15)

    if resp.status_code >= 400:
        raise FolioSearchError(f"Search failed: {resp.status_code} {resp.text}")

    # Normalize the payload into a small, template-friendly shape.
    data = resp.json()

    total = data.get("totalRecords", 0)
    instances = data.get("instances", [])

    records = []
    for inst in instances:
        # Pick only what we want to display.
        records.append({
            "title": inst.get("title"),
            "subjects": [s.get("value") for s in inst.get("subjects", [])],
            "contributors": [
                c.get("name") for c in inst.get("contributors", [])
            ],
            "created": inst.get("metadata", {}).get("createdDate")
        })

    return {
        "total": total,
        "records": records
    }
