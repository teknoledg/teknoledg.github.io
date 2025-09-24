# 🌐 Names.co.uk Domain Configuration Guide

## Perfect! Let's Set Up Your Domain with Names.co.uk

Since you're registered with names.co.uk, this guide will help you configure your domain to work with your registration system.

## 🎯 Domain Setup Options

### **Option 1: Use Your Existing Hosting (Recommended)**

If you already have hosting with names.co.uk or another provider:

#### **Step 1: Configure DNS Records**

Log into your names.co.uk control panel and set up these DNS records:

```
Type: A
Name: @
Value: YOUR_SERVER_IP_ADDRESS

Type: A  
Name: www
Value: YOUR_SERVER_IP_ADDRESS

Type: CNAME
Name: api
Value: YOUR_SERVER_IP_ADDRESS
```

#### **Step 2: Deploy Your Application**

Upload your application files to your hosting and configure:

```bash
# Upload files to your server
scp -r backend/ user@your-server.com:/var/www/teknoledg.com/
scp -r css/ user@your-server.com:/var/www/teknoledg.com/
scp -r js/ user@your-server.com:/var/www/teknoledg.com/
scp -r images/ user@your-server.com:/var/www/teknoledg.com/
scp index.html user@your-server.com:/var/www/teknoledg.com/
```

---

### **Option 2: GitHub Pages + Custom Domain**

Use GitHub Pages for the frontend and your existing server for the backend:

#### **Step 1: Configure GitHub Pages**

1. Go to your GitHub repository settings
2. Enable GitHub Pages
3. Set source to "Deploy from a branch"
4. Select "main" branch and "/docs" folder

#### **Step 2: Set Up Custom Domain**

In GitHub Pages settings:
- **Custom domain**: teknoledg.com
- **Enforce HTTPS**: ✅

#### **Step 3: Configure DNS Records**

In your names.co.uk control panel:

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

Type: A
Name: api
Value: YOUR_BACKEND_SERVER_IP
```

---

### **Option 3: Subdomain Setup**

Use subdomains to separate frontend and backend:

#### **DNS Configuration:**
```
Type: A
Name: @
Value: YOUR_SERVER_IP

Type: A
Name: www
Value: YOUR_SERVER_IP

Type: A
Name: api
Value: YOUR_SERVER_IP
```

#### **URL Structure:**
- **Main site**: https://teknoledg.com
- **API backend**: https://api.teknoledg.com
- **Admin panel**: https://api.teknoledg.com/admin

---

## 🔧 Names.co.uk Control Panel Setup

### **Step 1: Access DNS Management**

1. Log into your names.co.uk account
2. Go to "My Domains"
3. Click on teknoledg.com
4. Select "DNS Management" or "Advanced DNS"

### **Step 2: Configure DNS Records**

#### **For GitHub Pages (Recommended):**
```
Record Type: A
Name: @
Value: 185.199.108.153
TTL: 300

Record Type: A  
Name: @
Value: 185.199.109.153
TTL: 300

Record Type: A
Name: @
Value: 185.199.110.153
TTL: 300

Record Type: A
Name: @
Value: 185.199.111.153
TTL: 300

Record Type: CNAME
Name: www
Value: teknoledg.github.io
TTL: 300
```

#### **For Your Own Server:**
```
Record Type: A
Name: @
Value: YOUR_SERVER_IP
TTL: 300

Record Type: A
Name: www
Value: YOUR_SERVER_IP
TTL: 300

Record Type: A
Name: api
Value: YOUR_SERVER_IP
TTL: 300
```

---

## 🚀 Complete Deployment Process

### **Step 1: Choose Your Setup**

#### **Option A: GitHub Pages + Your Server**
```bash
# Deploy frontend to GitHub Pages
./setup-github-pages.sh
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main

# Deploy backend to your server
./deploy_existing_infrastructure.sh
```

#### **Option B: Everything on Your Server**
```bash
# Deploy everything to your server
./deploy_existing_infrastructure.sh
```

### **Step 2: Configure DNS**

1. **Log into names.co.uk**
2. **Go to DNS Management**
3. **Add the DNS records** (see above)
4. **Wait for propagation** (up to 24 hours)

### **Step 3: Set Up SSL**

#### **For GitHub Pages:**
- SSL is automatic
- GitHub handles certificates

#### **For Your Server:**
```bash
# Install Certbot for Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d teknoledg.com -d www.teknoledg.com
```

---

## 📧 Email Configuration

### **Using Your Existing Email System:**

#### **Step 1: Configure SMTP**
```env
SMTP_SERVER=mail.teknoledg.com
SMTP_PORT=587
EMAIL_USER=noreply@teknoledg.com
EMAIL_PASSWORD=your_email_password
```

#### **Step 2: Test Email**
```bash
python3 -c "
import smtplib
server = smtplib.SMTP('mail.teknoledg.com', 587)
server.starttls()
server.login('noreply@teknoledg.com', 'your_password')
print('Email configuration successful!')
server.quit()
"
```

---

## 🔐 Security Configuration

### **SSL Certificates:**
- **GitHub Pages**: Automatic SSL
- **Your Server**: Let's Encrypt certificates
- **Force HTTPS**: Redirect HTTP to HTTPS

### **CORS Configuration:**
```python
# In your Flask app
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://teknoledg.com', 'https://www.teknoledg.com'])
```

### **Admin Panel Security:**
- **Password protection**
- **Session management**
- **IP logging**

---

## 🛠️ Troubleshooting

### **Common Issues:**

1. **DNS Not Propagating**
   - Wait up to 24 hours
   - Check DNS propagation: https://dnschecker.org
   - Verify DNS records in names.co.uk

2. **SSL Certificate Issues**
   - Check domain configuration
   - Verify DNS propagation
   - Test with SSL checker

3. **CORS Errors**
   - Configure CORS settings
   - Check domain configuration
   - Verify SSL certificates

### **Debug Steps:**

1. **Check DNS Propagation:**
   ```bash
   nslookup teknoledg.com
   dig teknoledg.com
   ```

2. **Test SSL:**
   ```bash
   curl -I https://teknoledg.com
   ```

3. **Check Backend:**
   ```bash
   curl https://api.teknoledg.com/api/stats
   ```

---

## 📊 Final Architecture

### **Option 1: GitHub Pages + Your Server**
```
Frontend (GitHub Pages)
├── https://teknoledg.com
├── https://www.teknoledg.com
└── Form submissions → Your Server

Your Server
├── https://api.teknoledg.com
├── Database (your existing)
├── Email (your existing)
└── Admin panel
```

### **Option 2: Everything on Your Server**
```
Your Server
├── https://teknoledg.com (frontend)
├── https://teknoledg.com/api (backend)
├── Database (your existing)
├── Email (your existing)
└── Admin panel
```

---

## ✅ Success Checklist

- [ ] DNS records configured in names.co.uk
- [ ] Domain pointing to correct server
- [ ] SSL certificate working
- [ ] Frontend accessible
- [ ] Backend API working
- [ ] Form submissions working
- [ ] Email notifications sending
- [ ] Admin panel accessible

## 🎯 Next Steps

1. **Choose your deployment option**
2. **Configure DNS in names.co.uk**
3. **Deploy your application**
4. **Test everything**
5. **Go live!**

Your domain is ready to be configured with names.co.uk!
