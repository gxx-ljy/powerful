from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

# @app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"D:/codes/files/{filename}"
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return FileResponse(file_path, media_type='application/octet-stream', filename=filename)


app.get("/download/{filename}")(download_file)
# http://ip:8001/download/content1.pdf

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
