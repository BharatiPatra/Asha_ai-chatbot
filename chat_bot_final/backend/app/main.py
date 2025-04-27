import os
import uvicorn
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat

app = FastAPI()

origins = [
    "http://localhost:5173",  # your Vite dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(chat.router, prefix="/api")



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

if __name__ == "__main__":
    # Get the port from the environment variable, default to 8000 if not set
    port = int(os.environ.get("PORT", 8000))
    
    # Run the Uvicorn app with the correct host and port
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
