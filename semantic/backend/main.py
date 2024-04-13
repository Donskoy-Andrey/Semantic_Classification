import os
import json
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .model import SemanticModel
from .parser_file import ParserFile



app = FastAPI()

model_ = SemanticModel()
parser = ParserFile()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

mapping = {
    "proxy": "Доверенность",
    "contract": "Договор",
    "act": "Акт",
    "application": "Заявление",
    "order": "Приказ",
    "invoice": "Счет",
    "bill": "Приложение",
    "arrangement": "Соглашение",
    "contract offer": "Договор оферты",
    "statute": "Устав",
    "determination": "Решение",
}


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
    resp = {"files": {}}
    data = {'filename': [], 'text': []}
    try:
        for file in files:
            if file.filename.endswith(".txt"):
                contents = parser.read_txt(file)

                data["filename"].append(file.filename)
                data["text"].append(contents)

            if file.filename.endswith(".rtf"):
                contents = parser.read_rtf(file)
                data["filename"].append(file.filename)
                data["text"].append(contents)

            if file.filename.endswith(".pdf"):
                contents = parser.read_pdf(file)
                data["filename"].append(file.filename)
                data["text"].append(contents)

            if file.filename.endswith(".xlsx"):
                contents = parser.read_xlsx(file)
                data["filename"].append(file.filename)
                data["text"].append(contents)

            if file.filename.endswith(".docx"):
                print(file.filename)
                contents = parser.read_docx(file)
                print(file.filename)
                data["filename"].append(file.filename)
                data["text"].append(contents)

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
                    resp["files"][filename] = {
                        "category": mapping[category],
                        "valid_type": f"Неожиданная категория, ожидалась категория из списка: {cats}",
                    }
                    total_status = False
                elif cats[category] == 1:
                    resp["files"][filename] = {
                        "category": mapping[category],
                        "valid_type": "Правильный документ",
                    }
                    cats[category] -= 1
                else:
                    resp["files"][filename] = {
                        "category": mapping[category],
                        "valid_type": "Лишний документ",
                    }
                    total_status = False

            # resp : {'files': {'1.txt': {'category': 'application'}}}

            if total_status is True:
                resp["status"] = "ok"
            else:
                resp["status"] = "bad"

            return JSONResponse(content=resp, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Failed to upload files", "error": str(e)}, status_code=500)


@app.post("/handle_example")
async def handle_example(request: dict):
    if "name" not in request:
        return JSONResponse(content={"message": "Failed to upload files", "error": "wrong format"}, status_code=500)
    name = request["name"]
    if name == "first":

        res = {'files': {
            'soglasie.rtf':
                {'category': mapping['arrangement']},
            'bill.rtf':
                {'category': mapping['bill']},
            'bill_another.rtf':
                {'category': mapping['bill']}
        },
            'status': 'bad'
        }
    elif name == "second":
        res = {'files': {
            'soglasie.rtf':
                {'category': mapping['arrangement']},
            'bill.rtf':
                {'category': mapping['bill']},
            'order.rtf':
                {'category': mapping['order']}
        },
            'status': 'ok'
        }
    else:
        return JSONResponse(content={"message": "Failed to upload files", "error": "wrong format"}, status_code=500)

    return JSONResponse(content=res, status_code=200)
