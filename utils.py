from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

app = FastAPI()


@app.exception_handler(201)
async def custom_201_exception_handler(request, exc):
    return JSONResponse(content={"message": "Resource created successfully"}, status_code=201)


@app.exception_handler(200)
async def custom_200_exception_handler(request, exc):
    return JSONResponse(content={"message": "Request successful"}, status_code=200)


@app.exception_handler(404)
async def custom_404_exception_handler(request, exc):
    return JSONResponse(content={"message": "Resource not found"}, status_code=404)


@app.exception_handler(500)
async def custom_500_exception_handler(request, exc):
    return JSONResponse(content={"message": "Server Error"}, status_code=500)


