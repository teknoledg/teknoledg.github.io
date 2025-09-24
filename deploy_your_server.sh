#!/bin/bash

echo "🖥️ Deploy to Your Web Server (tb-hosting.com)"
echo "============================================="
echo ""

echo "📋 Using database credentials from secrets file..."
echo ""

# Read credentials from secrets file
DB_SERVER="tb-be03-linweb054.srv.teamblue-ops.net:3306"
DB_NAME="gdibat_teknoledg"
DB_USER="gdibat_admin"
DB_PASSWORD="tiqdeq-4mukhi-ryjByb"

echo "🔧 Step 1: Server Configuration"
echo ""

echo "Your server details:"
echo "Host: gdibat.ssh.tb-hosting.com"
echo "Username: gdibatb-hostingcom"
echo ""

# Using default server password (you may need to update this)
SERVER_PASSWORD="your-server-password-here"

echo ""
echo "📧 Step 2: Email Configuration"
echo ""

# Using Gmail SMTP for email notifications
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT="587"
EMAIL_USER="hello@thepersonaldataexchange.com"
EMAIL_PASSWORD="your-gmail-app-password-here"

echo ""
echo "🔐 Step 3: Admin Credentials"
echo ""

# Using default admin credentials
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="admin123"

# Generate password hash
ADMIN_PASSWORD_HASH=$(python3 -c "import hashlib; print(hashlib.sha256(b'$ADMIN_PASSWORD').hexdigest())")

echo ""
echo "📦 Step 4: Deploy Backend to Your Server"
echo ""

echo "Creating deployment package..."
tar -czf teknoledg-api-deployment.tar.gz backend/

echo "📤 Uploading to gdibat.ssh.tb-hosting.com..."
scp teknoledg-api-deployment.tar.gz gdibatb-hostingcom@gdibat.ssh.tb-hosting.com:/tmp/

echo "📦 Extracting files on server..."
sshpass -p "$SERVER_PASSWORD" ssh gdibatb-hostingcom@gdibat.ssh.tb-hosting.com "mkdir -p /var/www/teknoledg-api && cd /var/www/teknoledg-api && tar -xzf /tmp/teknoledg-api-deployment.tar.gz"

echo "🔧 Configuring server..."
sshpass -p "$SERVER_PASSWORD" ssh gdibatb-hostingcom@gdibat.ssh.tb-hosting.com "cd /var/www/teknoledg-api && chmod +x app_existing_db.py"

echo ""
echo "📝 Step 5: Create Environment Configuration"
echo ""

# Create environment file on server with actual database credentials
sshpass -p "$SERVER_PASSWORD" ssh gdibatb-hostingcom@gdibat.ssh.tb-hosting.com "cat > /var/www/teknoledg-api/.env << EOF
# Database Configuration (from secrets file)
DB_HOST=tb-be03-linweb054.srv.teamblue-ops.net
DB_USER=gdibat_admin
DB_PASSWORD=tiqdeq-4mukhi-ryjByb
DB_NAME=gdibat_teknoledg
DB_PORT=3306

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

echo "✅ Environment configuration created on server with database credentials"
echo ""

echo "📦 Step 6: Install Dependencies"
echo ""

sshpass -p "$SERVER_PASSWORD" ssh gdibatb-hostingcom@gdibat.ssh.tb-hosting.com "cd /var/www/teknoledg-api && pip3 install -r requirements_existing_db.txt"

echo ""
echo "🌐 Step 7: Configure DNS in Names.co.uk"
echo ""

echo "DNS Records to add in names.co.uk:"
echo ""
echo "Record Type: A"
echo "Name: data"
echo "Value: [Your server IP - get from hosting provider]"
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

echo "🔐 Step 8: Configure SSL Certificate"
echo ""

echo "On your server, run:"
echo "sudo certbot --nginx -d data.teknoledg.com"
echo ""

echo "📤 Step 9: Deploy Frontend to GitHub Pages"
echo ""

echo "Running GitHub Pages setup..."
./setup-github-pages.sh

echo ""
echo "🔧 Step 10: Update Frontend Configuration"
echo ""

# Update the JavaScript file to use your server
echo "Update js/script.js with your server URL:"
echo "const BACKEND_URL = 'https://data.teknoledg.com';"
echo ""

echo "📤 Step 11: Commit and Push to GitHub"
echo ""

echo "git add ."
echo "git commit -m 'Deploy with your server backend'"
echo "git push origin main"
echo ""
echo "Repository: https://github.com/teknoledg/teknoledg.github.io"
echo ""

echo "🌐 Step 12: Test Your Setup"
echo ""

echo "After DNS propagation (up to 24 hours), test:"
echo ""
echo "1. Main site: https://teknoledg.github.io"
echo "2. Custom domain: https://teknoledg.com (after DNS setup)"
echo "3. Backend API: https://data.teknoledg.com"
echo "4. Admin panel: https://data.teknoledg.com/admin"
echo "5. Form submission: Submit the form and check database"
echo ""

echo "✅ Deployment complete!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Get your server IP from hosting provider"
echo "2. Log into names.co.uk and add DNS records"
echo "3. Wait for DNS propagation (up to 24 hours)"
echo "4. Test your site at https://teknoledg.github.io"
echo "5. Test your backend at https://data.teknoledg.com"
echo "6. Access admin panel at https://data.teknoledg.com/admin"
echo ""
echo "🔍 To check DNS propagation:"
echo "Visit: https://dnschecker.org"
echo "Enter: data.teknoledg.com"
echo ""
echo "📞 If you need help:"
echo "- Check the DATA_SUBDOMAIN_SETUP.md guide"
echo "- Contact names.co.uk support for DNS issues"
echo "- Check your server logs for backend issues"
echo ""
echo "🗄️ Database Configuration:"
echo "Host: tb-be03-linweb054.srv.teamblue-ops.net:3306"
echo "Database: gdibat_teknoledg"
echo "User: gdibat_admin"
echo "Password: tiqdeq-4mukhi-ryjByb"
echo ""
echo "🖥️ Your Server:"
echo "Host: gdibat.ssh.tb-hosting.com"
echo "Username: gdibatb-hostingcom"
