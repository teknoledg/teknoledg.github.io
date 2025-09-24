# GitHub Pages Deployment Guide

## 🚀 Deploy to teknoledg.github.io

This guide will help you deploy your Teknoledge site to GitHub Pages at `teknoledg.github.io`.

## 📋 Prerequisites

1. **GitHub Repository** - Your code should be in a GitHub repository
2. **GitHub Pages enabled** - Enable in repository settings
3. **Custom domain** - teknoledg.com (optional)

## 🔧 Deployment Options

### Option 1: Static Site (Recommended for GitHub Pages)

Since GitHub Pages only supports static sites, we'll use a form service for submissions:

#### 1. Set up Formspree (Free form handling)

1. Go to [formspree.io](https://formspree.io)
2. Create a free account
3. Create a new form
4. Copy your form ID
5. Update `index-github.html` with your form ID:
   ```html
   <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
   ```

#### 2. Deploy to GitHub Pages

```bash
# Run the deployment script
./deploy-github.sh

# Commit and push to GitHub
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main
```

#### 3. Configure GitHub Pages

1. Go to your repository settings
2. Scroll to "Pages" section
3. Set source to "Deploy from a branch"
4. Select "main" branch and "/docs" folder
5. Save settings

### Option 2: Full Backend (Separate Hosting)

For the complete backend with database and admin panel:

#### Backend Hosting Options:

1. **Heroku** (Free tier available)
   ```bash
   # Install Heroku CLI
   # Create Heroku app
   heroku create teknoledg-backend
   
   # Set environment variables
   heroku config:set EMAIL_PASSWORD=your_password
   heroku config:set ADMIN_USERNAME=admin
   heroku config:set ADMIN_PASSWORD_HASH=your_hash
   
   # Deploy
   git subtree push --prefix=backend heroku main
   ```

2. **PythonAnywhere** (Free tier available)
   - Upload backend files
   - Configure WSGI file
   - Set up scheduled tasks

3. **Railway** (Modern alternative)
   - Connect GitHub repository
   - Automatic deployments
   - Environment variables

#### Frontend Configuration:

Update the JavaScript in `js/script.js` to point to your backend:

```javascript
// Change this line:
const response = await fetch('/api/register', {

// To your backend URL:
const response = await fetch('https://your-backend-url.herokuapp.com/api/register', {
```

## 🌐 Custom Domain Setup

### 1. Configure DNS

Add these DNS records to your domain provider:

```
Type: CNAME
Name: www
Value: teknoledg.github.io

Type: A
Name: @
Value: 185.199.108.153
Value: 185.199.109.153
Value: 185.199.110.153
Value: 185.199.111.153
```

### 2. GitHub Pages Settings

1. Go to repository settings
2. Scroll to "Pages" section
3. Enter custom domain: `teknoledg.com`
4. Check "Enforce HTTPS"

## 📁 File Structure for GitHub Pages

```
/
├── docs/                    # GitHub Pages source
│   ├── index.html          # Main page
│   ├── css/                # Styles
│   ├── js/                 # JavaScript
│   ├── images/             # Images
│   ├── CNAME              # Custom domain
│   └── .nojekyll          # Disable Jekyll
├── backend/                # Backend code (for separate hosting)
├── .github/workflows/      # GitHub Actions
└── deploy-github.sh       # Deployment script
```

## 🔄 Automated Deployment

The GitHub Actions workflow will automatically deploy when you push to main:

1. **Triggers on push** to main branch
2. **Builds static site** from source files
3. **Deploys to GitHub Pages** automatically

## 📧 Email Configuration

### For Static Site (Formspree):
- Formspree handles email notifications automatically
- Configure in Formspree dashboard
- Set recipient email to tim@teknoledg.com

### For Backend Hosting:
- Update email settings in `backend/app.py`
- Set environment variables for SMTP
- Configure email server details

## 🛠️ Development Workflow

1. **Make changes** to source files
2. **Test locally** with `python backend/app.py`
3. **Run deployment script** `./deploy-github.sh`
4. **Commit and push** to GitHub
5. **GitHub Actions** automatically deploys

## 🔍 Troubleshooting

### Common Issues:

1. **404 on GitHub Pages**
   - Check that files are in `/docs` folder
   - Verify GitHub Pages source is set to `/docs`

2. **Custom domain not working**
   - Check DNS records
   - Verify CNAME file exists
   - Wait for DNS propagation (up to 24 hours)

3. **Form submissions not working**
   - Verify Formspree form ID
   - Check form action URL
   - Test form submission

### Debug Steps:

1. Check GitHub Pages build logs
2. Verify file paths and structure
3. Test locally before deploying
4. Check browser console for errors

## 📞 Support

For deployment issues:
- Check GitHub Pages documentation
- Review repository settings
- Test with simple HTML first
- Contact GitHub support if needed

## 🎯 Final URLs

After deployment:
- **Main site:** https://teknoledg.github.io
- **Custom domain:** https://teknoledg.com (if configured)
- **Admin panel:** https://your-backend-url.com/admin (if using backend)
