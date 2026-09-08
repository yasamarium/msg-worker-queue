#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime, timezone, timedelta
import requests

GITHUB_API_URL = "https://api.github.com"

def retrigger():
    pat = os.getenv("GH_PAT") or os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    workflow_id = "workflow.yml"
    ref = os.getenv("GITHUB_REF_NAME", "main")
    
    if not pat or not repo:
        print("[INFO] No GH_PAT token or repository. Skipping auto-trigger.")
        return

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {pat}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    runs_url = f"{GITHUB_API_URL}/repos/{repo}/actions/workflows/{workflow_id}/runs"
    try:
        resp = requests.get(runs_url, headers=headers, params={"status": "in_progress", "per_page": 5}, timeout=15)
        if resp.status_code == 200:
            in_prog = resp.json().get("workflow_runs", [])
            curr_run_id = os.getenv("GITHUB_RUN_ID")
            other_active = [r for r in in_prog if str(r.get("id")) != str(curr_run_id)]
            if other_active:
                print(f"[GUARD] Active workflow run already exists (Run ID: {other_active[0]['id']}). Skipping.")
                return

        dispatch_url = f"{GITHUB_API_URL}/repos/{repo}/actions/workflows/{workflow_id}/dispatches"
        print(f"Dispatching next 5-hour cycle for {repo}...")
        dispatch_resp = requests.post(dispatch_url, headers=headers, json={"ref": ref}, timeout=15)
        if dispatch_resp.status_code == 204:
            print("[SUCCESS] Next 5-hour cycle triggered successfully.")
        else:
            print(f"[ERROR] Dispatch failed: HTTP {dispatch_resp.status_code} - {dispatch_resp.text}")
    except Exception as e:
        print(f"[ERROR] Retrigger error: {e}")

if __name__ == "__main__":
    retrigger()
