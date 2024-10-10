from fastapi import Header, HTTPException


def get_headers(
    clientSlug: str = Header(default=None),
    clientId: str = Header(default=None),
    serviceId: str = Header(default=None),
    requestId: str = Header(default=None),
) -> dict:
    if not clientSlug:
        raise HTTPException(status_code=400, detail="Missing client-slug header")
    # Additional checks for other headers if needed
    return {
        "clientSlug": clientSlug,
        "clientId": clientId,
        "serviceId": serviceId,
        "requestId": requestId,
    }
