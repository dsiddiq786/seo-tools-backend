# SEO Tools Backend

This is a backend project for SEO tools, built with FastAPI, PostgreSQL, and spaCy. It provides API endpoints for various SEO analysis features.

---

## Features

- FastAPI-based backend
- PostgreSQL for database management
- spaCy for natural language processing
- Dockerized deployment

---

## Prerequisites

Ensure you have the following installed:

- Python 3.9+
- PostgreSQL
- Git
- Railway account (for deployment)

---

## Setup Instructions

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dsiddiq786/seo-tools-backend.git
   cd seo-tools-backend
   Install dependencies:
   ```

```python
pip install -r requirements.txt
```

Set up the database:

Create a PostgreSQL database.

```python
Update the DATABASE_URL in .env or config.py with your database connection string.
```

Download spaCy model and nltk kit:

```python
python -m spacy download en_core_web_sm && python -c "import nltk; nltk.download('punkt'"

```

Run the project:

```python
uvicorn main:app --reload
```
