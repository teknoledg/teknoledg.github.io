#!/bin/bash

echo "🚀 Deploying Teknoledge API to Vercel..."

# Install Vercel CLI if not already installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Login to Vercel (if not already logged in)
echo "🔐 Logging into Vercel..."
vercel login

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Go to Vercel dashboard: https://vercel.com/dashboard"
echo "2. Find your project and go to Storage tab"
echo "3. Create a new Postgres database"
echo "4. Copy the connection string"
echo "5. Add it as environment variable: POSTGRES_URL"
echo "6. Redeploy the project"
echo ""
echo "🔗 Your API will be available at:"
echo "   - Registration: https://your-project.vercel.app/api/register"
echo "   - Admin Panel: https://your-project.vercel.app/api/admin"
echo "   - Registrations: https://your-project.vercel.app/api/registrations"
