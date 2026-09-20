# 🏟️ Exam Arena

> **AI-Powered Exam Analytics Platform** — Predict. Prepare. Excel.

Exam Arena analyses 12+ years of historical exam papers through mathematical regression and AI to predict which topics will appear next. Heatmaps, AI predictions, mock exams & dynamic study planner.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React + Vite + TailwindCSS |
| **Backend** | FastAPI (Python) |
| **Database** | Amazon RDS (PostgreSQL) |
| **AI** | Gemini API + Strands Agents SDK |
| **Auth** | Amazon Cognito |
| **Storage** | Amazon S3 |
| **Compute** | AWS Lambda + API Gateway (SAM) |
| **Hosting** | AWS Amplify |
| **Monitoring** | Amazon CloudWatch |
| **Async** | Amazon SQS |

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.12+
- AWS CLI configured
- SAM CLI installed

### Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env  # Fill in your credentials
SEED_DB=true uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
cp .env.example .env  # Set VITE_API_BASE
npm run dev
```

## 📄 License

MIT
