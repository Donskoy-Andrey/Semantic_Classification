import os
import json
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .model import SemanticModel
from .parser_file import ParserFile

model_ = SemanticModel()
parser = ParserFile()

app = FastAPI()

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


@app.post("/update_template")
async def update_template(request: dict):
    try:
        json_file_path = os.path.join("/app/data.json")
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if len(request['categories']) == 0:
            return HTTPException(status_code=500, detail={'error': "Вы не выбрали категории"})

        new_key = 'custom_key_'
        numeric_ending = 0
        for key in data:
            if request['name'] == data[key]["name"]:
                return HTTPException(status_code=500, detail={'error': f"Имя {request['name']} уже существует!"})

            if new_key + str(numeric_ending) in data:
                numeric_ending += 1

        new_key = 'custom_key_' + str(numeric_ending)

        new_value = {
            'name': request['name'],
            'categories': request['categories'],
            'docs_number': len(request['categories'])
        }
        data[new_key] = new_value
        with open(json_file_path, "w", encoding="utf-8") as file:
            json.dump(data, file)
        return JSONResponse(content=data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail={'error': str(e)})


@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...), doctype: str = Form(...)):
    resp = {"files": {}}
    data = {'filename': [], 'text': []}
    try:
        for file in files:
            print(file.filename)

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
                contents = await parser.read_docx(file)

                data["filename"].append(file.filename)
                data["text"].append(contents)

        # Parse json
        json_file_path = os.path.join(os.path.dirname(__file__), "/app/data.json")
        with open(json_file_path, "r", encoding="utf-8") as file:
            json_file = json.load(file)
        cats = json_file[doctype]['categories']
        cats = {cat: 1 for cat in cats}
        print('6')

        df_data = pd.DataFrame(data)
        res_data = model_.predict(df_data)
        print('7')

        total_status = True
        for filename, category in res_data.items():
            if category not in cats:
                resp["files"][filename] = {
                    "category": mapping[category],
                    "valid_type": f"Неожиданная категория, ожидалась категория из списка: "
                                  f"[{', '.join([mapping[i] for i in cats.keys()])}]",
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
        print('8')

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
                {'category': mapping['arrangement'], "valid_type": "Правильный документ"},
            'bill.rtf':
                {'category': mapping['bill'], "valid_type": "Правильный документ"},
            'bill_another.rtf':
                {'category': mapping['bill'], "valid_type": "Лишний документ"}
        },
            'status': 'bad'
        }
    elif name == "second":
        res = {'files': {
            'soglasie.rtf':
                {'category': mapping['arrangement'], "valid_type": "Правильный документ"},
            'bill.rtf':
                {'category': mapping['bill'], "valid_type": "Правильный документ"},
            'order.rtf':
                {'category': mapping['order'], "valid_type": "Правильный документ"}
        },
            'status': 'ok'
        }
    else:
        return JSONResponse(content={"message": "Failed to upload files", "error": "wrong format"}, status_code=500)

    return JSONResponse(content=res, status_code=200)
