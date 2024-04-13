import json
import os
import pandas as pd

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from .model import SemanticModel
from .parser_file import ParserFile

model_ = SemanticModel()
parser = ParserFile()

app = FastAPI()

# Allow requests from localhost:3000
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
        json_file_path = os.path.join(os.path.dirname(__file__), "../data.json")
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return JSONResponse(content=data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...), doctype: str = Form(...)):
    resp = {"files": {}}
    data = {'filename': [], 'text': []}
    try:
        for file in files:

            if file.filename.endswith(".txt"):
                contents = await parser.read_txt(file)

                data["filename"].append(file.filename)
                data["text"].append(contents)

            if file.filename.endswith(".rtf"):
                contents = await parser.read_rtf(file)

                data["filename"].append(file.filename)
                data["text"].append(contents)

            if file.filename.endswith(".pdf"):
                contents = await parser.read_pdf(file)

                data["filename"].append(file.filename)
                data["text"].append(contents)

            if file.filename.endswith(".xlsx"):
                contents = await parser.read_xlsx(file)

                data["filename"].append(file.filename)
                data["text"].append(contents)

            if file.filename.endswith(".docx"):
                contents = await parser.read_xlsx(file)

                data["filename"].append(file.filename)
                data["text"].append(contents)

        df_data = pd.DataFrame(data)
        res_data = model_.predict(df_data)

        for key, value in res_data.items():
            resp["files"][key] = {"category": f"{value}"}

        resp["status"] = "ok"

        return JSONResponse(content=resp, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Failed to upload files", "error": str(e)}, status_code=500)
