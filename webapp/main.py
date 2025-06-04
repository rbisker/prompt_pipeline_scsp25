from fastapi import FastAPI, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from posts import parse_posts_from_file
from mesh_pipeline import filter_relevant_posts, generate_mesh_prompt

import os
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, file: UploadFile):
    contents = await file.read()
    filename = f"uploads/{uuid.uuid4().hex}_{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    with open(filename, "wb") as f:
        f.write(contents)

    posts = parse_posts_from_file(filename)
    relevant_posts = filter_relevant_posts(posts)
    prompts = generate_mesh_prompt(relevant_posts)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "all_posts": posts,
        "relevant_posts": relevant_posts,
        "prompts": prompts
    })

@app.get("/reset")
async def reset():
    return RedirectResponse(url="/", status_code=302)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)