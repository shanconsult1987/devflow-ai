"""DevFlow custom MCP server.

Provides controlled repository and GitHub operations.

Transport: stdio
Authentication: GitHub CLI authentication
"""

import json
import os
import re
import subprocess

from pathlib import Path

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("DevFlow MCP Server")

ROOT = Path(
    os.environ.get("DEVFLOW_REPO", Path.cwd())
).resolve()

ALLOWED_FILES = {
    "README.md",
    "requirements.txt",
    "specs.md",
    "app/requests.py",
    "tests/test_requests.py",
}

VALID_LABELS = {
    "ai-in-progress",
    "ai-needs-review",
    "bug",
    "enhancement",
}


def run_command(
    command: list[str],
    timeout: int = 30,
) -> str:
    """Execute an explicitly constructed command."""

    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
            or result.stdout.strip()
            or "Command failed"
        )

    return result.stdout.strip()


def repository_name() -> str:
    """Return the authenticated GitHub repository name."""

    return run_command([
        "gh",
        "repo",
        "view",
        "--json",
        "nameWithOwner",
        "-q",
        ".nameWithOwner",
    ])


@mcp.tool()
def list_open_issues(limit: int = 10) -> str:
    """List open GitHub Issues."""

    if not 1 <= limit <= 30:
        raise ValueError("Limit must be between 1 and 30")

    repo = repository_name()

    output = run_command([
        "gh",
        "issue",
        "list",
        "--repo",
        repo,
        "--state",
        "open",
        "--limit",
        str(limit),
        "--json",
        "number,title,labels,url",
    ])

    return output


@mcp.tool()
def get_issue(issue_number: int) -> str:
    """Retrieve a GitHub Issue."""

    if issue_number < 1:
        raise ValueError("Invalid issue number")

    repo = repository_name()

    output = run_command([
        "gh",
        "api",
        f"repos/{repo}/issues/{issue_number}",
    ])

    issue = json.loads(output)

    return json.dumps({
        "number": issue["number"],
        "title": issue["title"],
        "body": issue.get("body") or "",
        "state": issue["state"],
        "html_url": issue["html_url"],
        "labels": [
            label["name"]
            for label in issue.get("labels", [])
        ],
    }, indent=2)


@mcp.tool()
def inspect_file(relative_path: str) -> str:
    """Read an explicitly allowlisted project file."""

    if relative_path not in ALLOWED_FILES:
        raise ValueError("File is not allowlisted")

    path = (ROOT / relative_path).resolve()

    if ROOT not in path.parents:
        raise ValueError("Path traversal is not permitted")

    if not path.is_file():
        raise FileNotFoundError(relative_path)

    return path.read_text(encoding="utf-8")


@mcp.tool()
def run_tests() -> str:
    """Run the complete pytest suite."""

    output = run_command(
        ["python", "-m", "pytest", "-v"],
        timeout=120,
    )

    return output


@mcp.tool()
def get_git_diff() -> str:
    """Return the current tracked working-tree diff."""

    return run_command([
        "git",
        "diff",
        "--",
        "app/",
        "tests/",
        "README.md",
    ])


@mcp.tool()
def add_issue_comment(
    issue_number: int,
    comment: str,
) -> str:
    """Add a progress comment to a GitHub Issue."""

    if issue_number < 1:
        raise ValueError("Invalid issue number")

    if not comment.strip():
        raise ValueError("Comment cannot be empty")

    if len(comment) > 5000:
        raise ValueError("Comment exceeds 5000 characters")

    repo = repository_name()

    return run_command([
        "gh",
        "issue",
        "comment",
        str(issue_number),
        "--repo",
        repo,
        "--body",
        comment,
    ])


@mcp.tool()
def update_issue_labels(
    issue_number: int,
    labels: list[str],
) -> str:
    """Replace Issue labels using an approved label allowlist."""

    if issue_number < 1:
        raise ValueError("Invalid issue number")

    if not labels:
        raise ValueError("At least one label is required")

    if not set(labels).issubset(VALID_LABELS):
        raise ValueError("Unsupported label requested")

    repo = repository_name()

    return run_command([
        "gh",
        "issue",
        "edit",
        str(issue_number),
        "--repo",
        repo,
        "--add-label",
        ",".join(labels),
    ])


@mcp.tool()
def create_pull_request(
    title: str,
    body: str,
) -> str:
    """Create a PR from the current feature branch into main.

    Does not merge the pull request.
    """

    if not title.strip() or len(title) > 200:
        raise ValueError("Invalid PR title")

    if not body.strip() or len(body) > 10000:
        raise ValueError("Invalid PR body")

    branch = run_command([
        "git",
        "branch",
        "--show-current",
    ])

    if branch == "main":
        raise ValueError("Cannot create a PR from main")

    if not re.fullmatch(
        r"feature/[a-z0-9][a-z0-9-]*",
        branch,
    ):
        raise ValueError("Unsupported feature branch")

    repo = repository_name()

    return run_command([
        "gh",
        "pr",
        "create",
        "--repo",
        repo,
        "--base",
        "main",
        "--head",
        branch,
        "--title",
        title,
        "--body",
        body,
    ], timeout=60)


if __name__ == "__main__":
    mcp.run(transport="stdio")