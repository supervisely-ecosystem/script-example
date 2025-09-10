import json
import os
from typing import Dict

import supervisely as sly
from dotenv import load_dotenv

# Ensure that supervisely.env contains SERVER_ADDRESS and API_TOKEN.
load_dotenv(os.path.expanduser("~/supervisely-prod.env"))
# Ensure that local.env contains TEAM_ID and WORKSPACE_ID.
load_dotenv("local.env")

team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()

api: sly.Api = sly.Api.from_env()

print(f"API instance created for team_id={team_id}, workspace_id={workspace_id}")

project_id = sly.env.project_id()
dataset_id = sly.env.dataset_id()
video_id = os.getenv("VIDEO_ID", None)
if video_id is not None:
    video_id = int(video_id)
else:
    raise ValueError("VIDEO_ID environment variable is not set.")
print(f"Project ID: {project_id}, Dataset ID: {dataset_id}, Video ID: {video_id}")

video_info = api.video.get_info_by_id(video_id)
if not video_info:
    raise ValueError(f"Video with ID {video_id} not found.")
print(f"Video name: {video_info.name}, Video ID: {video_info.id}")

project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))


def tags_duration_to_json(
    api: sly.Api, project_meta: sly.ProjectMeta, video_id: int
) -> Dict[str, int]:
    """
    Count frames for each tag on the video and return a dictionary with tag names and frame counts.
    """
    # Get video annotations (tags)
    video_ann_json = api.video.annotation.download(video_id)
    video_ann = sly.VideoAnnotation.from_json(video_ann_json, project_meta)

    # Dictionary to store tag frame counts
    tag_frame_counts = {}

    # Iterate through all tags in the video annotation
    for tag in video_ann.tags:
        tag_name = tag.meta.name

        # Initialize count for this tag if not exists
        if tag_name not in tag_frame_counts:
            tag_frame_counts[tag_name] = 0

        # Count frames for this tag
        if tag.frame_range is not None:
            # Tag has a frame range
            start_frame = tag.frame_range[0]
            end_frame = tag.frame_range[1]
            frame_count = end_frame - start_frame + 1
            tag_frame_counts[tag_name] += frame_count
        else:
            # Tag applies to single frame or entire video
            tag_frame_counts[tag_name] += 1

    # Print results in the requested format
    print("\nTag frame counts:")
    for tag_name, count in tag_frame_counts.items():
        print(f"{tag_name}: {count}")

    return tag_frame_counts


# Call the function to get tag frame counts
if __name__ == "__main__":
    tag_counts = tags_duration_to_json(api, project_meta, video_id)
    saved_path = "tag_frame_counts.json"
    with open(saved_path, "w") as f:
        json.dump(tag_counts, f, indent=4)
    print(f"\nTag frame counts saved to {saved_path}")
