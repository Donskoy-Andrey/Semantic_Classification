import os
import json
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .model import SemanticModel

model_ = SemanticModel()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/form_params")
async def read_json_file():
    try:
        json_file_path = os.path.join(os.path.dirname(__file__), "/app/data.json")
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return JSONResponse(content=data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...), doctype: str = Form(...)):
    try:
        resp = {"files": {}}
        data = {'filename': [], 'text': []}
        for file in files:
            if file.filename.split(".")[-1] == "txt":
                contents = await file.read()
                data["filename"].append(file.filename)
                data["text"].append(contents.decode("utf-8"))

        # Parse json
        json_file_path = os.path.join(os.path.dirname(__file__), "/app/data.json")
        with open(json_file_path, "r", encoding="utf-8") as file:
            json_file = json.load(file)
        cats = json_file[doctype]['categories']
        cats = {cat: 1 for cat in cats}

        df_data = pd.DataFrame(data)
        res_data = model_.predict(df_data)

        total_status = True
        for filename, category in res_data.items():
            if category not in cats:
                resp["files"][filename] = {"category": category, "valid_type": "Неожиданная категория"}
                total_status = False
            elif cats[category] == 1:
                resp["files"][filename] = {"category": category, "valid_type": "Правильный документ"}
                cats[category] -= 1
            else:
                resp["files"][filename] = {"category": category, "valid_type": "Лишний документ"}
                total_status = False

        # resp : {'files': {'1.txt': {'category': 'application'}}}

        if total_status is True:
            resp["status"] = "ok"
        else:
            resp["status"] = "bad"

        return JSONResponse(content=resp, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Failed to upload files", "error": str(e)}, status_code=500)


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
