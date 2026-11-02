"""Service request management business logic."""

VALID_STATUSES = (
    "open",
    "in_progress",
    "closed",
)


def create_request(
    title: str,
    description: str,
) -> dict:
    """Create a service request."""

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title is required")

    if (
        not isinstance(description, str)
        or not description.strip()
    ):
        raise ValueError("Description is required")

    return {
        "title": title.strip(),
        "description": description.strip(),
        "status": "open",
    }


def update_status(
    request: dict,
    status: str,
) -> dict:
    """Update service request status."""

    if not isinstance(request, dict):
        raise TypeError("Request must be a dictionary")

    if status not in VALID_STATUSES:
        raise ValueError("Invalid status")

    request["status"] = status

    return request


def get_request_summary(request: dict) -> dict:
    """Return a request summary."""

    if not isinstance(request, dict):
        raise TypeError("Request must be a dictionary")

    for field in ("title", "status"):
        if field not in request:
            raise ValueError(f"Missing field: {field}")

    return {
        "title": request["title"],
        "status": request["status"],
    }


def get_open_requests(requests: list[dict]) -> list[dict]:
    """Return only requests that are open."""

    if not isinstance(requests, list):
        raise TypeError("Requests must be a list")

    return [
        request
        for request in requests
        if isinstance(request, dict)
        and request.get("status") == "open"
    ]