from fastapi import FastAPI

from src.checkout import checkout_router

app = FastAPI()

app.include_router(checkout_router.router)

@app.get("/")
def root():
    return {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)