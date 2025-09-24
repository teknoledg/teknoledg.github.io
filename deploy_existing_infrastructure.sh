#!/bin/bash

echo "🚀 Deploying to your existing teknoledg.com infrastructure"
echo ""

echo "📋 This script will help you integrate with your existing database and email system"
echo ""

echo "🔧 Step 1: Configure your existing database"
echo "Please provide the following information about your existing database:"
echo ""

read -p "Database Host (e.g., localhost or your server IP): " DB_HOST
read -p "Database Username: " DB_USER
read -s -p "Database Password: " DB_PASSWORD
echo ""
read -p "Database Name: " DB_NAME
read -p "Database Port (default 3306): " DB_PORT
DB_PORT=${DB_PORT:-3306}

echo ""
echo "📧 Step 2: Configure your existing email system"
echo ""

read -p "SMTP Server (e.g., mail.teknoledg.com): " SMTP_SERVER
read -p "SMTP Port (default 587): " SMTP_PORT
SMTP_PORT=${SMTP_PORT:-587}
read -p "Email Username (e.g., noreply@teknoledg.com): " EMAIL_USER
read -s -p "Email Password: " EMAIL_PASSWORD
echo ""

echo "🔐 Step 3: Set up admin credentials"
echo ""

read -p "Admin Username (default: admin): " ADMIN_USERNAME
ADMIN_USERNAME=${ADMIN_USERNAME:-admin}
read -s -p "Admin Password: " ADMIN_PASSWORD
echo ""

# Generate password hash
ADMIN_PASSWORD_HASH=$(python3 -c "import hashlib; print(hashlib.sha256(b'$ADMIN_PASSWORD').hexdigest())")

echo ""
echo "📝 Creating environment configuration..."
echo ""

# Create .env file
cat > backend/.env << EOF
# Database Configuration
DB_HOST=$DB_HOST
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_NAME=$DB_NAME
DB_PORT=$DB_PORT

# Email Configuration
SMTP_SERVER=$SMTP_SERVER
SMTP_PORT=$SMTP_PORT
EMAIL_USER=$EMAIL_USER
EMAIL_PASSWORD=$EMAIL_PASSWORD

# Flask Configuration
FLASK_ENV=production
PORT=5000
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Admin Configuration
ADMIN_USERNAME=$ADMIN_USERNAME
ADMIN_PASSWORD_HASH=$ADMIN_PASSWORD_HASH
EOF

echo "✅ Environment configuration created!"
echo ""

echo "📦 Installing dependencies..."
cd backend
pip install -r requirements_existing_db.txt
cd ..

echo ""
echo "🗄️ Testing database connection..."
python3 -c "
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

try:
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT', 3306))
    )
    print('✅ Database connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Starting the application..."
    echo ""
    echo "Your registration system is now running with your existing infrastructure!"
    echo ""
    echo "🌐 URLs:"
    echo "  Main site: http://localhost:5000"
    echo "  Admin panel: http://localhost:5000/admin"
    echo ""
    echo "📧 Email notifications will be sent to: tim@teknoledg.com"
    echo "🗄️ Data will be stored in your existing database: $DB_NAME"
    echo ""
    echo "🔧 To run in production:"
    echo "  python3 backend/app_existing_db.py"
    echo ""
    echo "📋 Next steps:"
    echo "1. Test the form submission"
    echo "2. Check your database for new registrations"
    echo "3. Verify email notifications are working"
    echo "4. Access admin panel to view data"
else
    echo ""
    echo "❌ Database connection failed. Please check your credentials and try again."
    echo ""
    echo "🔧 Troubleshooting:"
    echo "1. Verify database credentials"
    echo "2. Check if database server is running"
    echo "3. Ensure database user has proper permissions"
    echo "4. Check firewall settings"
fi
