# 📄 Smart Legal Document Manager

> A Flask REST API that helps lawyers track, compare, and manage changes in legal documents — with full version history, line-by-line diffing, and smart background notifications.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-stdlib-003B57?style=flat&logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-36%20passing-2ea44f?style=flat)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat)

---

## ✨ Features

- **Immutable versioning** — every edit creates a new version; old content is never overwritten
- **Full audit trail** — author and timestamp recorded automatically on every save
- **Line-by-line diff** — compare any two versions with `equal`, `insert`, `delete`, `replace` tags
- **Smart notifications** — background thread fires alerts only for meaningful changes (not whitespace)
- **Metadata management** — update the document title without creating a new version
- **Soft deletes** — remove a single version or an entire document without destroying the database record

---

## 🛠 Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| Framework | Flask 3 | WSGI web framework |
| Database | SQLite (`sqlite3`) | Python stdlib, WAL mode, zero config |
| Diff Engine | `difflib` | Python stdlib `SequenceMatcher` |
| Notifications | `threading` | Daemon threads, fire-and-forget |
| Testing | `unittest` | Stdlib runner + Flask test client |

> **Zero external dependencies beyond Flask.** `pip install flask` is all you need.

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/legal-doc-manager.git
cd legal-doc-manager
```

### 2. Install the dependency

```bash
pip install flask
```

### 3. Run the server

```bash
python run.py
```

Server starts at `http://127.0.0.1:5000`

### 4. Run the tests

```bash
python -m unittest discover tests -v
# Ran 36 tests ... OK
```

---

## 📁 Project Structure

```
legal_doc_manager/
├── run.py                   # Entrypoint
├── requirements.txt
├── app/
│   ├── database.py          # SQLite connection management (thread-local)
│   ├── repository.py        # All SQL queries — no ORM
│   ├── diff_engine.py       # Line-by-line diff + significance check
│   ├── notifications.py     # Background notification dispatch
│   └── routes.py            # All Flask routes
└── tests/
    └── test_api.py          # 36 integration tests
```

---

## 📡 API Reference

### Documents

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/documents/` | Create a document + initial version |
| `GET` | `/documents/` | List all documents |
| `GET` | `/documents/<id>` | Get document with full version history |
| `PATCH` | `/documents/<id>` | Update title only — no new version created |
| `DELETE` | `/documents/<id>` | Soft-delete the entire document |

### Versions

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/documents/<id>/versions` | Save a new immutable version |
| `GET` | `/documents/<id>/versions` | List all version summaries |
| `GET` | `/documents/<id>/versions/<n>` | Get a specific version with full content |
| `DELETE` | `/documents/<id>/versions/<n>` | Soft-delete one version (history preserved) |

### Diff

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/documents/<id>/diff?from_version=1&to_version=2` | Compare two versions line-by-line |

---

## 🔍 Diff Example

```bash
GET /documents/1/diff?from_version=1&to_version=2
```

```json
{
  "document_id": 1,
  "from_version": 1,
  "to_version": 2,
  "is_significant": true,
  "similarity_ratio": 0.72,
  "hunks": [
    { "tag": "equal",   "before": "Party A agrees to pay.",       "after": "Party A agrees to pay."       },
    { "tag": "replace", "before": "Amount: $5,000.",              "after": "Amount: $10,000."             },
    { "tag": "delete",  "before": "Payment due in 30 days.",      "after": null                           },
    { "tag": "insert",  "before": null,                           "after": "Payment due in 14 days."      },
    { "tag": "insert",  "before": null,                           "after": "Late fees apply after 14 days." }
  ]
}
```

| Tag | Meaning |
|---|---|
| `equal` | Line unchanged |
| `insert` | Line added in the new version |
| `delete` | Line removed from the old version |
| `replace` | Line changed — before and after shown side-by-side |

---

## 🔔 Smart Notifications

Notifications fire in a **background thread** — the API always returns `201` immediately.

| Change Type | Similarity Ratio | Notification |
|---|---|---|
| Trailing whitespace added | ≥ 0.95 | ❌ Suppressed |
| Clause rewritten | < 0.95 | ✅ Sent |
| Entirely new document | 0.0 | ✅ Sent |

The threshold is configurable in `app/diff_engine.py`:

```python
SIGNIFICANCE_THRESHOLD = 0.95
```

To plug in real email delivery, replace the stub in `app/notifications.py`:

```python
def _send_email(...):
    # Replace with smtplib / SendGrid / AWS SES
    ...
```

---

## 🧪 Tests

```
36 tests across 4 groups — all passing

Shape 1 — Versioning        10 tests   create, increment, immutability, audit trail
Shape 2 — Diff              10 tests   insert/delete/replace detection, similarity, errors
Shape 3 — Notifications      5 tests   non-blocking response, significance thresholds
Shape 4 — Doc Management    11 tests   title update, soft-delete, version isolation, 404s
```

---

## 💡 Usage Examples

### Create a document

```bash
curl -X POST http://localhost:5000/documents/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "NDA Agreement",
    "created_by": "alice",
    "content": "Party A agrees to maintain confidentiality.\nThis agreement is valid for 2 years."
  }'
```

### Save a new version

```bash
curl -X POST http://localhost:5000/documents/1/versions \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Party A agrees to maintain strict confidentiality.\nThis agreement is valid for 5 years.",
    "saved_by": "bob",
    "change_summary": "Extended term to 5 years"
  }'
```

### Compare versions

```bash
curl "http://localhost:5000/documents/1/diff?from_version=1&to_version=2"
```

### Update title only (no new version)

```bash
curl -X PATCH http://localhost:5000/documents/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "NDA Agreement — Final"}'
```

### Windows PowerShell

```powershell
Invoke-WebRequest -Uri http://localhost:5000/documents/ `
  -Method POST -ContentType "application/json" `
  -Body '{"title": "NDA Agreement", "created_by": "alice", "content": "Party A agrees..."}'
```

---

## 🗺 Roadmap

- [ ] Web UI with visual diff viewer
- [ ] JWT authentication and role-based access control
- [ ] Real email delivery (SMTP / SendGrid / SES)
- [ ] Full-text search and document tagging
- [ ] PostgreSQL support for production deployments
- [ ] OpenAPI / Swagger documentation

---

## 👤 Author

**Krishna** — Project, 2026
