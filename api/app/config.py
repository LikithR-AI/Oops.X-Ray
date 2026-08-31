import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", os.path.join(BASE_DIR, "data", "uploads"))
WORKSPACES_DIR = os.environ.get("WORKSPACE_DIR", os.path.join(BASE_DIR, "data", "workspaces"))
LLM_MODE = os.environ.get("LLM_MODE", "mock") #'Mock' or 'real'