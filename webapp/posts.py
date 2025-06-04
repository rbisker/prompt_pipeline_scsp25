import re

def parse_posts_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split into posts by double newlines
    raw_posts = [p.strip() for p in content.split("\n\n") if p.strip()]
    
    structured_posts = []
    for post in raw_posts:
        # Look for image filename in format: (Image: filename.jpg)
        match = re.search(r"\(Image:\s*([^\)]+\.jpg)\)", post, re.IGNORECASE)
        image_filename = match.group(1).strip() if match else None
        
        # Remove the image reference from the post text
        clean_text = re.sub(r"\(Image:\s*[^\)]+\)", "", post).strip()
        
        structured_posts.append({
            "text": clean_text,
            "image": image_filename
        })
    
    return structured_posts


if __name__ == "__main__":
    posts = parse_posts_from_file("forum_posts.txt")
    for post in posts:
        print(post["text"])
        if post["image"]:
            print(f"Image: {post['image']}")
        print()