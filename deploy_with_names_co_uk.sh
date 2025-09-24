#!/bin/bash

echo "🚀 Complete Deployment with Names.co.uk"
echo "======================================="
echo ""

echo "📋 This script will help you deploy your registration system"
echo "using your names.co.uk domain and existing infrastructure."
echo ""

echo "🔧 Step 1: Choose Your Deployment Method"
echo ""
echo "1) GitHub Pages + Your Server (Recommended)"
echo "2) Everything on Your Server"
echo "3) Subdomain Setup"
echo ""

read -p "Choose option (1-3): " DEPLOY_OPTION

case $DEPLOY_OPTION in
    1)
        echo ""
        echo "✅ GitHub Pages + Your Server Setup"
        echo ""
        
        echo "📦 Step 1: Deploy Frontend to GitHub Pages"
        echo ""
        echo "Running GitHub Pages setup..."
        ./setup-github-pages.sh
        
        echo ""
        echo "📤 Step 2: Deploy Backend to Your Server"
        echo ""
        echo "Running backend deployment..."
        ./deploy_existing_infrastructure.sh
        
        echo ""
        echo "🌐 Step 3: Configure DNS in Names.co.uk"
        echo ""
        echo "DNS Records to add:"
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
        echo "Record Type: A"
        echo "Name: api"
        echo "Value: YOUR_SERVER_IP"
        echo "TTL: 300"
        echo ""
        echo "🔧 Step 4: Update Frontend Configuration"
        echo ""
        read -p "Enter your backend server URL (e.g., https://api.teknoledg.com): " BACKEND_URL
        
        # Update the JavaScript file
        sed -i.bak "s|const BACKEND_URL = 'https://your-backend-url.railway.app';|const BACKEND_URL = '$BACKEND_URL';|g" js/script.js
        
        echo "✅ Frontend updated with backend URL: $BACKEND_URL"
        echo ""
        echo "📤 Step 5: Commit and Push to GitHub"
        echo ""
        echo "git add ."
        echo "git commit -m 'Deploy with names.co.uk domain'"
        echo "git push origin main"
        echo ""
        echo "🌐 Your site will be available at:"
        echo "  https://teknoledg.com"
        echo "  https://www.teknoledg.com"
        echo "  Admin: $BACKEND_URL/admin"
        ;;
    2)
        echo ""
        echo "✅ Everything on Your Server Setup"
        echo ""
        
        read -p "Enter your server IP address: " SERVER_IP
        read -p "Enter your server username: " SERVER_USER
        read -p "Enter your server domain (e.g., teknoledg.com): " SERVER_DOMAIN
        
        echo ""
        echo "📦 Step 1: Deploy to Your Server"
        echo ""
        echo "Uploading files to your server..."
        
        # Create deployment package
        tar -czf teknoledg-deployment.tar.gz index.html css/ js/ images/ backend/
        
        echo "📤 Uploading to $SERVER_USER@$SERVER_IP..."
        scp teknoledg-deployment.tar.gz $SERVER_USER@$SERVER_IP:/tmp/
        
        echo "📦 Extracting files on server..."
        ssh $SERVER_USER@$SERVER_IP "cd /var/www && tar -xzf /tmp/teknoledg-deployment.tar.gz"
        
        echo "🔧 Configuring server..."
        ssh $SERVER_USER@$SERVER_IP "cd /var/www && chmod +x backend/app_existing_db.py"
        
        echo ""
        echo "🌐 Step 2: Configure DNS in Names.co.uk"
        echo ""
        echo "DNS Records to add:"
        echo ""
        echo "Record Type: A"
        echo "Name: @"
        echo "Value: $SERVER_IP"
        echo "TTL: 300"
        echo ""
        echo "Record Type: A"
        echo "Name: www"
        echo "Value: $SERVER_IP"
        echo "TTL: 300"
        echo ""
        echo "Record Type: A"
        echo "Name: api"
        echo "Value: $SERVER_IP"
        echo "TTL: 300"
        echo ""
        echo "🔐 Step 3: Configure SSL"
        echo ""
        echo "On your server, run:"
        echo "sudo certbot --nginx -d $SERVER_DOMAIN -d www.$SERVER_DOMAIN"
        echo ""
        echo "🌐 Your site will be available at:"
        echo "  https://$SERVER_DOMAIN"
        echo "  https://www.$SERVER_DOMAIN"
        echo "  Admin: https://$SERVER_DOMAIN/admin"
        ;;
    3)
        echo ""
        echo "✅ Subdomain Setup"
        echo ""
        
        read -p "Enter your server IP address: " SERVER_IP
        read -p "Enter your server username: " SERVER_USER
        
        echo ""
        echo "📦 Step 1: Deploy Frontend"
        echo ""
        echo "Uploading frontend files..."
        scp -r index.html css/ js/ images/ $SERVER_USER@$SERVER_IP:/var/www/teknoledg.com/
        
        echo ""
        echo "📦 Step 2: Deploy Backend"
        echo ""
        echo "Uploading backend files..."
        scp -r backend/ $SERVER_USER@$SERVER_IP:/var/www/api.teknoledg.com/
        
        echo ""
        echo "🌐 Step 3: Configure DNS in Names.co.uk"
        echo ""
        echo "DNS Records to add:"
        echo ""
        echo "Record Type: A"
        echo "Name: @"
        echo "Value: $SERVER_IP"
        echo "TTL: 300"
        echo ""
        echo "Record Type: A"
        echo "Name: www"
        echo "Value: $SERVER_IP"
        echo "TTL: 300"
        echo ""
        echo "Record Type: A"
        echo "Name: api"
        echo "Value: $SERVER_IP"
        echo "TTL: 300"
        echo ""
        echo "🔧 Step 4: Update Frontend Configuration"
        echo ""
        # Update the JavaScript file
        sed -i.bak "s|const BACKEND_URL = 'https://your-backend-url.railway.app';|const BACKEND_URL = 'https://api.teknoledg.com';|g" js/script.js
        
        echo "✅ Frontend updated with backend URL: https://api.teknoledg.com"
        echo ""
        echo "🌐 Your site will be available at:"
        echo "  https://teknoledg.com"
        echo "  https://www.teknoledg.com"
        echo "  Admin: https://api.teknoledg.com/admin"
        ;;
    *)
        echo "❌ Invalid option. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Log into your names.co.uk account"
echo "2. Go to 'My Domains'"
echo "3. Click on teknoledg.com"
echo "4. Select 'DNS Management' or 'Advanced DNS'"
echo "5. Add the DNS records shown above"
echo "6. Save changes"
echo ""
echo "⏰ DNS propagation can take up to 24 hours"
echo ""
echo "🔍 To check DNS propagation:"
echo "Visit: https://dnschecker.org"
echo "Enter: teknoledg.com"
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📞 If you need help:"
echo "- Check the NAMES_CO_UK_SETUP.md guide"
echo "- Contact names.co.uk support"
echo "- Test your site after DNS propagation"
