import os
from dotenv import load_dotenv
from webapp.posts import parse_posts_from_file
from webapp.mesh_pipeline import *
from webapp.meshy_api import *

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

posts = parse_posts_from_file("forum_posts.txt")


relevant_posts = filter_relevant_posts(posts)

print("Relevant posts:")
for post in relevant_posts:
    print(post["text"])
    if post["image"]:
        print(f"Image: {post['image']}")
    print()

meshy_prompts = generate_mesh_prompt(relevant_posts)

for prompt in meshy_prompts:
    print(prompt["prompt"])
    if prompt["image"]:
        image_path = os.path.join("images", prompt["image"])

        if os.path.isfile(image_path):
            print(f"✅ Image found: {prompt['image']} — sending to Meshy image-to-3D...")
            meshy_img_to_3d(prompt["image"])
        else:
            print(f"⚠️ Image file not found: {prompt['image']} — falling back to Meshy text-to-3D...")
            meshy_txt_to_3d(prompt["prompt"])
    else:
        print("ℹ️ No image present — sending to Meshy text-to-3D...")
        meshy_txt_to_3d(prompt["prompt"])
    





