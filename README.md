# Teknoledge Registration System

A modern registration system with glassmorphic design, SQLite database storage, and email notifications.

## Features

- **Glassmorphic UI Design** - Modern, transparent interface
- **Form Validation** - Client and server-side validation
- **SQLite Database** - Local database storage for registrations
- **Email Notifications** - Automatic alerts to tim@teknoledg.com
- **Responsive Design** - Works on all devices
- **AI Background** - Animated AI selfie images

## Setup Instructions

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `env_example.txt` to `.env` and configure:

```bash
cp env_example.txt .env
```

Update the following variables in `.env`:
- `EMAIL_PASSWORD` - Your email server password
- `FLASK_ENV` - Set to 'production' for production
- `PORT` - Server port (default: 5000)

### 3. Email Server Configuration

Update these settings in `backend/app.py`:
- `SMTP_SERVER` - Your email server (e.g., 'mail.teknoledg.com')
- `SMTP_PORT` - Email server port (587 for TLS, 465 for SSL)
- `EMAIL_USER` - Sender email address
- `ADMIN_EMAIL` - Recipient email (tim@teknoledg.com)

### 4. Run the Application

```bash
python backend/app.py
```

The application will:
- Initialize the SQLite database automatically
- Start the Flask server
- Serve the frontend and handle API requests

## API Endpoints

### POST /api/register
Register a new user for updates.

**Request:**
```json
{
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Thank you for registering! We'll notify you when we launch.",
  "email_sent": true
}
```

### GET /api/stats
Get registration statistics.

**Response:**
```json
{
  "total_registrations": 150,
  "recent_registrations": 5
}
```

## Database Schema

The SQLite database includes a `registrations` table with:
- `id` - Primary key
- `email` - User email (unique)
- `name` - User name (optional)
- `timestamp` - Registration time
- `ip_address` - User IP address
- `user_agent` - Browser information

## Deployment Options

### Option 1: Heroku
1. Create a Heroku app
2. Set environment variables in Heroku dashboard
3. Deploy using Git

### Option 2: PythonAnywhere
1. Upload files to PythonAnywhere
2. Configure WSGI file
3. Set up scheduled tasks if needed

### Option 3: VPS/Cloud Server
1. Install Python 3 and pip
2. Install requirements
3. Configure reverse proxy (nginx)
4. Set up SSL certificate

## File Structure

```
/
├── index.html              # Main page
├── css/style.css          # Styles
├── js/script.js           # Frontend JavaScript
├── images/                # Logo and background images
├── backend/
│   ├── app.py            # Flask backend
│   ├── requirements.txt  # Python dependencies
│   └── env_example.txt   # Environment template
├── Procfile              # Heroku deployment
└── README.md            # This file
```

## Security Notes

- Email passwords should be stored as environment variables
- Consider using HTTPS in production
- Implement rate limiting for registration endpoint
- Regular database backups recommended

## Support

For technical support, contact tim@teknoledg.com
