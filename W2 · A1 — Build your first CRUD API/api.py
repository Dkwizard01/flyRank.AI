import fastapi
app = fastapi.FastAPI()

# Stage 0: hello server
# @app.get("/")
# async def hello_server():
  #  return {"status_code": "200", "message": "Hello World"}
@app.get("/")
async def root():
   return  { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }
@app.get("/health")
async def health():
   return { "status": "ok" } 
