from fastapi import APIRouter


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/")
def hello_world() -> dict:
    return {"message": "Hello, World!"}
