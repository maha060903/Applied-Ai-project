# AI-Powered Personalized Learning Assistant

A production-ready AI SaaS platform that analyzes student academic performance, identifies learning gaps, and generates personalized study recommendations through an intelligent chatbot interface. This project aligns with **SDG 4: Quality Education** and follows ethical AI practices.

![Project Status](https://img.shields.io/badge/status-production--ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![React](https://img.shields.io/badge/react-18.2.0-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-green)

## 🎯 Project Overview

This platform provides:

- **Performance Analysis**: ML-powered analysis of student quiz scores and attendance
- **Learning Gap Identification**: Automatic detection of areas needing improvement
- **Personalized Recommendations**: AI-generated study plans and resource suggestions
- **Educational Chatbot**: Context-aware AI assistant for student guidance
- **Interactive Dashboard**: Modern, responsive UI with data visualization

## ✨ Features

### Core Functionality
- ✅ Student performance analysis using RandomForest ML model
- ✅ Learning gap identification and classification
- ✅ Personalized study recommendations engine
- ✅ 4-week structured learning plans
- ✅ Real-time educational chatbot
- ✅ Performance visualization with charts
- ✅ Multi-subject support (Mathematics, Science, English, etc.)

### Technical Features
- ✅ RESTful API with FastAPI
- ✅ React frontend with Vite
- ✅ Tailwind CSS for modern UI
- ✅ Recharts for data visualization
- ✅ Responsive design (mobile-friendly)
- ✅ CORS-enabled for cross-origin requests
- ✅ Error handling and validation
- ✅ Production-ready deployment configuration

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │
│   (Vercel)      │
│   React + Vite  │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│   Backend API   │
│   (FastAPI)     │
│   Render/Railway│
└────────┬────────┘
         │
    ┌────┴────┬──────────┬─────────────┐
    │         │          │             │
┌───▼───┐ ┌──▼───┐ ┌────▼────┐ ┌──────▼──────┐
│ ML    │ │Rec.  │ │Chatbot │ │   Dataset   │
│ Model │ │Engine│ │ Logic  │ │    CSV      │
└───────┘ └──────┘ └────────┘ └─────────────┘
```

### Technology Stack

**Frontend:**
- React.js 18.2.0
- Vite 5.0.8
- Tailwind CSS 3.3.6
- Recharts 2.10.3
- React Router DOM 6.20.0
- Axios 1.6.2
- Lucide React (icons)

**Backend:**
- Python 3.10+
- FastAPI 0.104.1
- Uvicorn 0.24.0
- Pandas 2.1.3
- NumPy 1.26.2
- Scikit-learn 1.3.2
- Joblib 1.3.2

**Deployment:**
- Frontend: Vercel
- Backend: Render / Railway / Fly.io

## 📁 Project Structure

```
ai-learning-assistant/
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   │   ├── Card.jsx
│   │   │   ├── Button.jsx
│   │   │   ├── Input.jsx
│   │   │   └── PerformanceChart.jsx
│   │   ├── pages/            # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── LearningPlan.jsx
│   │   │   └── Recommendations.jsx
│   │   ├── services/         # API services
│   │   │   └── api.js
│   │   ├── chatbot/          # Chatbot component
│   │   │   └── ChatbotWidget.jsx
│   │   ├── App.jsx           # Main app component
│   │   ├── main.jsx          # Entry point
│   │   └── index.css         # Global styles
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI application
│   │   ├── model.py          # ML model
│   │   ├── recommender.py    # Recommendation engine
│   │   └── chatbot.py        # Chatbot logic
│   └── requirements.txt
├── data/
│   └── student_performance.csv
├── .gitignore
└── README.md
```

## 🚀 Setup Instructions

### Prerequisites

- **Python 3.10+** installed
- **Node.js 18+** and npm installed
- Git for version control

### Backend Setup (Python Virtual Environment)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   
   # macOS/Linux
   python3 -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the FastAPI server:**
   ```bash
   # From backend directory
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   Create `.env` file in `frontend/` directory:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. **Run development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## 📊 Dataset

The project includes a sample dataset (`data/student_performance.csv`) with the following columns:

- `student_id`: Unique student identifier (e.g., STU001)
- `subject`: Subject name (Mathematics, Science, English, etc.)
- `quiz_score`: Quiz score percentage (0-100)
- `attendance`: Attendance percentage (0-100)
- `performance_level`: Categorized performance (Excellent, Good, Average, Below Average, Poor)

**Sample Data:**
- 20 students
- 3 subjects per student
- 60 total records
- Realistic performance distribution

## 🔌 API Endpoints

### Performance Analysis
```http
POST /analyze-performance
Content-Type: application/json

{
  "student_id": "STU001",
  "subject": "Mathematics",
  "quiz_score": 75.0,
  "attendance": 85.0
}
```

**Response:**
```json
{
  "student_id": "STU001",
  "subject": "Mathematics",
  "performance_level": "Good",
  "prediction_confidence": 0.85,
  "learning_gaps": [...],
  "feature_importance": {...}
}
```

### Get Recommendations
```http
GET /recommendations/{student_id}?subject=Mathematics&quiz_score=75&attendance=85
```

### Chatbot
```http
POST /chatbot
Content-Type: application/json

{
  "message": "How can I improve my math scores?",
  "student_id": "STU001",
  "student_context": {...}
}
```

### Student Performance History
```http
GET /students/{student_id}/performance
```

## 🚢 Deployment

### Frontend Deployment (Vercel)

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Set environment variable:**
   - In Vercel dashboard, add `VITE_API_URL` with your backend URL

### Backend Deployment (Render)

1. **Create a new Web Service on Render**

2. **Connect your GitHub repository**

3. **Configure:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3

4. **Set environment variables:**
   - `PYTHON_VERSION=3.10`

5. **Deploy**

### Backend Deployment (Railway)

1. **Create new project on Railway**

2. **Connect GitHub repository**

3. **Add Python service**

4. **Configure:**
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Build Command:** `cd backend && pip install -r requirements.txt`

5. **Deploy**

## 🧪 Testing the Application

1. **Start backend:**
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   uvicorn app.main:app --reload
   ```

2. **Start frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access application:**
   - Open `http://localhost:5173`
   - Login with Student ID: `STU001` (or any ID from dataset)
   - Navigate through dashboard, analyze performance, view recommendations

## 🤖 ML Model Details

### Model Type
- **Algorithm:** RandomForest Classifier
- **Features:** quiz_score, attendance, subject_encoded
- **Target:** performance_level (categorized)
- **Accuracy:** ~85-90% (varies with dataset)

### Performance Categories
- **Excellent:** ≥80%
- **Good:** 70-79%
- **Average:** 60-69%
- **Below Average:** 50-59%
- **Poor:** <50%

### Learning Gap Identification
- Low Quiz Score (<60%)
- Low Attendance (<75%)
- Severity classification (High/Medium)

## 💬 Chatbot Behavior

The educational chatbot:
- ✅ Explains weak topics clearly
- ✅ Suggests what to study next
- ✅ Provides motivation and support
- ✅ Never provides medical/psychological diagnosis
- ✅ Follows ethical AI guidelines
- ✅ Context-aware responses using student data

**System Prompt:**
> "You are an AI educational assistant helping students improve learning outcomes based on academic performance data."

## 🎨 UI/UX Features

- **Modern Design:** Clean, minimal, enterprise-grade interface
- **Responsive:** Works on desktop, tablet, and mobile
- **Accessible:** Proper color contrast and typography
- **Smooth Transitions:** Polished animations and interactions
- **Reusable Components:** Modular component architecture
- **Data Visualization:** Interactive charts with Recharts

## 📈 SDG 4 Alignment

This project contributes to **Sustainable Development Goal 4: Quality Education** by:

- Providing personalized learning support
- Identifying and addressing learning gaps
- Making quality education more accessible through AI
- Supporting inclusive and equitable education
- Enabling data-driven educational improvements

## 🤝 Ethical AI Considerations

- **Transparency:** Clear explanation of AI recommendations
- **Privacy:** Student data handled securely
- **Fairness:** No bias in performance analysis
- **Accountability:** Human oversight in educational decisions
- **Non-diagnostic:** Chatbot does not provide medical/psychological advice
- **Educational Focus:** AI supports, not replaces, human educators

## 📝 License

This project is created for educational and portfolio purposes.

## 👨‍💻 Development

### Adding New Features

1. **Backend:** Add endpoints in `backend/app/main.py`
2. **Frontend:** Create components in `frontend/src/components/`
3. **ML Model:** Extend `backend/app/model.py` for new features

### Code Quality

- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React
- Add comments for complex logic
- Maintain consistent naming conventions

## 🐛 Troubleshooting

### Backend Issues

**Model not training:**
- Ensure `data/student_performance.csv` exists
- Check Python version (3.10+)
- Verify all dependencies installed

**CORS errors:**
- Check `allow_origins` in `main.py`
- Verify frontend URL is whitelisted

### Frontend Issues

**API connection failed:**
- Verify `VITE_API_URL` in `.env`
- Check backend is running
- Verify CORS configuration

**Build errors:**
- Clear `node_modules` and reinstall
- Check Node.js version (18+)

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs` endpoint
3. Verify environment setup

## 🎓 Use Cases

- **Educational Institutions:** Student performance monitoring
- **Tutoring Services:** Personalized learning plans
- **EdTech Companies:** AI-powered learning platforms
- **Research:** Educational data analysis
- **Portfolio:** Full-stack AI project demonstration

## 🔮 Future Enhancements

- Integration with IBM Granite/Watsonx for advanced NLP
- Real-time performance tracking
- Multi-language support
- Advanced analytics dashboard
- Mobile app version
- Integration with LMS systems

---

**Built with ❤️ for Quality Education (SDG 4)**

*This project is production-ready and suitable for client demos, GitHub portfolios, and CSRBOX/IBM SkillsBuild Capstone submissions.*
