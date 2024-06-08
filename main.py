from fastapi import FastAPI
from joblib import load
from assets.preprocessing import TextPreprocessor  # Assuming preprocess is a custom module you've created
from datetime import datetime
from pyprojroot import here

app = FastAPI()

# Load your model
model = load(here('model/SVM_v1.0.0.joblib'))
classes = ['anger', 'fear', 'happy', 'love', 'sadness']

# Define a global uncertainty threshold
uncertainty_threshold = 0.5  # Adjust as needed

@app.get("/predict-teks")
async def predict(text: str):
    # Membuat instance TextPreprocessor dengan teks yang diberikan
    preprocessor = TextPreprocessor(text)
    # Memanggil metode text_preprocessing pada instance preprocessor
    vector = preprocessor.text_preprocess
    probs = model.predict_proba(vector)[0]  # Get prediction probabilities
    
    # Determine the index of the maximum probability (predicted class)
    pred_index = probs.argmax()
    prediction = classes[pred_index]
    confidence = probs[pred_index]
    
    # Determine if the prediction is uncertain
    is_uncertain = confidence < uncertainty_threshold
    is_uncertain = bool(is_uncertain)  # Explicit conversion to Python bool
    
    # Get the current timestamp and format it
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        "text": text,
        "prediction": prediction,
        "confidence": float(confidence),  # Convert to Python float for JSON serialization
        "is_uncertain": is_uncertain,
        "timestamp": timestamp  # Include the formatted timestamp in the response
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)