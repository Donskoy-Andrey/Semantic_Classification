import json
import os

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
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


@app.post("/handle_example")
async def handle_example(request: dict):
    if "name" not in request:
        return JSONResponse(content={"message": "Failed to upload files", "error": "wrong format"}, status_code=500)
    name = request["name"]
    if name == "first":

        res = {'files': {
            'soglasie.rtf':
                {'category': 'agreement'},
            'bill.rtf':
                {'category': 'bill'},
            'bill_another.rtf':
                {'category': 'bill'}
        },
            'status': 'bad'
        }
    elif name == "second":
        res = {'files': {
            'soglasie.rtf':
                {'category': 'agreement'},
            'bill.rtf':
                {'category': 'bill'},
            'order.rtf':
                {'category': 'order'}
        },
            'status': 'ok'
        }
    else:
        return JSONResponse(content={"message": "Failed to upload files", "error": "wrong format"}, status_code=500)

    return JSONResponse(content=res, status_code=200)



@app.get("/form_params")
async def read_json_file():
    try:
        json_file_path = os.path.join(os.path.dirname(__file__), "../data.json")
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            print(f"{data}")
        return JSONResponse(content=data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...), doctype: str = Form(...)):
    try:
        print(f"{doctype=}")
        total_files = len(files)
        files_uploaded = 0
        resp = {"files": {}}

        for file in files:
            contents = await file.read()

            # Do something with the file contents, such as saving it to disk or processing it
            # For example, to save it to disk:
            # with open(file.filename, "wb") as f:
            #     f.write(contents)
            print(f"{file.filename=}")

            resp["files"][file.filename] = {"category": f"category_{files_uploaded}"}
            files_uploaded += 1

            # Simulate processing asynchronously
            await simulate_processing()
        resp["status"] = "bad"
        print(f"{resp=}")

        return JSONResponse(content=resp, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Failed to upload files", "error": str(e)}, status_code=500)
