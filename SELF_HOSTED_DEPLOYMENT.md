# 🚀 Self-Hosted Deployment Guide

## No Third-Party Services Required!

This guide shows you how to deploy your own backend without using Formspree or other services.

## 🎯 Deployment Options

### **Option 1: Railway (Recommended - Easiest)**

Railway is the easiest way to deploy your Python backend:

#### **Step 1: Deploy Backend**
```bash
# Run the deployment script
./deploy-railway.sh
```

#### **Step 2: Get Your Backend URL**
After deployment, Railway will give you a URL like:
`https://teknoledg-backend-production.railway.app`

#### **Step 3: Update Frontend**
1. Open `js/script.js`
2. Replace `https://your-backend-url.railway.app` with your actual Railway URL
3. Deploy frontend to GitHub Pages

#### **Step 4: Set Environment Variables**
In Railway dashboard, add:
- `EMAIL_PASSWORD`: Your email password
- `ADMIN_USERNAME`: admin
- `ADMIN_PASSWORD_HASH`: `sha256 hash of your password`

---

### **Option 2: PythonAnywhere (Free Tier)**

#### **Step 1: Create Account**
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create free account
3. Upload your `backend` folder

#### **Step 2: Configure Web App**
1. Go to "Web" tab
2. Create new web app
3. Choose "Flask" and Python 3.9
4. Set source code: `/home/yourusername/backend`
5. Set working directory: `/home/yourusername/backend`

#### **Step 3: Create WSGI File**
Add this to your WSGI file:
```python
import sys
path = '/home/yourusername/backend'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

#### **Step 4: Set Environment Variables**
In PythonAnywhere console:
```bash
export EMAIL_PASSWORD="your_password"
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD_HASH="your_hash"
```

---

### **Option 3: Render (Free Tier)**

#### **Step 1: Connect GitHub**
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Select "Web Service"

#### **Step 2: Configure Service**
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && python app.py`
- **Environment**: Python 3

#### **Step 3: Set Environment Variables**
- `EMAIL_PASSWORD`: Your email password
- `ADMIN_USERNAME`: admin
- `ADMIN_PASSWORD_HASH`: Your password hash

---

## 🔧 Complete Setup Process

### **1. Deploy Backend (Choose One)**

#### **Railway (Recommended):**
```bash
./deploy-railway.sh
```

#### **PythonAnywhere:**
```bash
./deploy-pythonanywhere.sh
```

#### **Render:**
1. Push to GitHub
2. Connect to Render
3. Deploy automatically

### **2. Update Frontend**

1. **Get your backend URL** from your hosting service
2. **Update `js/script.js`:**
   ```javascript
   const BACKEND_URL = 'https://your-actual-backend-url.com';
   ```
3. **Deploy frontend to GitHub Pages:**
   ```bash
   ./setup-github-pages.sh
   git add .
   git commit -m "Deploy with self-hosted backend"
   git push origin main
   ```

### **3. Configure Email**

Update `backend/app.py` with your email settings:
```python
# Email configuration
SMTP_SERVER = "smtp.gmail.com"  # or your email provider
SMTP_PORT = 587
EMAIL_USER = "tim@teknoledg.com"
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
```

### **4. Test Everything**

1. **Visit your site**: https://teknoledg.github.io
2. **Submit the form** - should work with your backend
3. **Check admin panel**: https://your-backend-url.com/admin
4. **Verify email** - should receive notification

## 📧 Email Configuration

### **Gmail Setup:**
1. Enable 2-factor authentication
2. Generate app password
3. Use app password as `EMAIL_PASSWORD`

### **Other Email Providers:**
- **Outlook**: smtp-mail.outlook.com, port 587
- **Yahoo**: smtp.mail.yahoo.com, port 587
- **Custom**: Use your domain's SMTP settings

## 🔐 Admin Panel Access

After deployment, access your admin panel:
- **URL**: `https://your-backend-url.com/admin`
- **Username**: admin
- **Password**: Whatever you set in `ADMIN_PASSWORD_HASH`

## 📊 Database Management

Your SQLite database will be automatically created and managed. You can:
- **View registrations** in admin panel
- **Export data** as CSV
- **Delete entries** as needed
- **View statistics** (total, daily, weekly)

## 🛠️ Troubleshooting

### **Common Issues:**

1. **Backend not responding**
   - Check environment variables
   - Verify deployment logs
   - Test backend URL directly

2. **Form submissions failing**
   - Check CORS settings
   - Verify backend URL in JavaScript
   - Check browser console for errors

3. **Email not sending**
   - Verify email credentials
   - Check SMTP settings
   - Test with different email provider

### **Debug Steps:**

1. **Test backend directly:**
   ```bash
   curl https://your-backend-url.com/
   ```

2. **Check admin panel:**
   ```bash
   curl https://your-backend-url.com/admin
   ```

3. **Test API endpoint:**
   ```bash
   curl -X POST https://your-backend-url.com/api/register \
        -H "Content-Type: application/json" \
        -d '{"email":"test@example.com","name":"Test User"}'
   ```

## 💰 Cost Breakdown

### **Free Options:**
- **Railway**: Free tier (500 hours/month)
- **PythonAnywhere**: Free tier (limited CPU)
- **Render**: Free tier (limited hours)
- **GitHub Pages**: Completely free

### **Paid Options (if needed):**
- **Railway**: $5/month for unlimited
- **PythonAnywhere**: $5/month for always-on
- **Render**: $7/month for always-on

## 🎯 Final Architecture

```
Frontend (GitHub Pages)
├── https://teknoledg.github.io
├── https://teknoledg.com (custom domain)
└── Form submissions → Backend API

Backend (Your Choice)
├── Railway/PythonAnywhere/Render
├── Python Flask + SQLite
├── Email notifications
└── Admin panel
```

## ✅ Success Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend updated with backend URL
- [ ] Form submissions working
- [ ] Email notifications sending
- [ ] Admin panel accessible
- [ ] Database storing data
- [ ] Custom domain configured (optional)

## 🚀 You're Done!

Your complete self-hosted solution is now running:
- **No third-party services** required
- **Full control** over your data
- **Professional admin panel**
- **Email notifications** to tim@teknoledg.com
- **Database management** capabilities

The system is completely self-contained and professional!
