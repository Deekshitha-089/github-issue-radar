
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# GitHub organization we want to inspect
github_profile = "openvinotoolkit"

# GitHub API URL for the organization's repositories
api_url = (
    f"https://api.github.com/orgs/{github_profile}/repos"
    "?per_page=100"
)

# Create a request with a User-Agent header
request = Request(
    api_url,
    headers={
        "User-Agent": "github-issue-radar"
    }
)

try:
    # Send the request to GitHub
    with urlopen(request, timeout=15) as response:

        # Read the response and convert JSON into Python data
        data = json.loads(response.read().decode("utf-8"))

    print("Successfully connected to GitHub!")
    print(f"Organization: {github_profile}")
    print(f"Repositories found: {len(data)}")

    # Display repository names
    for repository in data:
        print(repository["name"])

except HTTPError as error:
    print(f"GitHub returned an error: {error.code}")

except URLError as error:
    print(f"Could not connect to GitHub: {error.reason}")
