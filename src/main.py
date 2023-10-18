import os

import supervisely as sly

from dotenv import load_dotenv
from rich.console import Console

console = Console()

console.log("Script starting...")

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ABSOLUTE_PATH)
console.log(f"Absolute path: {ABSOLUTE_PATH}\nParent dir: {PARENT_DIR}")

if sly.is_development():
    # * For convinient development, has no effect in the production.
    local_env_path = os.path.join(PARENT_DIR, "local.env")
    supervisely_env_path = os.path.expanduser("~/supervisely.env")
    console.log(
        "Running in development mode. Will load .env files...\n"
        f"Local .env path: {local_env_path}, Supervisely .env path: {supervisely_env_path}"
    )

    if os.path.exists(local_env_path) and os.path.exists(supervisely_env_path):
        console.log("Both .env files exists. Will load them.")
        load_dotenv(local_env_path)
        load_dotenv(supervisely_env_path)
    else:
        console.log("One of the .env files is missing. It may cause errors.")

TEAM_ID = sly.io.env.team_id()
WORKSPACE_ID = sly.io.env.workspace_id()
console.log(f"TEAM_ID: {TEAM_ID}, WORKSPACE_ID: {WORKSPACE_ID}")

api: sly.Api = sly.Api.from_env()

console.log("API instance initialized.")
