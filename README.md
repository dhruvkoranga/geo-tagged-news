# GeoTaggedNews

This project is a FastAPI application that scrapes news articles based on keywords, processes them to extract locations, and provides an API to retrieve articles by location.

## Setup

1. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
3. **Download spacy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running the Application

### 1. Run the API Server

   ```bash
   uvicorn app.main:app --reload
   ```

   The API server will be running at `http://127.0.0.1:8000`.

### 2. Run the Worker

   In a separate terminal, run the following command to start the worker:

   ```bash
   python -m app.worker
   ```

   The worker will start scraping articles based on the keywords.

## API Usage

### Add a keyword

   ```bash
   curl -X POST "http://127.0.0.1:8000/keywords?value=london" -H "accept: application/json" -d ""
   ```

### List active keywords

   ```bash
   curl -X GET "http://127.0.0.1:8000/keywords" -H "accept: application/json"
   ```

### Get articles by location

   ```bash
   curl -X GET "http://127.0.0.1:8000/articles/by-location?location=london" -H "accept: application/json"
   ```
