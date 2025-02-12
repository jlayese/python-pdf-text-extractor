from fastapi import FastAPI, File, UploadFile
import fitz
from io import BytesIO
import logging

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return {"error": "Only PDF files are allowed."}

    try:
        pdf_data = BytesIO(await file.read())
        document = fitz.open(stream=pdf_data, filetype="pdf")

        extracted_text = ""
        for page in document:
            extracted_text += page.get_text() + "\n"

        return {"text": extracted_text.strip()}

    except Exception as e:
        logging.error(f"Error: {e}")
        return {"error": str(e)}


# python -m uvicorn api:app --reload