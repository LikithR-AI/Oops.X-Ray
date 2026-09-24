import os
import json
from api.app.config import DEMO_REPO_PATH

# This mock returns a deterministic "patch" for the demo app.
def produce_mock_investigation(incident, repo_path=DEMO_REPO_PATH):
    """
    For the demo we return:
    - root_cause: short string
    - affected_files: list of paths relative to repo root
    - path_file: path under data/workspaces/... where we will write the patch data(for bokkeeping)
    - patch_preview: short preview string to show in UI
    - patch_content: dict { "target_files": path, "new_content": "..."}
    """

    # For simplicity, read demos/demo-app/fix/new_app_py.txt as the new file content
    fix_path = os.path.join(repo_path, "fix", "new_app_py.txt")
    with open(fix_path, "r", encoding="utf-8") as fh:
        new_content = fh.read()

    patch_files = {
        "target_file": "app.py"
        "new_content": new_content
    }

    # write patch json to a file a so sand_box can find can find it via Investigaton.path_file
    import tempfile, os
    base = os.environ.get("WORKSPACE_DIR") or os.path.join(os.path.dirname(__file__),"..","..","data", "workspaces")
    os.mkdirs(base, exist_ok=True)
    path_file = os.path.join(base, f"patch_incident_{incident.id}.json")
    with open(path_file, "w", encoding="utf-8") as fh:
        json.dump(patch_content, fh)

    preview = f"Replace {patch_content['target_file']} with fixed version (preview first 200 chars):\n\n" + new_content[:200]
    return {
        "root_cause": "off-by-one logic in the function causing test to return wrong value",
        "affected_files": [patch_content["target_file"]],
        "patch_file": patch_files,
        "patch_preview": preview,
        "patch_content": patch_content
    }