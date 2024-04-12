from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

# Allow requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


async def simulate_processing():
    # Simulate processing by waiting for 1 second
    await asyncio.sleep(1)

@app.get("/")
async def main():
    return JSONResponse({"message": "hello world"})


@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...), doctype: str = Form(...)):
    try:
        print(f"{doctype=}")
        total_files = len(files)
        files_uploaded = 0

        for file in files:
            contents = await file.read()
            # Do something with the file contents, such as saving it to disk or processing it
            # For example, to save it to disk:
            # with open(file.filename, "wb") as f:
            #     f.write(contents)
            print(f"{file.filename=}")

            files_uploaded += 1

            # Simulate processing asynchronously
            await simulate_processing()

        return JSONResponse(content={"message": "Files uploaded successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Failed to upload files", "error": str(e)}, status_code=500)
