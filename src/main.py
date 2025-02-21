import os
from random import randint
from time import perf_counter
from typing import List, Tuple

import supervisely as sly
from dotenv import load_dotenv
from tqdm import tqdm

# Ensure that supervisely.env contains SERVER_ADDRESS and API_TOKEN.
load_dotenv(os.path.expanduser("~/supervisely-dev.env"))
# Ensure that local.env contains TEAM_ID and WORKSPACE_ID.
load_dotenv("local.env")

team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
project_id = sly.env.project_id()
dataset_id = sly.env.dataset_id()

api: sly.Api = sly.Api.from_env()

video_project_name = api.project.get_info_by_id(project_id).name

print(
    f"API instance created for team_id={team_id}, workspace_id={workspace_id}, "
    f"project_id={project_id}, dataset_id={dataset_id}"
)

start_time = perf_counter()
videos = api.video.get_list(dataset_id, recursive=True)
got_videos_time = perf_counter() - start_time
print(f"Videos count: {len(videos)} in {got_videos_time:.2f} sec.")


def get_quarters(count: int) -> List[Tuple[int, int]]:
    quarter = count // 4
    return [
        (0, quarter),
        (quarter + 1, 2 * quarter),
        (2 * quarter + 1, 3 * quarter),
        (3 * quarter + 1, count),
    ]


new_images_project_name = "MP: Images Sample for Detection Task"
project_info = api.project.get_info_by_name(workspace_id, new_images_project_name)
if project_info is not None:
    api.project.remove(project_info.id)
    print(f"Project {new_images_project_name} already exists. Removing it.")

project_info = api.project.create(workspace_id, new_images_project_name)
print(f"Project {new_images_project_name} created.")

dataset_info = api.dataset.create(project_info.id, "ds0")

for video in tqdm(videos, desc="Iterating over videos", unit="video"):
    video_dataset_name = api.dataset.get_info_by_id(video.dataset_id).name
    quarters = get_quarters(video.frames_count)

    for min_idx, max_idx in quarters:
        random_quarter_idx = randint(min_idx, max_idx)

        # Get frame as numpy array.
        frame_np = api.video.frame.download_np(video.id, random_quarter_idx)

        custom_data = {
            "original_project_id": project_id,
            "original_project_name": video_project_name,
            "original_dataset_id": video.dataset_id,
            "original_dataset_name": video_dataset_name,
            "original_video_id": video.id,
            "original_video_name": video.name,
            "original_frame_index": random_quarter_idx,
        }

        # Upload image to the new project from the numpy array.
        image_name = f"{video_dataset_name}_{video.name}_{random_quarter_idx}.png"
        new_image_info = api.image.upload_np(
            dataset_info.id, image_name, frame_np, meta=custom_data
        )
