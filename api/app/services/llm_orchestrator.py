import json
import os
import shutil
import subprocess
import tempfile

from api.app.config import DEMO_REPO_PATH, WORKSPACE_DIR

def run_sandbox_for_investigation(investigation):
    """
    Demo sandbox:
    - load patch file for this investigation
    - copy demo repo into temporary workspace
    - overwrite target file
    - run pytest
    - return (status, logs_path, logs_text)
    """
    if not investigation.patch_file or not os.path.exists(investigation.patch_file):
        return ("ERROR", None, "No patch file found for investigation")

    with open(investigation.patch_file, "r", encoding="utf-8") as fh:
        patch = json.load(fh)

    ws_parent = WORKSPACE_DIR
    os.makedirs(ws_parent, exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="workspace_", dir=ws_parent)

    repo_copy = os.path.join(tmpdir, "repo")
    shutil.copytree(DEMO_REPO_PATH, repo_copy, dirs_exist_ok=True)

    target_rel = patch["target_file"]
    target_abs = os.path.join(repo_copy, target_rel)
    os.makedirs(os.path.dirname(target_abs), exist_ok=True)

    with open(target_abs, "w", encoding="utf-8") as fh:
        fh.write(patch["new_content"])

    cmd = ["pytest", "-q"]
    proc = subprocess.Popen(
        cmd,
        cwd=repo_copy,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        out, _ = proc.communicate(timeout=60)
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        proc.kill()
        out = "Sandbox timed out"
        exit_code = 124

    logs_path = os.path.join(tmpdir, "sandbox_logs.txt")
    with open(logs_path, "w", encoding="utf-8") as fh:
        fh.write(out)

    if exit_code == 0:
        status = "VERIFIED"
    elif exit_code == 124:
        status = "TIMEOUT"
    else:
        status = "FAILED"

    return status, logs_path, out