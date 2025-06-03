import os
import requests
import base64
import time
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("MESHY_API_KEY")
print("Loaded API key:", os.getenv("MESHY_API_KEY"))
headers = {"Authorization": f"Bearer {api_key}"}

# --- Send prompt to text-to-3d endpoint ---
def meshy_txt_to_3d(prompt):
    payload = {
        "mode": "preview",
        "prompt": prompt,
        "art_style": "realistic",
        "should_remesh": False,
        "symmetry_mode": "auto",
        "ai_model": "meshy-5",
        }
    
    preview_response = requests.post(
        "https://api.meshy.ai/openapi/v2/text-to-3d",
        headers=headers,
        json=payload,
    )

    preview_response.raise_for_status()
    preview_task_id = preview_response.json()["result"]
    print("Preview task created. Task ID:", preview_task_id)

    # Poll preview task statsu until finished
    preview_task = None

    while True:
        preview_task_response = requests.get(
            f"https://api.meshy.ai/openapi/v2/text-to-3d/{preview_task_id}",
            headers=headers,
        )

        preview_task_response.raise_for_status()
        preview_task = preview_task_response.json()

        if preview_task["status"] == "SUCCEEDED":
            print("Preview task completed.")
            break

        print("Preview task status:", preview_task["status"], "| Progress:", preview_task["progress"], "| Retrying in 5 seconds...")
        time.sleep(5)

    # Download preview model in obj format
    preview_model_url = preview_task["model_urls"]["obj"]
    preview_model_response = requests.get(preview_model_url)
    preview_model_response.raise_for_status()

    with open("drone_from_txt.obj", "wb") as f:
        f.write(preview_model_response.content)

    print("Preview model downloaded as drone_from_txt.obj")


def image_to_data_uri(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"


def meshy_img_to_3d(image):

        # --- Send image to image-to-3d endpoint ---
        image_path = os.path.join("images", image)  #change to actual image path
        data_uri = image_to_data_uri(image_path)

        payload = {
            "image_url": data_uri,
            "enable_pbr": False,  # Generates PBR maps (metallic, roughness, etc.)
            "should_remesh": False,  #Enable to use target_polycount and topology
            "should_texture": False,
            "ai_model": "meshy-5",
            "symmetry_mode": "auto",
        }

        response = requests.post(
            "https://api.meshy.ai/openapi/v1/image-to-3d",
            headers=headers,
            json=payload
        )

        response.raise_for_status()
        task_id = response.json()["result"]
        print("Task created. Task ID:", task_id)

        # Poll task status until finished

        while True:
            task_response = requests.get(
                f"https://api.meshy.ai/openapi/v1/image-to-3d/{task_id}",
                headers=headers,
            )

            task_response.raise_for_status()
            task = task_response.json()

            if task["status"] == "SUCCEEDED":
                print("Image to 3D task completed.")
                break

            print("Task status:", task["status"], "| Progress:", task["progress"], "| Retrying in 5 seconds...")
            time.sleep(5)

        # Download model in obj format
        model_url = task["model_urls"]["obj"]
        model_response = requests.get(model_url)

        with open("drone_from_img.obj", "wb") as f:
            f.write(model_response.content)

        print("Model downloaded as drone_from_img.obj")

    
if __name__ == "__main__":
    meshy_txt_to_3d("a UAS drone with four propellors")
    meshy_img_to_3d("quad_drone.jpg")


