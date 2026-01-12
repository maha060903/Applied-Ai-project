# Backend API - AI Learning Assistant

FastAPI backend for the AI-Powered Personalized Learning Assistant.

## Quick Start

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Production Deployment

For Render/Railway deployment, use:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Environment Variables

No environment variables required for basic setup. The dataset path is configured to use `../data/student_performance.csv`.
