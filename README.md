# DevFlow AI

DevFlow AI provides service request management functions in `app.requests`.

## Service requests

Create a request with a title and description. New requests have an `open`
status and a default `Medium` priority.

```python
from app.requests import create_request, get_requests_by_priority

request = create_request("Login issue", "Unable to log in")
requests = [request]
high_priority_requests = get_requests_by_priority(requests, "High")
```

Supported priorities are `Low`, `Medium`, `High`, and `Critical`.
`get_requests_by_priority` requires a list of requests and raises `ValueError`
for an unsupported priority.

## Tests

Run the test suite with:

```sh
python -m pytest -v
```
