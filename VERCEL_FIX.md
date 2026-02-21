# Fix Vercel Deployment - Registration Page 500 Error

## The Problem
The registration page is returning a 500 error with HTML instead of JSON because:
1. The backend API isn't properly configured
2. Environment variables might not be set
3. Database connection is failing

## Solution Steps

### Step 1: Set Environment Variables in Vercel

Go to your Vercel project dashboard and add these environment variables:

1. Go to: https://vercel.com/dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add the following variables:

```
DB_HOST=your-aiven-mysql-host.aivencloud.com
DB_PORT=your-port (usually 3306)
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=your-database-name
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=1
FLASK_ENV=production
FLASK_DEBUG=False
```

**IMPORTANT**: Make sure to add these to "Production", "Preview", and "Development" environments!

### Step 2: Redeploy

After setting environment variables:

```bash
git add .
git commit -m "Fix Vercel API configuration"
git push origin main
```

Or manually trigger a redeploy in Vercel dashboard.

### Step 3: Check Vercel Logs

1. Go to your Vercel project dashboard
2. Click on "Deployments"
3. Click on the latest deployment
4. Click on "Functions" tab
5. Look for `/api/register` function
6. Check the logs for errors

Common errors:
- **"No module named 'app'"** → Python path issue (fixed in api/index.py)
- **"Can't connect to MySQL server"** → Database credentials wrong or firewall blocking
- **"No environment variable"** → Environment variables not set

### Step 4: Test Locally First

Before deploying, test that everything works locally:

```bash
# Make sure server is running
python run.py

# Test registration in browser
# Open: http://localhost:5000/register.html
```

If it works locally but not on Vercel, the issue is with Vercel configuration.

### Step 5: Alternative - Use Vercel Dev

Test Vercel deployment locally:

```bash
# Install Vercel CLI if not installed
npm install -g vercel

# Run Vercel dev server
vercel dev
```

This will simulate the Vercel environment locally and help you debug.

## Quick Checklist

- [ ] Environment variables set in Vercel dashboard
- [ ] Database allows connections from Vercel IPs
- [ ] `api/index.py` exists and is correct
- [ ] `api/requirements.txt` exists
- [ ] `vercel.json` is configured correctly
- [ ] Code is pushed to Git
- [ ] Redeployed after changes

## Still Not Working?

### Check Database Connection

Your Aiven MySQL database might be blocking Vercel's IP addresses. To fix:

1. Go to Aiven console
2. Find your MySQL service
3. Check "Allowed IP Addresses"
4. Add `0.0.0.0/0` (allow all) for testing
5. Later, restrict to Vercel's IP ranges

### Check Function Logs

In Vercel dashboard:
1. Go to your deployment
2. Click "Functions" tab
3. Click on the `/api/register` function
4. Look for error messages

### Test API Directly

Try calling the API directly:

```bash
curl -X POST https://your-app.vercel.app/api/register \
  -H "Content-Type: application/json" \
  -d '{"uid":"test","uname":"testuser","password":"test1234","email":"test@test.com","phone":"1234567890"}'
```

This should return JSON, not HTML.

## Alternative Deployment Options

If Vercel continues to have issues, consider:

1. **Railway** (https://railway.app) - Better for Python/Flask apps
2. **Render** (https://render.com) - Free tier for web services
3. **PythonAnywhere** (https://www.pythonanywhere.com) - Specialized for Python
4. **Heroku** (https://heroku.com) - Classic PaaS (paid)

All of these are easier for Flask apps than Vercel.
