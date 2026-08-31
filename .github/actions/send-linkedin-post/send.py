#!/usr/bin/env python3
import json
import os
import sys
import urllib.error
import urllib.request

LINKEDIN_API_VERSION = "202608"
USERINFO_URL = "https://api.linkedin.com/v2/userinfo"
POSTS_URL = "https://api.linkedin.com/rest/posts"


def open_request(request):
    return urllib.request.urlopen(request, timeout=30)


def person_urn(access_token, opener=open_request):
    request = urllib.request.Request(
        USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    with opener(request) as response:
        data = json.load(response)

    subject = data.get("sub")
    if not isinstance(subject, str) or not subject:
        raise ValueError("LinkedIn userinfo response does not contain a member subject")
    return f"urn:li:person:{subject}"


def publish_post(access_token, author, message, opener=open_request):
    payload = {
        "author": author,
        "commentary": message,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    request = urllib.request.Request(
        POSTS_URL,
        data=json.dumps(payload, ensure_ascii=False).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Linkedin-Version": LINKEDIN_API_VERSION,
            "X-Restli-Protocol-Version": "2.0.0",
        },
    )
    with opener(request) as response:
        if response.status != 201:
            raise ValueError(f"LinkedIn create-post request returned HTTP {response.status}, expected 201")
        post_id = response.headers.get("x-restli-id")

    if not post_id:
        raise ValueError("LinkedIn create-post response does not contain x-restli-id")
    return post_id


def write_output(post_id):
    if "\n" in post_id:
        raise ValueError("LinkedIn post identifier must be a single line")
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        print(f"post-id={post_id}", file=output)


def write_summary(post_id):
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    with open(summary_path, "a") as summary:
        print(f"LinkedIn post published: `{post_id}`", file=summary)


def error_detail(error):
    body = error.read().decode(errors="replace").strip()
    return f"LinkedIn API request failed with HTTP {error.code}: {body or error.reason}"


def main():
    try:
        access_token = os.environ["LINKEDIN_ACCESS_TOKEN"]
        author = person_urn(access_token)
        post_id = publish_post(access_token, author, os.environ["MESSAGE"])
        write_output(post_id)
        write_summary(post_id)
    except urllib.error.HTTPError as error:
        print(error_detail(error), file=sys.stderr)
        return 1
    except (KeyError, OSError, ValueError, urllib.error.URLError) as error:
        print(f"LinkedIn post failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
