#!/bin/bash

# Deploy script for GitHub Pages
echo "🚀 Deploying to GitHub Pages..."

# Create docs directory for GitHub Pages
mkdir -p docs

# Copy static files
echo "📁 Copying static files..."
cp index-github.html docs/index.html
cp -r css docs/
cp -r js docs/
cp -r images docs/

# Create CNAME file for custom domain
echo "🌐 Setting up custom domain..."
echo "teknoledg.com" > docs/CNAME

# Create .nojekyll file to prevent Jekyll processing
echo "⚙️ Creating .nojekyll file..."
touch docs/.nojekyll

echo "✅ Deployment files ready!"
echo "📝 Next steps:"
echo "1. Commit and push to GitHub"
echo "2. Enable GitHub Pages in repository settings"
echo "3. Set source to 'docs' folder"
echo "4. Configure custom domain: teknoledg.com"
