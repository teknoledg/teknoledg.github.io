# 🚀 Vercel Deployment Guide

## 📋 **Step-by-Step Deployment:**

### **1. Create Vercel Account**
- Go to [vercel.com](https://vercel.com)
- Sign up with GitHub account
- Connect your `teknoledg` GitHub account

### **2. Deploy API**
- Go to [vercel.com/dashboard](https://vercel.com/dashboard)
- Click "New Project"
- Import from GitHub: `teknoledg/teknoledg.github.io`
- **Root Directory**: Leave empty (deploy from root)
- **Framework Preset**: Other
- Click "Deploy"

### **3. Setup Database**
- Go to your project dashboard
- Click "Storage" tab
- Click "Create Database"
- Choose "Postgres"
- Name: `teknoledg-db`
- Click "Create"

### **4. Get Connection String**
- In Storage tab, click on your database
- Go to "Settings" tab
- Copy the "Connection String"
- It looks like: `postgres://username:password@host:port/database`

### **5. Add Environment Variable**
- Go to project "Settings" tab
- Click "Environment Variables"
- Add new variable:
  - **Name**: `POSTGRES_URL`
  - **Value**: (paste connection string)
  - **Environment**: Production
- Click "Save"

### **6. Create Database Table**
- Go to your database dashboard
- Click "Query" tab
- Run this SQL:

```sql
CREATE TABLE IF NOT EXISTS registrations (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **7. Redeploy**
- Go to "Deployments" tab
- Click "Redeploy" on latest deployment
- Wait for deployment to complete

## 🔗 **Your API URLs:**
- **Registration**: `https://your-project.vercel.app/api/register`
- **Admin Panel**: `https://your-project.vercel.app/api/admin`
- **Registrations**: `https://your-project.vercel.app/api/registrations`

## 🧪 **Test Your API:**
1. Visit admin panel URL
2. Login: `admin` / `teknoledg2024`
3. Test form submission on your site
4. Check registrations in admin panel

## ✅ **Success Indicators:**
- ✅ API responds without errors
- ✅ Admin panel loads and shows login
- ✅ Form submissions work
- ✅ Registrations appear in admin panel
