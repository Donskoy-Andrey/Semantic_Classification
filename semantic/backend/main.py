import os
import time

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import tempfile

app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.post("/handle_image")
async def process_image(file: UploadFile = File(...)):
    try:
        # Read the uploaded image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        time.sleep(2)

        # Process the image (Example: Convert to grayscale)
        grayscale_image = image.convert('L')

        # Save the processed image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            grayscale_image.save(temp_file, format="JPEG")

        # Return the processed image as a response
        return FileResponse(temp_file.name, media_type="image/jpeg")

    except Exception as e:
        return {"error": str(e)}

@app.post("/handle_example")
async def process_example(data: dict):
    print("handle example")
    print(data)
    action = data.get("name")
    print(f"{action=}")

    try:
        # Check if action is specified and equals "first"
        if action == "first":
            # Read the image file
            image_path = ali.pngos.path.join(os.path.dirname(__file__), "ali.png")
            image = Image.open(image_path)
            time.sleep(2)

            # Process the image (Example: Convert to grayscale)
            grayscale_image = image.convert('L')

            # Save the processed image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                grayscale_image.save(temp_file, format="JPEG")

            # Return the processed image as a response
            print("return file")
            return FileResponse(temp_file.name, media_type="image/jpeg")
        else:
            return {"error": "Action not recognized or no action provided."}

    except Exception as e:
        print("exception")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
