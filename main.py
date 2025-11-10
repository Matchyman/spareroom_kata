from fastapi import FastAPI

from src.checkout import checkoutRouter

app = FastAPI()

app.include_router(checkoutRouter.router)

@app.get("/")
def root():
    return {"message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)