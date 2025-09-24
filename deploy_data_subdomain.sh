#!/bin/bash

echo "🗄️ Data.teknoledg.com Subdomain Deployment"
echo "=========================================="
echo ""

echo "📋 This script will help you deploy your backend to data.teknoledg.com"
echo "while keeping your frontend on teknoledg.com"
echo ""

echo "🔧 Step 1: Configure Your Server Details"
echo ""

read -p "Enter your server IP address: " SERVER_IP
read -p "Enter your server username: " SERVER_USER
read -p "Enter your server domain (e.g., your-server.com): " SERVER_DOMAIN

echo ""
echo "📧 Step 2: Configure Email Settings"
echo ""

read -p "SMTP Server (e.g., mail.teknoledg.com): " SMTP_SERVER
read -p "SMTP Port (default 587): " SMTP_PORT
SMTP_PORT=${SMTP_PORT:-587}
read -p "Email Username (e.g., noreply@teknoledg.com): " EMAIL_USER
read -s -p "Email Password: " EMAIL_PASSWORD
echo ""

echo "🗄️ Step 3: Configure Database Settings"
echo ""

read -p "Database Host (e.g., localhost): " DB_HOST
read -p "Database Username: " DB_USER
read -s -p "Database Password: " DB_PASSWORD
echo ""
read -p "Database Name: " DB_NAME
read -p "Database Port (default 3306): " DB_PORT
DB_PORT=${DB_PORT:-3306}

echo ""
echo "🔐 Step 4: Set Up Admin Credentials"
echo ""

read -p "Admin Username (default: admin): " ADMIN_USERNAME
ADMIN_USERNAME=${ADMIN_USERNAME:-admin}
read -s -p "Admin Password: " ADMIN_PASSWORD
echo ""

# Generate password hash
ADMIN_PASSWORD_HASH=$(python3 -c "import hashlib; print(hashlib.sha256(b'$ADMIN_PASSWORD').hexdigest())")

echo ""
echo "📦 Step 5: Deploy Backend to data.teknoledg.com"
echo ""

echo "Creating deployment package..."
tar -czf data-teknoledg-deployment.tar.gz backend/

echo "📤 Uploading to $SERVER_USER@$SERVER_IP..."
scp data-teknoledg-deployment.tar.gz $SERVER_USER@$SERVER_IP:/tmp/

echo "📦 Extracting files on server..."
ssh $SERVER_USER@$SERVER_IP "mkdir -p /var/www/data.teknoledg.com && cd /var/www/data.teknoledg.com && tar -xzf /tmp/data-teknoledg-deployment.tar.gz"

echo "🔧 Configuring server..."
ssh $SERVER_USER@$SERVER_IP "cd /var/www/data.teknoledg.com && chmod +x app_existing_db.py"

echo ""
echo "📝 Step 6: Create Environment Configuration"
echo ""

# Create environment file on server
ssh $SERVER_USER@$SERVER_IP "cat > /var/www/data.teknoledg.com/.env << EOF
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
EOF"

echo "✅ Environment configuration created on server"
echo ""

echo "📦 Step 7: Install Dependencies"
echo ""

ssh $SERVER_USER@$SERVER_IP "cd /var/www/data.teknoledg.com && pip3 install -r requirements_existing_db.txt"

echo ""
echo "🌐 Step 8: Configure DNS in Names.co.uk"
echo ""

echo "DNS Records to add in names.co.uk:"
echo ""
echo "Record Type: A"
echo "Name: data"
echo "Value: $SERVER_IP"
echo "TTL: 300"
echo ""
echo "Record Type: A"
echo "Name: @"
echo "Value: 185.199.108.153"
echo "TTL: 300"
echo ""
echo "Record Type: A"
echo "Name: @"
echo "Value: 185.199.109.153"
echo "TTL: 300"
echo ""
echo "Record Type: A"
echo "Name: @"
echo "Value: 185.199.110.153"
echo "TTL: 300"
echo ""
echo "Record Type: A"
echo "Name: @"
echo "Value: 185.199.111.153"
echo "TTL: 300"
echo ""
echo "Record Type: CNAME"
echo "Name: www"
echo "Value: teknoledg.github.io"
echo "TTL: 300"
echo ""

echo "🔐 Step 9: Configure SSL Certificate"
echo ""

echo "On your server, run:"
echo "sudo certbot --nginx -d data.teknoledg.com"
echo ""

echo "📤 Step 10: Deploy Frontend to GitHub Pages"
echo ""

echo "Running GitHub Pages setup..."
./setup-github-pages.sh

echo ""
echo "🔧 Step 11: Update Frontend Configuration"
echo ""

# Update the JavaScript file to use data.teknoledg.com
sed -i.bak "s|const BACKEND_URL = 'https://your-backend-url.railway.app';|const BACKEND_URL = 'https://data.teknoledg.com';|g" js/script.js

echo "✅ Frontend updated to use data.teknoledg.com"
echo ""

echo "📤 Step 12: Commit and Push to GitHub"
echo ""

echo "git add ."
echo "git commit -m 'Deploy with data.teknoledg.com backend'"
echo "git push origin main"
echo ""

echo "🌐 Step 13: Test Your Setup"
echo ""

echo "After DNS propagation (up to 24 hours), test:"
echo ""
echo "1. Main site: https://teknoledg.com"
echo "2. Backend API: https://data.teknoledg.com"
echo "3. Admin panel: https://data.teknoledg.com/admin"
echo "4. Form submission: Submit the form and check database"
echo ""

echo "✅ Deployment complete!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Log into names.co.uk and add the DNS records shown above"
echo "2. Wait for DNS propagation (up to 24 hours)"
echo "3. Test your site at https://teknoledg.com"
echo "4. Test your backend at https://data.teknoledg.com"
echo "5. Access admin panel at https://data.teknoledg.com/admin"
echo ""
echo "🔍 To check DNS propagation:"
echo "Visit: https://dnschecker.org"
echo "Enter: data.teknoledg.com"
echo ""
echo "📞 If you need help:"
echo "- Check the DATA_SUBDOMAIN_SETUP.md guide"
echo "- Contact names.co.uk support for DNS issues"
echo "- Check your server logs for backend issues"
