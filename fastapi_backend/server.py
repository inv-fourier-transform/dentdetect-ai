from fastapi import FastAPI, File, UploadFile
from model_helper import predict_damage

app = FastAPI()

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

@app.post("/upload")
async def obtain_prediction(file: UploadFile = File(...)): # FastAPI has in-built PyDantic model validation

    try:
        image_bytes = await file.read() # Async programming in Python

        image_path = "temp_file.jpg"

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        damage_prediction = predict_damage(image_path)
        return {"Prediction": damage_prediction}

    except Exception as e:
        return {"error": str(e)}


