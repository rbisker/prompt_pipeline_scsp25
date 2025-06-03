import os
os.environ["OPENAI_API_KEY"] = "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" 

from posts import parse_posts_from_file
from mesh_pipeline import *



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




