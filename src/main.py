import os

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

dataset_A = 93739
dataset_B = 93740

images_A = api.image.get_list(dataset_A)
print(f"Found {len(images_A)} images in dataset_A")
images_B = api.image.get_list(dataset_B)
print(f"Found {len(images_B)} images in dataset_B")

not_in_B = []
not_in_A = []
matched = []
unmatched = []

images_A_dict = {image.name: image for image in images_A}
images_B_dict = {image.name: image for image in images_B}

for name, image_A in images_A_dict.items():
    if name in images_B_dict:
        image_B = images_B_dict[name]
        if image_A.hash == image_B.hash:
            matched.append(image_A)
        else:
            unmatched.append(image_A)
            print(f"Unmatched: {image_A.name}")
        del images_B_dict[name]
    else:
        not_in_B.append(image_A)

not_in_A.extend(images_B_dict.values())

md_file = "comparison.md"

sly.ImageInfo.preview_url

with open(md_file, "w") as f:
    f.write("# Comparison\n")
    f.write(f"## ✅ Matched ({len(matched)})\n")
    for image in matched:
        f.write(f"- [{image.name}]({image.preview_url})\n")
    f.write(f"## ⛔️ Unmatched ({len(unmatched)})\n")
    for image in unmatched:
        f.write(f"- [{image.name}]({image.preview_url})\n")
    f.write(f"## 🅰️ Only exists in dataset A ({len(not_in_B)})\n")
    for image in not_in_B:
        f.write(f"- [{image.name}]({image.preview_url})\n")
    f.write(f"## 🅱️ Only exists in dataset B ({len(not_in_A)})\n")
    for image in not_in_A:
        f.write(f"- [{image.name}]({image.preview_url})\n")
