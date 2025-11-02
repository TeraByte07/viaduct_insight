# 🚀 Viaduct Internal SaaS Platform

Viaduct Generation’s internal SaaS tool for consolidating research, SEO insights, and AI-driven workflows.  
The platform combines **FastAPI**, **PostgreSQL**, and **React** to support internal teams with data, automation, and smart insights.

---

## 🌟 Project Overview

**Goal:**  
To create a lightweight, scalable SaaS tool that helps Viaduct teams access:
- SEO metrics and insights (via APIs like SerpAPI, Moz, Ahrefs)
- Internal research and project notes
- Client benchmarks and competitor analysis
- AI-powered data insights for decision-making

**Key Objectives:**
- 🧩 **Centralized Platform** – Unified space for SEO and internal data.  
- 🤖 **AI-Powered Insights** – Integrations with tools like SerpAPI, Moz, Ahrefs.  
- 🏗️ **Scalability** – Built with clean MVC architecture.  
- ⚙️ **Automation** – Reduce repetitive SEO research and manual workflows.  
- 👥 **Collaboration** – Role-based access, shared dashboards, and reporting.

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | FastAPI (Python) |
| **Frontend** | React (planned) |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy + Alembic |
| **Auth** | JWT (Access + Refresh tokens) |
| **Integrations** | SerpAPI, Moz, Ahrefs (planned) |
| **Deployment** | AWS / Render / Railway (to be finalized) |

---

## 📁 Project Structure

viaduct/
├── app/
│ ├── core/ # Security, JWT, and config
│ ├── db/ # Database engine, session, and Alembic base
│ ├── models/ # SQLAlchemy models
│ ├── routes/ # API endpoints
│ ├── schemas/ # Pydantic models
│ ├── services/ # Business logic (e.g., SerpAPI service)
│ ├── utils/ # Helper modules (rate limiting, etc.)
│ └── main.py # FastAPI entry point
├── alembic/ # Alembic migrations
├── .env # Environment variables
├── requirements.txt
└── README.md


---

## 🔐 Authentication Flow

- **Register:** Create a user with email & password  
- **Login:** Get access + refresh tokens  
- **Logout:** Blacklist active token  
- **Refresh Token:** Request new access token  
- (optional) **Verify Email:** Coming soon  

Anonymous users can still test limited endpoints (e.g. `/analysis/serp`) up to **3 times per day**.

---

## Domain Analysis (SerpAPI Integration)

**Endpoint:**  
`POST /analysis/serp`

**Request Body:**
json
{
  "query": "site:ahrefs.com"
}

## Running the Project
1) Clone and Setup-
git clone https://github.com/TeraByte07/viaduct-insight.git

cd viaduct-insight

python -m venv venv

venv\Scripts\activate(Windows)
or
source venv/bin/activate (Mac/Linux)

2) Install Dependencies

pip install -r requirements.txt

4) Setup an environment(create a .env file in the project root folder)with the following as variables

DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/viaduct

SECRET_KEY=your_jwt_secret

SERP_API_KEY=your_serpapi_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7

4) Run migrations

alembic upgrade head

6) Start FastAPI

uvicorn app.main:app --reload

Open in browser:
➡️ http://127.0.0.1:8000/

Current Features
✅ User Registration & Login
✅ Logout & Token Blacklisting
✅ Token Refresh
✅ Domain Analysis (SerpAPI)
✅ Rate Limiting for Anonymous Users
🚧 Email Verification (coming soon)
🚧 Dashboard & Reporting (next phase)

Authors
Viaduct Generation Internal Dev Team
Backend: FastAPI · Database: PostgreSQL · Integration: SerpAPI


