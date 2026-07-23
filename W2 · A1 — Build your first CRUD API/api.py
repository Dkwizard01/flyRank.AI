import fastapi
app = fastapi.FastAPI()


@app.get("/")
async def hello_server():
    return {"status_code": "200", "message": "Hello World"}
