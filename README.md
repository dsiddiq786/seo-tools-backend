# SEO Tools Backend

This project is a comprehensive backend for SEO tools, designed with FastAPI, PostgreSQL, and several advanced libraries to support efficient and scalable API services. The backend provides endpoints for various SEO-related functionalities, including keyword analysis, content optimization, image tools, and more.

---

## Features

- **FastAPI**: High-performance API framework.
- **PostgreSQL**: Relational database for structured data management.
- **MongoDB**: (Optional) For semi-structured or unstructured data.
- **Natural Language Processing**: Powered by spaCy and nltk.
- **Image Tools**: Tools for resizing, conversion, and metadata extraction.
- **Utility Tools**: Including QR code generation, password management, and minification tools.
- **Dockerized Deployment**: Easily deployable with Docker and Railway.

---

## Prerequisites

Make sure the following are installed on your system:

- **Python**: Version 3.9 or higher.
- **PostgreSQL**: For database operations.
- **Git**: For version control.
- **Docker**: For containerized deployment.
- **Railway Account**: For cloud hosting (optional).

---

## Setup Instructions

### Local Setup

#### Step 1: Clone the Repository

```bash
git clone https://github.com/dsiddiq786/seo-tools-backend.git
cd seo-tools-backend
```

#### Step 2: Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # For Windows: venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Configure the Database

1. Create a PostgreSQL database.
2. Update the `.env` file with your database connection string:

   ```env
   DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>
   ```

#### Step 5: Download Required NLP Models and Data

Install necessary models for spaCy and nltk:

```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt')"
python -m textblob.download_corpora
```

#### Step 6: Run the Application

Start the server:

```bash
uvicorn app.main:app --reload
```

Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

### Dockerized Setup

#### Step 1: Build and Run the Docker Container

1. Build the Docker image:

   ```bash
   docker build -t seo-tools-backend .
   ```

2. Run the container:

   ```bash
   docker run -d -p 8000:8000 --env-file .env seo-tools-backend
   ```

#### Step 2: Access the Application

Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

### Deployment on Railway

1. Login to Railway:

   ```bash
   railway login
   ```

2. Link the project:

   ```bash
   railway init
   ```

3. Set environment variables in the Railway dashboard:

   - `DATABASE_URL`
   - `REDIS_URL` (if required)

4. Deploy:

   ```bash
   railway up
   ```

---

## Project Structure

```plaintext
seo-tools-backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── tools/
│   │   │   │   │   ├── text_analysis.py
│   │   │   │   │   ├── keyword_analysis.py
│   │   │   │   │   └── ...
│   │   │   ├── routers.py
│   │   │   └── schemas/
│   ├── core/
│   ├── db/
│   │   ├── models/
│   │   ├── migrations/
│   │   └── session.py
│   ├── main.py
│   └── tests/
├── config/
│   ├── dev.env
│   ├── prod.env
│   └── test.env
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Tools Developed

### Text Tools

- Text Analysis
- Readability Suggestions
- Grammar Checker
- Content Rephraser

### SEO Tools

- Meta Tag Generator
- Keyword Analysis
- Keyword Finder

### Utility Tools

- QR Code Generator
- Robots.txt Generator
- Open Graph Generator
- JSON Validator
- XML to JSON Converter

### Image Tools

- Image Resizer
- Favicon Generator
- Image Metadata Extractor

---

## Commands for Model Downloads

Here are the commands to download and install required models and dependencies:

### spaCy

```bash
python -m spacy download en_core_web_sm
```

### NLTK

```bash
python -c "import nltk; nltk.download('punkt')"
```
wget https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx

### TextBlob:

```bash
python -m textblob.download_corpora
```

## Dependencies

The project relies on the following libraries:

- **FastAPI**: For building APIs.
- **SQLAlchemy**: For database ORM.
- **Pillow**: For image processing.
- **spaCy**: For natural language processing.
- **nltk**: For additional NLP tasks.
- **Pytest**: For testing.

Install them via `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
