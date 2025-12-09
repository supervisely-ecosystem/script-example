# supervisely==6.73.482

import os
import sys

import supervisely as sly
from dotenv import load_dotenv


# Ensure that supervisely.env contains SERVER_ADDRESS and API_TOKEN.
load_dotenv(os.path.expanduser("~/supervisely.env"))
# Ensure that local.env contains TEAM_ID and WORKSPACE_ID.
load_dotenv("local.env")


team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()

api: sly.Api = sly.Api.from_env()

print(f"API instance created for team_id={team_id}, workspace_id={workspace_id}")

# Enter all figure_ids to restore.
figure_ids = [
    18638233,
    # 12345678,
    # 23456789,
]

# ===== RESTORE ONLY THE FIRST FIGURE =====
test_figure_id = figure_ids[0]

print(f"Restoring only the first figure id={test_figure_id}")
# Figure must be archived to restore it.
api.image.figure.restore_batch([test_figure_id])
print(
    "Figure restored. Check in the interface, that everything is ok.\n"
    "When you are sure, delete this block (before sys.exit), "
    "to enable batch restoration."
)
sys.exit(0)
# ========================================


# ===== BATCH MODE: RESTORE ALL FIGURES =====
print(f"Restoring {len(figure_ids)} figures.")
api.image.figure.restore_batch(figure_ids)
print("All specified figures have been restored.")
# ===========================================
