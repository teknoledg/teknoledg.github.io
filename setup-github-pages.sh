#!/bin/bash

echo "🚀 Setting up GitHub Pages deployment for teknoledg.github.io"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please initialize git first:"
    echo "   git init"
    echo "   git remote add origin https://github.com/teknoledg/teknoledg.github.io.git"
    exit 1
fi

echo "📁 Creating docs directory for GitHub Pages..."
mkdir -p docs

echo "📄 Copying files for GitHub Pages deployment..."
cp index-github.html docs/index.html
cp -r css docs/ 2>/dev/null || echo "⚠️  CSS directory not found"
cp -r js docs/ 2>/dev/null || echo "⚠️  JS directory not found"
cp -r images docs/ 2>/dev/null || echo "⚠️  Images directory not found"

echo "🌐 Setting up custom domain (teknoledg.com)..."
echo "teknoledg.com" > docs/CNAME

echo "⚙️ Creating .nojekyll file..."
touch docs/.nojekyll

echo "📝 Creating README for GitHub Pages..."
cat > docs/README.md << 'EOF'
# Teknoledge

Welcome to Teknoledge - Harnessing Artificial Intelligence to empower users.

## Features

- Modern glassmorphic design
- AI-powered background animations
- Registration form for product updates
- Responsive design for all devices

## Contact

For more information, visit our main site or contact tim@teknoledg.com
EOF

echo ""
echo "✅ GitHub Pages setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update index-github.html with your Formspree form ID"
echo "2. Commit and push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Deploy to GitHub Pages'"
echo "   git push origin main"
echo ""
echo "3. Enable GitHub Pages:"
echo "   - Go to repository settings"
echo "   - Scroll to 'Pages' section"
echo "   - Set source to 'Deploy from a branch'"
echo "   - Select 'main' branch and '/docs' folder"
echo "   - Save settings"
echo ""
echo "4. Configure custom domain (optional):"
echo "   - Add DNS records for teknoledg.com"
echo "   - Set custom domain in GitHub Pages settings"
echo ""
echo "🌐 Your site will be available at:"
echo "   https://teknoledg.github.io"
echo "   https://teknoledg.com (after DNS setup)"
echo ""
echo "📧 For form submissions, set up Formspree:"
echo "   1. Go to https://formspree.io"
echo "   2. Create a free account"
echo "   3. Create a new form"
echo "   4. Update the form action in docs/index.html"
