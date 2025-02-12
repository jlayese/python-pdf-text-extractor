import requests
from io import BytesIO
import fitz

def handler(pd: "pipedream"):
    # Step 1: Receive the uploaded file
    if "file" not in pd.steps["trigger"]["event"]["body"]:
        pd.respond({
            "status": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": {"error": "No file uploaded"}
        })
        return
    
    file = pd.steps["trigger"]["event"]["body"]["file"]
    
    # Step 2: Check if the file is a PDF
    if file["mimetype"] != "application/pdf":
        pd.respond({
            "status": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": {"error": "Only PDF files are allowed."}
        })
        return
    
    try:
        # Step 3: Get the file content
        response = requests.get(file["url"])
        response.raise_for_status()  # Ensure we catch HTTP errors
        pdf_data = BytesIO(response.content)
        
        # Step 4: Extract text from the PDF
        document = fitz.open(stream=pdf_data, filetype="pdf")
        
        extracted_text = ""
        for page in document:
            extracted_text += page.get_text() + "\n"
        
        # Step 5: Return the extracted text
        pd.respond({
            "status": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": {"text": extracted_text.strip()}
        })
    
    except Exception as e:
        # Step 6: Handle errors
        pd.respond({
            "status": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": {"error": str(e)}
        })
