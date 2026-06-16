# ONYX Cybersecurity Backend

A FastAPI backend for the ONYX cybersecurity module. This platform provides steganographic watermark embedding/extraction, tamper detection, and a traitor tracing system.

## Prerequisites

- Python 3.10+
- PostgreSQL Server

## Setup Instructions

1. **Configure the Database**
   Create a PostgreSQL database. You can use the default credentials defined in the `.env` file or update them to match your local setup:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/onyx
   ```
   *Note: The database tables will be auto-created when the application starts.*

2. **Install Dependencies**
   Navigate to the project directory and install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**
   Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
   The server will run at `http://127.0.0.1:8000`.

## API Endpoints

You can explore and test the endpoints directly using the auto-generated Swagger UI at `http://127.0.0.1:8000/docs`.

### 1. Steganography Watermarking
- **`POST /embed-watermark`**
  - **Inputs:** `image` (File), `signature` (Form string)
  - **Output:** Downloadable PNG image with the hidden LSB watermark.
- **`POST /extract-watermark`**
  - **Inputs:** `image` (File)
  - **Output:** JSON containing the hidden `watermark` text, or an error if none is found.

### 2. Tamper Detection
- **`POST /verify-integrity`**
  - **Inputs:** `original_image` (File), `suspect_image` (File)
  - **Output:** JSON detailing status (`AUTHENTIC` or `TAMPERED`). If tampered, provides a list of `tampered_regions` bounding box coordinates.

### 3. Traitor Tracing
- **`POST /generate-recipient-copy`**
  - **Inputs:** `image` (File), `recipient_name` (Form string), `signature` (Form string, optional)
  - **Output:** Downloadable uniquely watermarked PNG image. Also registers the recipient in the PostgreSQL database.
- **`POST /trace-leak`**
  - **Inputs:** `leaked_image` (File)
  - **Output:** JSON returning the `recipient_name` of the leaked copy if a match is found.
- **`GET /recipients`**
  - **Output:** JSON array of all registered recipients.
