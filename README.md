# 📄 Smart Legal Document Manager

A backend system for lawyers and legal teams to **track, version, and compare legal documents** with full audit trails. Every change is preserved — nothing is ever overwritten.

---

## ✨ Features

- **Document Versioning** — Every edit creates a new version with author, timestamp, and version number
- **Version Comparison (Diff)** — Compare any two versions with clear added/removed line highlighting
- **Smart Notifications** — Background alerts on meaningful content changes (ignores whitespace)
- **Metadata Management** — Update titles, delete specific versions, or remove documents entirely
- **Non-Destructive Editing** — Complete audit trail for legal compliance

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Language | Python 3.10+ |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Task Queue | Celery |
| Message Broker | Redis |
| Server | Uvicorn |

---

## 📁 Project Structure

```
smart-legal-doc-manager/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── diff_utils.py
│   ├── notification.py
│   ├── celery_worker.py
│   └── tasks.py
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Krishna31m/smart-legal-doc-manager.git
cd smart-legal-doc-manager
```

### 2. Create & Activate a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄 Database Setup

1. Install PostgreSQL and open the shell:

```bash
psql -U postgres
```

2. Create the database:

```sql
CREATE DATABASE legal_docs;
\q
```

3. Configure the connection in `app/database.py`:

```python
DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/legal_docs"
```

> **Note:** Special characters in passwords must be URL-encoded (e.g., `@` → `%40`)

---

## ▶️ Running the Application

**Start the FastAPI server:**

```bash
uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Interactive Docs: `http://127.0.0.1:8000/docs`

**Start the background worker (in a separate terminal):**

```bash
# Start Redis
redis-server

# Start Celery
celery -A app.tasks worker --loglevel=info
```

---

## 📡 API Endpoints

### Create a Document
```http
POST /documents
```
```json
{
  "title": "Employment Contract",
  "content": "Payment must be made within 30 days.",
  "user": "krishna"
}
```

### Upload a New Version
```http
POST /documents/{document_id}/versions
```
```json
{
  "content": "Payment must be made within 45 days.",
  "user": "krishna"
}
```

### Compare Two Versions
```http
GET /documents/{document_id}/compare?v1=1&v2=2
```
```diff
- Payment must be made within 30 days.
+ Payment must be made within 45 days.
```

### Update Document Title
```http
PATCH /documents/{document_id}
```
```json
{
  "title": "Updated Contract Title"
}
```

### Delete a Specific Version
```http
DELETE /documents/{document_id}/versions/{version}
```

### Delete a Document
```http
DELETE /documents/{document_id}
```

---

## 🔄 Example Workflow

```
1. POST   /documents                          → Create document
2. POST   /documents/{id}/versions            → Upload revised version
3. GET    /documents/{id}/compare?v1=1&v2=2   → Review changes
4. PATCH  /documents/{id}                     → Update title if needed
5. DELETE /documents/{id}/versions/{version}  → Remove a specific version
```

---

## 👨‍💻 Author

**Krishna** —  Project  
Smart Legal Document Manager
