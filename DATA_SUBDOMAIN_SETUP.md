# 🗄️ Data.teknoledg.com Subdomain Configuration

## Perfect! Using data.teknoledg.com for Your Backend

This is an excellent setup - using `data.teknoledg.com` for your backend API and database services while keeping the main site on `teknoledg.com`.

## 🎯 Architecture Overview

```
Frontend (teknoledg.com)
├── https://teknoledg.com (main site)
├── https://www.teknoledg.com (main site)
└── Form submissions → data.teknoledg.com

Backend (data.teknoledg.com)
├── https://data.teknoledg.com (API endpoint)
├── https://data.teknoledg.com/admin (admin panel)
├── Database (your existing)
└── Email (your existing)
```

## 🚀 Quick Setup

### **Step 1: Deploy Backend to data.teknoledg.com**

```bash
# Run the data subdomain deployment script
./deploy_data_subdomain.sh
```

### **Step 2: Configure DNS in Names.co.uk**

Add these DNS records in your names.co.uk control panel:

```
Record Type: A
Name: data
Value: YOUR_SERVER_IP
TTL: 300

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

### **Step 3: Update Frontend Configuration**

The frontend will automatically use `data.teknoledg.com` as the backend URL.

## 🔧 DNS Configuration for Names.co.uk

### **Main Domain (teknoledg.com):**
- **A Records**: Point to GitHub Pages IPs
- **CNAME**: www → teknoledg.github.io

### **Data Subdomain (data.teknoledg.com):**
- **A Record**: Point to your server IP
- **SSL**: Configure SSL certificate

## 📧 Email Configuration

### **Using Your Existing Email System:**
```env
SMTP_SERVER=mail.teknoledg.com
SMTP_PORT=587
EMAIL_USER=noreply@teknoledg.com
EMAIL_PASSWORD=your_email_password
```

### **Email Notifications:**
- **From**: noreply@teknoledg.com
- **To**: tim@teknoledg.com
- **Subject**: New Registration - {email}

## 🗄️ Database Integration

### **Uses Your Existing Database:**
- **Host**: Your existing database server
- **Database**: Your existing database
- **Table**: `registrations` (will be created)

### **Database Schema:**
```sql
CREATE TABLE registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔐 Security Configuration

### **CORS Settings:**
```python
CORS(app, origins=[
    'https://teknoledg.com',
    'https://www.teknoledg.com',
    'https://teknoledg.github.io'
])
```

### **SSL Configuration:**
- **Main site**: GitHub Pages (automatic SSL)
- **Data subdomain**: Your server SSL certificate

## 🛠️ Deployment Process

### **Step 1: Deploy Backend**

```bash
# Upload backend files to your server
scp -r backend/ user@your-server.com:/var/www/data.teknoledg.com/

# Configure server
ssh user@your-server.com "cd /var/www/data.teknoledg.com && chmod +x app_existing_db.py"
```

### **Step 2: Configure SSL**

```bash
# Get SSL certificate for data.teknoledg.com
sudo certbot --nginx -d data.teknoledg.com
```

### **Step 3: Update Frontend**

The frontend will automatically use `data.teknoledg.com` as the backend URL.

## 📊 Admin Panel

### **Access:**
- **URL**: https://data.teknoledg.com/admin
- **Username**: admin
- **Password**: Your configured password

### **Features:**
- **View Registrations**: All user signups
- **Export Data**: CSV download
- **Delete Entries**: Remove unwanted registrations
- **Statistics**: Total, daily, weekly counts

## 🔄 Form Submission Flow

1. **User visits**: https://teknoledg.com
2. **Submits form**: JavaScript sends data to data.teknoledg.com
3. **Backend processes**: Stores in your database
4. **Email sent**: Notification to tim@teknoledg.com
5. **Success message**: User sees confirmation

## 🌐 Final URLs

After deployment:
- **Main site**: https://teknoledg.com
- **Backend API**: https://data.teknoledg.com
- **Admin panel**: https://data.teknoledg.com/admin
- **Form endpoint**: https://data.teknoledg.com/api/register

## ✅ Benefits of This Setup

### **✅ Clean Separation:**
- **Frontend**: GitHub Pages (free, fast, reliable)
- **Backend**: Your server (full control, existing infrastructure)

### **✅ Professional Setup:**
- **Custom domain**: teknoledg.com
- **API subdomain**: data.teknoledg.com
- **SSL certificates**: Both domains secured

### **✅ Cost Effective:**
- **Frontend**: Free (GitHub Pages)
- **Backend**: Uses your existing server
- **No additional hosting**: Leverages your infrastructure

### **✅ Scalable:**
- **Frontend**: GitHub Pages scales automatically
- **Backend**: Your server infrastructure
- **Database**: Your existing database system

## 🚀 Quick Start

```bash
# Run the complete setup
./deploy_data_subdomain.sh

# Follow the prompts to:
# 1. Configure your server details
# 2. Set up DNS records in names.co.uk
# 3. Deploy the backend
# 4. Test the integration
```

## 📞 Support

If you need help:
- **Names.co.uk**: Contact their support for DNS configuration
- **Server setup**: Check your hosting provider documentation
- **SSL certificates**: Use Let's Encrypt for free SSL

Your data.teknoledg.com subdomain setup is ready to go!
