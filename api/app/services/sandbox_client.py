import os
import shutil
import json
import subprocess
import tempfile
from datetime import datetime
from api.app.config import WORKSPACE_DIR, DEMO_REPO_PATH

def run_sandbox_for_investigation(Investigation):
    """
    For demo: copy DEMO_REPO_PATH to a temp workspace, read the patch JSON referenced
    by investigation.patch_file, overwrite the target file, run pytest, and return (status, logs_path, logs_text)
    """
    repo_src = DEMO_REPO_PATH
    # load patch file
    if not investigation.patch_file or not os.path.exists(investigation.patch_file):
        return ("ERROR", None, "No patch file found")

    with open(investigation.patch_file, "r", encoding="utf-8") as fh:
        patch = json.load(fh)

    # create temp workspace
    ws_parent = WORKSPACES_DIR if WORKSPACES_DIR else os.path.join(os.path.dirname(__file__), "..", "..", "data", "workspaces")
    os.makedirs(ws_parent, exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="workspace_", dir=ws_parent)
    # copy repo
    shutil.copytree(repo_src, os.path.join(tmpdir, "repo"), dirs_exist_ok=True)
    workspace_repo = os.path.join(tmpdir, "repo")

    # apply patch (for demo: overwrite the target file)
    target_rel = patch["target_file"]
    target_abs = os.path.join(workspace_repo, target_rel)
    os.makedirs(os.path.dirname(target_abs), exist_ok=True)
    with open(target_abs, "w", encoding="utf-8") as fh:
        fh.write(patch["new_content"])

    # run tests using subprocess pytest -q
    cmd = ["pytest", "-q"]
    proc = subprocess.Popen(cmd, cwd=workspace_repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        out, _ = proc.communicate(timeout=60)
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        proc.kill()
        out = "Sandbox timed out"
        exit_code = 124

    # write logs to a file
    logs_path = os.path.join(tmpdir, "sandbox_logs.txt")
    with open(logs_path, "w", encoding="utf-8") as fh:
        fh.write(out)

    if exit_code == 0:
        status = "VERIFIED"
    elif exit_code == 124:
        status = "TIMEOUT"
    else:
        status = "FAILED"

    # NOTE: For a real sandbox you would destroy tmpdir after storing logs to object storage.
    return (status, logs_path, out)