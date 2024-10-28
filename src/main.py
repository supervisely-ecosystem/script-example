import os
from time import perf_counter

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

project_id = 42517
local_dir = "saved"
if os.path.exists(local_dir):
    sly.fs.remove_dir(local_dir)
    print(f"Directory {local_dir} was removed")


project_info = api.project.get_info_by_id(project_id)

project_size_in_bytes = project_info.size
project_size_in_mb = round(int(project_size_in_bytes) / 1000 / 1000, 2)
number_of_images = project_info.images_count
print(f"Project size: {project_size_in_mb} Mb, number of images: {number_of_images}")

download_start = perf_counter()
sly.Project.download(api, project_id, local_dir)
download_end = perf_counter()

elapsed_time = download_end - download_start
print(f"Downloaded in {elapsed_time} seconds")
print(f"Download speed: {round(project_size_in_mb/elapsed_time, 2, )} Mb/s")
