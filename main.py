import json

from flask import Flask, request, Response
import requests

ci_app = Flask("IzunaCI")

base_data = {
    "target_url": "https://martmists.com/check_status",
    "context": "continuous-integration/izuna"
}


@ci_app.route("/git_hook", methods=["POST"])
def git_hook():
    data = json.loads(request.data.decode())
    commit = data["commits"][0]
    files = commit["added"] + commit["modified"]
    owner, repo = data["repository"]["full_name"].split("/")
    sha = commit["id"]
    url = f"https://api.github.com/repos/{owner}/{repo}/statuses/{sha}"
    err = False
    print("Files:", files)
    print("  Url:", url)
    print(" Repo:", repo)
    print("  SHA:", sha)
    if not err:
        end_data = {
            "status": "success",
            "description": "The build passed!"
        }
    else:
        end_data = {
            "status": "failed",
            "description": "The build failed!"
        }

    requests.post(url, data=end_data.update(base_data))
    return Response("OK", 200)


ci_app.run("0.0.0.0", 5000)
