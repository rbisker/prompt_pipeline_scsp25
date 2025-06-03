import os
from dotenv import load_dotenv
from posts import parse_posts_from_file
from mesh_pipeline import *

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


posts = parse_posts_from_file("forum_posts.txt")

relevant_posts = filter_relevant_posts(posts)

for post in relevant_posts:
    print(post["text"])
    if post["image"]:
        print(f"Image: {post['image']}")
    print()

meshy_prompts = generate_mesh_prompt(relevant_posts)

for prompt in meshy_prompts:
    print(prompt["prompt"])
    if prompt["image"]:
        print(f"Image: {prompt['image']}")




