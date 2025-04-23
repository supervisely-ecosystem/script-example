import json
import os
from time import perf_counter

import supervisely as sly
from dotenv import load_dotenv
from pympler import asizeof

DATA_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_DIR, exist_ok=True)
start = perf_counter()
print(f"Start time: {start:.2f} seconds")

# Ensure that supervisely.env contains SERVER_ADDRESS and API_TOKEN.
load_dotenv(os.path.expanduser("~/supervisely-demo.env"))
# Ensure that local.env contains TEAM_ID and WORKSPACE_ID.
load_dotenv("local.env")

team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()

api: sly.Api = sly.Api.from_env()

print(f"API instance created for team_id={team_id}, workspace_id={workspace_id}")

# Change this value to the project ID you want to work with.
project_id = 1514

# Change this value to the dataset ID you want to work with.
dataset_id = 3644

# Change this value to the video ID you want to work with.
video_id = 401553

# Obtaining list of all the figures without the actual geometry, because
# it's too heavy to download all the geometry at once.
figures_data = api.video.figure.download(
    dataset_id=dataset_id, video_ids=[video_id], skip_geometry=True
)

figures: list[sly.FigureInfo] = list(figures_data.values())[0]
print(f"The video contains {len(figures)} figures.")

# Split figures into batches.
# Change this value to the desired batch size.
BATCH_SIZE = 10

batch_idx = 0
for figures_batch in sly.batched(figures, batch_size=BATCH_SIZE):
    batch_start = perf_counter()
    # ! Debug information (can be removed):
    size_of_figures_wo_geometry = round(asizeof.asizeof(figures_batch) / 1024 / 1024, 3)
    print(
        f"Batch size: {len(figures_batch)}. "
        f"Size of figures without geometry: {size_of_figures_wo_geometry} MB"
    )

    # Process each batch of figures.
    # For example, you can print the figure IDs.
    figure_ids = [figure.id for figure in figures_batch]

    figures_with_geometry = api.video.figure.get_by_ids(
        dataset_id=dataset_id, ids=figure_ids
    )

    # ! Debug information (can be removed):
    size_of_figures_with_geometry = round(
        asizeof.asizeof(figures_with_geometry) / 1024 / 1024, 3
    )
    print(
        f"Batch size: {len(figures_with_geometry)}. "
        f"Size of figures with geometry   : {size_of_figures_with_geometry} MB"
    )

    # Convert figures to JSON format.
    json_batch = [figure.to_json() for figure in figures_with_geometry]

    # Save the JSON batch to a file.
    save_path = os.path.join(DATA_DIR, f"video_{video_id}_batch_{batch_idx}.json")
    with open(save_path, "w") as f:
        json.dump(json_batch, f, indent=4)
    print(f"Batch {batch_idx} saved to {save_path}")
    batch_idx += 1

    # Print the time taken for this batch.
    batch_end = perf_counter()
    batch_time = batch_end - batch_start
    print(f"Batch time: {batch_time:.2f} seconds")

end_time = perf_counter()
print(f"End time: {end_time:.2f} seconds")

# Print the total time taken for the script to run.
total_time = end_time - start
print(f"Total time: {total_time:.2f} seconds")
