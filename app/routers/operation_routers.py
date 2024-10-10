import concurrent.futures
from app.db.config import template_get_uow
from fastapi import APIRouter, HTTPException, Depends, Request
from app.schemas.divide import DivideRequest, DivideResponse
from app.models.operations.divide import DivideOperation
from app.services.operation_service import OperationService
from app.utils.logger import JsonLogger
from app.dependencies import get_headers
from app.db.unitOfWork import UnitOfWork

router = APIRouter()


@router.post("/divide", tags=["operations"], response_model=DivideResponse)
def divide(
    request: DivideRequest,
    fastapi_request: Request,
    headers: dict = Depends(get_headers),
    template_uow: UnitOfWork = Depends(template_get_uow),
) -> dict:
    JsonLogger.log(
        level="INFO",
        message="Starting division",
        headers=headers,
        metadata={
            "endpoint": fastapi_request.url.path,
            "request": request.model_dump(),
        },
    )
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(OperationService.divide, request.a, request.b)
            try:
                result = future.result(timeout=10)  # Timeout after 10 seconds
            except concurrent.futures.TimeoutError:
                raise HTTPException(
                    status_code=504, detail="Task timed out after 10 seconds"
                )
            with template_uow as uow:
                operation = DivideOperation(
                    a=request.a, b=request.b, result=result.result
                )
                uow.operations_divide_repo.add(operation)
        response = DivideResponse(result=result.result)
        response_dict = response.model_dump()
        JsonLogger.log(
            level="INFO",
            message="Division completed",
            headers=headers,
            metadata={"endpoint": fastapi_request.url.path, "response": response_dict},
        )
        return response_dict
    except HTTPException as e:
        JsonLogger.log(
            level="ERROR",
            message="Error during division",
            headers=headers,
            metadata={"endpoint": fastapi_request.url.path, "error": str(e.detail)},
        )
        raise e
    except Exception as e:
        JsonLogger.log(
            level="ERROR",
            message="Unexpected error during division",
            headers=headers,
            metadata={"endpoint": fastapi_request.url.path, "error": str(e)},
        )
        raise HTTPException(status_code=500, detail="Unexpected error during division")
