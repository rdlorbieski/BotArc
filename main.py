from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/status")
def status():
    return {"message": "API funcionando"}


# @app.post("/process-message/")
# def process_message(message: str):
#     agent = SpecialistAgent("suporte ao cliente")
#     response = agent.process_message(message)
#     return {"response": response}
