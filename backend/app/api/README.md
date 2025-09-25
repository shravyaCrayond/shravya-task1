# FastAPI LangGraph Gemini Boilerplate
## Project Overview

This project is a **production-ready backend boilerplate** built using **FastAPI** and **LangGraph**, integrated with **Google Gemini models**.
It provides a **streaming chat API** with support for:
- Rate-limiting (Redis-based)
- CORS configuration
- Input validation using Pydantic
- PostgreSQL integration via SQLAlchemy
## Project Setup

### Backend
1. **Create and activate virtual environment**
python -m venv .venv
.venv\Scripts\Activate.ps1
* Windows PowerShell
2. **Install required packages**

```bash
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings
pip install -r requirements.txt
```
3. **Run FastAPI server**

```bash
uvicorn backend.app.main:app --reload
```
### To test in postman(extension installed in VScode):
CORS limited to post and get only , http://localhost:8000/v1/chat/stream use as url,
body -> raw -> text(json format)
{
    "prompt": "what is ai in 1sentence"
}
beautify->send -> response recieved. (data:{text:....}) format!!

### Frontend Setup (Vite + React) -- Optional

```bash
npm install
npm create vite@latest
npm run dev
```
### Git Setup

```bash
git init
git remote add origin <url>
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main
```
**Note:** To update credentials or fix SSH issues:
# when we have 2 github accounts in same device
```powershell
git credential-manager erase
type $env:USERPROFILE\.ssh\id_ed25519.pub
git remote set-url origin git@github.com:shravyaCrayond/shravya-task1.git
```
### Redis Setup (for Rate Limiting)
1. Install Redis
```bash
pip install fastapi-limiter redis
```
2. Start Redis server (two terminals):
```bash
redis-server
redis-cli ping
```
3. Test streaming endpoint with rate-limiting:
```bash
curl -X POST http://127.0.0.1:8000/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Test Redis"}'
```
**Note:** If you exceed the rate limit, you’ll get HTTP 429:
```json
{"detail":"Too Many Requests"}
```
## Configuration
Add a `.env` file with the following variables:
```env
DATABASE_URL=postgresql+asyncpg://postgres:admin@localhost:5432/mydb
REDIS_URL=redis://localhost:6379/0
GEMINI_API_KEY=<your_google_gemini_api_key>
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
RATE_LIMIT=5/minute
```
**Explanations:**
* `DATABASE_URL` → PostgreSQL connection string
* `REDIS_URL` → Redis server for rate-limiting
* `GEMINI_API_KEY` → Google Gemini API key
* `ALLOWED_ORIGINS` → CORS configuration (frontend URLs allowed)
* `RATE_LIMIT` → Requests per minute per IP
## Production Features
### CORS Configuration
* Ensures only your frontend domains can call the API
### Input Validation
* Pydantic ensures request fields are valid
* Enforces:
  * Required fields
  * String lengths
  * Optional `session_id`
* Todo improvements:
  * Regex validation for allowed characters
  * Max tokens for prompts
### Database Integration
* PostgreSQL database with SQLAlchemy
* Async or sync support via SQLAlchemy engine
* Models defined in `models.py`
* Database session managed in `session.py`


### ONESHOTT
# Quick Glance about its Adaption
* Install Redis latest download(https://github.com/microsoftarchive/redis/releases)
* Open CMD after extracting files from the folder
  ```bash
  C:\Users\yadav\Downloads\Redis-x64-3.0.504> .\redis-server.exe
  ```
* In another PowerShell:

  ```bash
  PS C:\Users\yadav\downloads\Redis-x64-3.0.504> .\redis-cli.exe
  ```
* Test Redis:
  ```bash
  127.0.0.1:6379> ping
  ```
  You should get **PONG** if correct.
* To test keys:

  ```bash
  keys *
  ```
  Should show:
  `"fastapi-limiter:127.0.0.1:/v1/chat/stream:4:0"` like this.
* In another CMD at random location, you can check for this:
  ```bash
  curl -X POST http://127.0.0.1:8000/v1/chat/stream \
       -H "Content-Type: application/json" \
       -d "{\"prompt\":\"Test Redis\"}"
  ```

  *(Rate limiting done)*
## Backend Setup
* Install required backend frameworks like **FastAPI**, and **Uvicorn**, with sample endpoint like `/health`.
* Test it with **POST** requests.
* Use **Postman** for checking API endpoints hitting, use the proper URL, provided above in the section.
* If you need UI, setup basic React:
  npm create vite@latest
  npm install
  npm run dev

* Run the dev server with using `backend_url` in frontend and render and return the components.
## Features Achieved

* Live streaming achieved
* CORS for efficient backend, only needs GET and POST (from docs)
* Pydantic models validation about the user prompt (min_len and max_len)
## IMPORTANT – DB Integration

* Install **PostgreSQL (pgAdmin)**
* Setup username, password, portNum-default (5432) and add in `.env`
* Create **database**, and a **table** with required attributes
* Add the model with the seq and route it accordingly

**Result:**
Now when entered query, (id, text, response, timestamp) that we made in frontend/in postman is effected in table (as we inserted in `models.py`)

Use:SELECT * FROM tab_name;
You can see changes modified!!
## ALL CATEGORIES MET!!!!
