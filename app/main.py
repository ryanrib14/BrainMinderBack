from .routers import demo_route, operation_routers
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(
    title="t4h-iag-template-server",
    version="1.0",
    description="template server for t4h-iag",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(demo_route.router)

app.include_router(operation_routers.router, prefix="/api/v1")
