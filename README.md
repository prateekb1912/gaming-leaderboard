# Gaming Leaderboard

A real-time multiplayer gaming leaderboard system built with FastAPI backend and React frontend. This project provides a scalable ranking system that can be integrated into multiplayer games to track player scores and rankings.

## 🎮 Features

- **Real-time Leaderboard**: Live updates of top players and rankings
- **Score Submission**: API endpoints for submitting game scores
- **User Ranking**: Individual player rank lookup functionality
- **Caching System**: Redis-based caching for improved performance
- **Responsive UI**: Modern, mobile-friendly frontend interface
- **Database Persistence**: PostgreSQL database for reliable data storage
- **CORS Support**: Cross-origin resource sharing for frontend integration

## 🏗️ Architecture

### Backend (FastAPI)

- **Framework**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for leaderboard caching
- **Deployment**: render.com hosting

### Frontend (React)

- **Framework**: React 19 with TypeScript
- **Styling**: Tailwind CSS for modern UI
- **Build Tool**: Vite for fast development
- **HTTP Client**: Axios for API communication

## 📁 Project Structure

```
gaming-leaderboard/
├── app/                    # Backend FastAPI application
│   ├── __init__.py
│   ├── main.py            # FastAPI app and endpoints
│   ├── models.py          # SQLAlchemy database models
│   ├── schemas.py         # Pydantic data validation schemas
│   ├── services.py        # Business logic and database operations
│   ├── database.py        # Database connection and session management
│   ├── cache.py           # Redis caching utilities
│   ├── utils.py           # Helper functions
│   └── newrelic.ini       # New Relic monitoring configuration
├── frontend/              # React frontend application
│   ├── src/
│   │   ├── App.tsx        # Main React component
│   │   ├── main.tsx       # React entry point
│   │   └── index.css      # Global styles
│   ├── package.json       # Frontend dependencies
│   └── vite.config.ts     # Vite configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL database
- Redis server

### Backend Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd gaming-leaderboard
   ```

2. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:

   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/gaming_leaderboard
   REDIS_URL=redis://localhost:6379
   ```

4. **Run the backend server**
   ```bash
   cd app
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Install Node.js dependencies**

   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**

   ```bash
   npm run dev
   ```

3. **Build for production**
   ```bash
   npm run build
   ```

## 📚 API Documentation

### Base URL

```
https://gaming-leaderboard-9euy.onrender.com
```

### Endpoints

#### Submit Score

```http
POST /api/leaderboard/submit
```

**Request Body:**

```json
{
  "user_id": 123,
  "score": 1500
}
```

**Response:**

```json
{
  "status": "success"
}
```

#### Get Top Players

```http
GET /api/leaderboard/top
```

**Response:**

```json
[
  {
    "user_id": 123,
    "username": "player1",
    "total_score": 5000,
    "rank": 1
  },
  {
    "user_id": 456,
    "username": "player2",
    "total_score": 4500,
    "rank": 2
  }
]
```

#### Get User Rank

```http
GET /api/leaderboard/rank/{user_id}
```

**Response:**

```json
{
  "user_id": 123,
  "username": "player1",
  "total_score": 5000,
  "rank": 1
}
```

## 🗄️ Database Schema

### Users Table

- `id` (Primary Key): Unique user identifier
- `username` (String): User's display name
- `join_date` (Timestamp): User registration date

### Game Sessions Table

- `id` (Primary Key): Session identifier
- `user_id` (Foreign Key): Reference to users table
- `score` (Integer): Score achieved in this session
- `game_mode` (String): Type of game played
- `timestamp` (Timestamp): When the session occurred

### Leaderboard Table

- `id` (Primary Key): Leaderboard entry identifier
- `user_id` (Foreign Key): Reference to users table
- `total_score` (Integer): Cumulative score across all sessions
- `rank` (Integer): Current ranking position

## 🔧 Configuration

### Environment Variables

| Variable       | Description                  | Default                               |
| -------------- | ---------------------------- | ------------------------------------- |
| `DATABASE_URL` | PostgreSQL connection string | Required                              |
| `REDIS_URL`    | Redis connection string      | Required                              |
| `CORS_ORIGINS` | Allowed frontend origins     | `https://leaderboard-fe.onrender.com` |

### Caching

The system uses Redis for caching leaderboard data to improve performance:

- Leaderboard data is cached for 5 minutes
- Cache is invalidated when new scores are submitted
- Fallback to database query if cache is unavailable

## 🧪 Testing

### Backend Testing

```bash
# Run with pytest (if tests are added)
pytest app/tests/
```

### Frontend Testing

```bash
cd frontend
npm test
```

## 📊 Monitoring

The application includes New Relic monitoring for:

- Application performance metrics
- Error tracking
- Request monitoring
- Database query analysis

## 🚀 Deployment

### Backend Deployment (Render.com)

1. Connect your GitHub repository to Render
2. Configure environment variables
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment

1. Build the application: `npm run build`
2. Deploy the `dist` folder to your hosting provider
3. Configure CORS origins in the backend
