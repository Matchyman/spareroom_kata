from fastapi import FastAPI
import uvicorn
import sys
from src.checkout import checkoutRouter

app = FastAPI()

app.include_router(checkoutRouter.router)

@app.get("/")
def root():
    return {"message": "API is running"}

def main(args = ""):
    if args == "prod":
        uvicorn.run("main:app", host="localhost", port=8000, reload=True, log_config="config\prod_log_conf.yml")
    else:
        uvicorn.run("main:app", host="localhost", port=8000, reload=True, log_config="config\dev_log_conf.yml")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        main(arg)
    main()