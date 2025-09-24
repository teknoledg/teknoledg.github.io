#!/bin/bash

echo "🚀 Deploying to Railway (Self-hosted solution)"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install railway
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://railway.app/install.sh | sh
    else
        echo "❌ Please install Railway CLI manually from https://railway.app"
        exit 1
    fi
fi

echo "🔐 Logging into Railway..."
railway login

echo "🚀 Creating new Railway project..."
railway init

echo "📤 Deploying backend..."
railway up

echo "🔧 Setting up environment variables..."
echo "Please set these environment variables in Railway dashboard:"
echo ""
echo "EMAIL_PASSWORD=your_email_password"
echo "ADMIN_USERNAME=admin"
echo "ADMIN_PASSWORD_HASH=$(python3 -c 'import hashlib; print(hashlib.sha256(b"your_password").hexdigest())')"
echo ""

echo "✅ Deployment complete!"
echo ""
echo "🌐 Your backend will be available at:"
echo "   https://your-project-name.railway.app"
echo ""
echo "📧 Admin panel:"
echo "   https://your-project-name.railway.app/admin"
echo ""
echo "🔧 Next steps:"
echo "1. Update js/script.js with your Railway URL"
echo "2. Deploy frontend to GitHub Pages"
echo "3. Test form submissions"
