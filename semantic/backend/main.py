import io
import json
import os
import pandas as pd

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from striprtf.striprtf import rtf_to_text

from PyPDF2 import PdfReader

from .model import SemanticModel


model_ = SemanticModel()

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
                contents = await file.read()
                data["filename"].append(file.filename)
                data["text"].append(contents.decode("utf-8"))

            if file.filename.endswith(".rtf"):
                contents = await file.read()
                text_rtf = contents.decode('UTF-8')
                extracted_text = rtf_to_text(text_rtf)
                data["filename"].append(file.filename)
                data["text"].append(extracted_text)

            if file.filename.endswith(".pdf"):
                contents = await file.read()
                pdf_reader = PdfReader(io.BytesIO(contents))
                extracted_text = ''
                for page in pdf_reader.pages:
                    extracted_text += page.extract_text()

                data["filename"].append(file.filename)
                data["text"].append(extracted_text)


        df_data = pd.DataFrame(data)
        res_data = model_.predict(df_data)

        for key, value in res_data.items():
            resp["files"][key] = {"category": f"{value}"}

        resp["status"] = "ok"

        return JSONResponse(content=resp, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Failed to upload files", "error": str(e)}, status_code=500)
