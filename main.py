from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import csv
import json
import os

app = FastAPI()

def make_json(csv_file, json_file):
    data = []
    with open(csv_file, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)
        for row in csv_reader:
            data.append(row)
    with open(json_file, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/convert_csv_to_json")
async def convert_csv_to_json(csv_file: UploadFile = File(...)):
    if not allowed_file(csv_file.filename):
        return JSONResponse(content={"error": "Invalid file format. Only CSV files are allowed."}, status_code=400)
    
    try:
        with open(csv_file.filename, 'wb') as f:
            f.write(csv_file.file.read())

        json_filename = f"{csv_file.filename.rsplit('.', 1)[0]}.json"
        make_json(csv_file.filename, json_filename)
        
        # Return the JSON file as a response
        with open(json_filename, 'r') as json_file:
            json_data = json_file.read()
        
        os.remove(csv_file.filename)
        os.remove(json_filename)

        return JSONResponse(content=json_data)
    
    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {str(e)}"}, status_code=500)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=6969, host='0.0.0.0')

