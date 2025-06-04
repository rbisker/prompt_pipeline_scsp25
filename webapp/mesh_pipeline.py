from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

filter_prompt = PromptTemplate(
    input_variables=["post"],
    template="""
You are an analyst reviewing military field reports.

Determine if the post below is about a drone or counter-UAS system.

Post:
"{post}"

Respond with only "yes" or "no".
"""
)

mesh_prompt_template = PromptTemplate(
    input_variables=["post"],
    template="""
You are generating a 3D modeling prompt for a game engine.

From the following military field report, extract a clear, concise description of a drone or anti-drone system suitable for 3D model generation.

Post:
"{post}"

Respond with just the description, like:
"a quadcopter drone with four rotors, a thermal camera, and blinking IR strobes"
"""
)

llm = ChatOpenAI(model="gpt-4o", temperature=0)
relevance_chain = filter_prompt | llm  # This creates a RunnableSequence

def filter_relevant_posts(posts):
    relevant = []
    for post in posts:
        response = relevance_chain.invoke({"post": post["text"]}).content.strip().lower()
        if response == "yes":
            relevant.append(post)
    return relevant

mesh_prompt_chain = mesh_prompt_template | llm

def generate_mesh_prompt(posts):
    prompts = []
    for post in posts:
        result = mesh_prompt_chain.invoke({"post": post["text"]})
        prompt_text = result.content.strip()

        prompts.append({
            "prompt": prompt_text,
            "image": post.get("image")  # Carry over the image if available
        })

    return prompts
