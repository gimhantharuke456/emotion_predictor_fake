from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
import requests
import datetime
import tensorflow as tf
import gc
import uvicorn
app = FastAPI()

# Set up CORS to allow requests from all origins
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


def analyze_emotion(filename):
    emotions = DeepFace.analyze(filename)
    emotion = emotions[0]['dominant_emotion']
    print(f"emotion is {emotion}")
    return emotion


@app.get("/test")
def test():
    return {"message": "helloworld"}


@app.post("/predict")
async def predict_image(request: dict):
    try:
        image_url = request["url"]
        response = requests.get(image_url)
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"image_{current_time}.jpg"

        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print("Image downloaded successfully.")
        else:
            print("Failed to download image. Status code:", response.status_code)
            return {"error": "Failed to download image"}, 500

        emotion = analyze_emotion(filename)

        # Clear TensorFlow session
        DeepFace.close_session()

        gc.collect()  # Perform garbage collection

        # Remove the downloaded image
        import os
        os.remove(filename)

        return {"emotion": emotion}
    except Exception as e:
        return {"error": f"Error while predicting emotion: {str(e)}"}, 500


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
