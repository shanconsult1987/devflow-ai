import pytest

from app.requests import (
    create_request,
    update_status,
    get_request_summary,
    get_open_requests,
    get_requests_by_priority,
)


def test_create_request():
    request = create_request(
        "Login issue",
        "Unable to log in",
    )

    assert request["title"] == "Login issue"
    assert request["status"] == "open"
    assert request["priority"] == "Medium"


def test_create_request_strips_whitespace():
    request = create_request(
        "  Login issue  ",
        "  Unable to log in  ",
    )

    assert request["title"] == "Login issue"
    assert request["description"] == "Unable to log in"


@pytest.mark.parametrize(
    "title",
    ["", " ", None, 123],
)
def test_invalid_title(title):
    with pytest.raises(ValueError):
        create_request(title, "Description")


@pytest.mark.parametrize(
    "description",
    ["", " ", None, 123],
)
def test_invalid_description(description):
    with pytest.raises(ValueError):
        create_request("Title", description)


def test_update_status():
    request = create_request("Login", "Issue")

    result = update_status(request, "closed")

    assert result["status"] == "closed"


def test_invalid_status():
    request = create_request("Login", "Issue")

    with pytest.raises(ValueError):
        update_status(request, "invalid")


def test_invalid_request_object():
    with pytest.raises(TypeError):
        update_status(None, "closed")


def test_get_request_summary():
    request = create_request("Login", "Issue")

    assert get_request_summary(request) == {
        "title": "Login",
        "status": "open",
    }


def test_summary_missing_field():
    with pytest.raises(ValueError):
        get_request_summary({"title": "Login"})


def test_summary_invalid_input():
    with pytest.raises(TypeError):
        get_request_summary(None)


def test_get_open_requests():
    requests = [
        {"title": "A", "status": "open"},
        {"title": "B", "status": "closed"},
        {"title": "C", "status": "open"},
    ]

    result = get_open_requests(requests)

    assert len(result) == 2
    assert all(r["status"] == "open" for r in result)


def test_get_open_requests_empty():
    assert get_open_requests([]) == []


def test_get_open_requests_invalid():
    with pytest.raises(TypeError):
        get_open_requests(None)


@pytest.mark.parametrize(
    "priority",
    ["Low", "Medium", "High", "Critical"],
)
def test_get_requests_by_priority(priority):
    requests = [
        {"title": "Low request", "priority": "Low"},
        {"title": "Medium request", "priority": "Medium"},
        {"title": "High request", "priority": "High"},
        {"title": "Critical request", "priority": "Critical"},
        {"title": "Missing priority"},
        None,
    ]

    result = get_requests_by_priority(requests, priority)

    assert result == [
        {"title": f"{priority} request", "priority": priority}
    ]


@pytest.mark.parametrize(
    "priority",
    ["", "low", "urgent", None, 1],
)
def test_get_requests_by_priority_invalid_priority(priority):
    with pytest.raises(ValueError):
        get_requests_by_priority([], priority)


@pytest.mark.parametrize(
    "requests",
    [None, (), {"priority": "High"}],
)
def test_get_requests_by_priority_invalid_collection(requests):
    with pytest.raises(TypeError):
        get_requests_by_priority(requests, "High")


def test_get_requests_by_priority_empty():
    assert get_requests_by_priority([], "Low") == []
