# AI YouTube Shorts Generator

A Django API that takes a YouTube URL, automatically generates a vertical short highlight video, uploads it to Cloudinary, and stores the information in Supabase.

## Features

- Extract the most engaging parts of a YouTube video
- Automatically create a short vertical video format (9:16 aspect ratio)
- Upload the generated short to Cloudinary
- Store video information in Supabase database
- Track processing status with a RESTful API

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd AI-Youtube-Shorts-Generator
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:

```
OPENAI_API_KEY=your_openai_api_key

# Cloudinary credentials
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Supabase credentials
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SUPABASE_TABLE=shorts

# Redis URL for Celery
REDIS_URL=redis://localhost:6379/0
```

4. Install and start Redis:

```bash
# Install Redis (MacOS)
brew install redis

# Install Redis (Ubuntu)
sudo apt-get install redis-server

# Install Redis (Windows)
# Option 1: Using Windows Subsystem for Linux (WSL) - Recommended
# Install WSL: https://learn.microsoft.com/en-us/windows/wsl/install
# Then install Redis in WSL:
sudo apt-get update
sudo apt-get install redis-server
sudo service redis-server start

# Option 2: Using Memurai (Redis-compatible Windows port)
# Download and install Memurai from: https://www.memurai.com/get-memurai
# Run Memurai from Start Menu

# Start Redis server
redis-server
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Start the Django server:

```bash
python manage.py runserver
```

7. Start Celery worker (in a separate terminal):

```bash
cd server

# For macOS, set this environment variable before starting Celery
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# For Windows, set these environment variables
# Windows doesn't support the 'fork' process model, so use 'solo' instead
# Open Command Prompt and run:
set FORKED_BY_MULTIPROCESSING=1
set CELERY_WORKER_POOL=solo

# Start Celery worker
celery -A shorts_generator worker --loglevel=info
```

## API Endpoints

### Create a Short

```
POST /api/shorts/
```

Request body:

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "username": "user_name"
}
```

Response:

```json
{
  "message": "Video processing started",
  "processing": {
    "id": 1,
    "username": "user_name",
    "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "status": "PENDING",
    "cloudinary_url": null,
    "created_at": "2023-06-15T10:30:00Z",
    "updated_at": "2023-06-15T10:30:00Z"
  }
}
```

### Check Processing Status

```
GET /api/shorts/status/{processing_id}/
```

Response:

```json
{
  "id": 1,
  "username": "user_name",
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "status": "COMPLETED",
  "cloudinary_url": "https://res.cloudinary.com/your-cloud/video/upload/v1234567890/shorts/final_1.mp4",
  "created_at": "2023-06-15T10:30:00Z",
  "updated_at": "2023-06-15T10:35:00Z"
}
```

### Get User's Videos

```
GET /api/shorts/user/{username}/
```

Response:

```json
[
  {
    "id": 1,
    "username": "user_name",
    "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "status": "COMPLETED",
    "cloudinary_url": "https://res.cloudinary.com/your-cloud/video/upload/v1234567890/shorts/final_1.mp4",
    "created_at": "2023-06-15T10:30:00Z",
    "updated_at": "2023-06-15T10:35:00Z"
  },
  {
    "id": 2,
    "username": "user_name",
    "youtube_url": "https://www.youtube.com/watch?v=ANOTHER_VIDEO_ID",
    "status": "PROCESSING",
    "cloudinary_url": null,
    "created_at": "2023-06-15T11:30:00Z",
    "updated_at": "2023-06-15T11:30:00Z"
  }
]
```

## Supabase Database Structure

The Supabase database table `shorts` structure:

| Column      | Type      | Description                           |
| ----------- | --------- | ------------------------------------- |
| id          | integer   | Auto-incrementing primary key         |
| username    | text      | Username of the video owner           |
| youtube_url | text      | Original YouTube video URL            |
| short_url   | text      | Cloudinary URL of the generated short |
| created_at  | timestamp | Creation timestamp                    |

## Technology Stack

- Django & Django REST Framework
- OpenAI for highlight extraction
- MoviePy for video editing
- OpenCV for face detection and tracking
- Cloudinary for video hosting
- Supabase for database
- PyTube for YouTube video downloading
