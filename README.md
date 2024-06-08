# Project Overview

This project aims to predict emotions in text using a Support Vector Machine (SVM) model. The model is trained on a dataset of labeled text samples representing different emotions such as anger, fear, happiness, love, and sadness.

## Model Version

SVM_v1.0.0

## Data Version

The dataset used to train the model is version 1.0.0.

# How to Set Up

Follow these steps to set up the project:

1. Clone this repository to your local machine:
```bash
git clone <repository_url>
```
2. Navigate to the project directory:
```bash
cd <project_directory>
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```


# How to Run

To run the application, follow these steps:

1. Navigate to the project directory if you haven't already:
```bash
cd <project_directory>
```
2. Run the FastAPI application using Uvicorn:
```bash
uvicorn main
--host=0.0.0.0 --port=8000
```
3. Once the application is running, you can access the API at `http://localhost:8000`.

4. Use the `/predict-teks` endpoint to make predictions on text samples. Send a GET request with the text you want to analyze, for example:

```bash
curl -X 'GET' \
  'http://localhost:8000/predict-teks?text=Ini%20adalah%20contoh%20teks%20yang%20ingin%20dianalisis' \
  -H 'accept: application/json'
```

Replace Ini%20adalah%20contoh%20teks%20yang%20ingin%20dianalisis with your desired text.



