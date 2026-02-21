# Kodbank Vercel Deployment Guide

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install globally
   ```bash
   npm install -g vercel
   ```
3. **Git Repository**: Push your code to GitHub, GitLab, or Bitbucket

## Important Notes

⚠️ **Database Consideration**: Your app uses MySQL (Aiven). Vercel serverless functions work well with this, but ensure:
- Your Aiven database allows connections from Vercel's IP ranges
- Connection pooling is properly configured
- Environment variables are set in Vercel

## Deployment Steps

### Step 1: Prepare Your Project

1. Ensure all files are committed to Git:
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

### Step 2: Configure Environment Variables

Create a `.env.production` file (don't commit this):

```env
# Database Configuration
DB_HOST=your-aiven-host.aivencloud.com
DB_PORT=your-port
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=your-database-name

# JWT Configuration
JWT_SECRET_KEY=your-production-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=1

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
```

### Step 3: Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard (Easiest)

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "Add New Project"
3. Import your Git repository
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: (leave empty)
   - **Output Directory**: frontend
5. Add Environment Variables:
   - Go to "Environment Variables" section
   - Add all variables from `.env.production`
6. Click "Deploy"

#### Option B: Deploy via CLI

1. Login to Vercel:
   ```bash
   vercel login
   ```

2. Deploy:
   ```bash
   vercel
   ```

3. Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? (select your account)
   - Link to existing project? **N**
   - Project name? **kodbank**
   - Directory? **./
   - Override settings? **N**

4. Add environment variables:
   ```bash
   vercel env add DB_HOST
   vercel env add DB_PORT
   vercel env add DB_USER
   vercel env add DB_PASSWORD
   vercel env add DB_NAME
   vercel env add JWT_SECRET_KEY
   ```

5. Deploy to production:
   ```bash
   vercel --prod
   ```

### Step 4: Update Frontend API URLs

After deployment, update your frontend to use the Vercel URL:

In `frontend/js/dashboard.js`, `frontend/js/login.js`, and `frontend/js/register.js`:

```javascript
// Change from:
const response = await fetch('/api/balance', {

// To:
const response = await fetch('https://your-app.vercel.app/api/balance', {
```

Or better, use environment-based URLs:

```javascript
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000' 
  : 'https://your-app.vercel.app';

const response = await fetch(`${API_BASE_URL}/api/balance`, {
```

### Step 5: Configure CORS

Update `backend/app.py` CORS configuration to include your Vercel domain:

```python
CORS(app, 
     origins=[
         'http://localhost:3000', 
         'http://localhost:5500', 
         'http://127.0.0.1:5500', 
         'http://127.0.0.1:3000',
         'https://your-app.vercel.app',  # Add your Vercel domain
         'https://*.vercel.app'  # Allow preview deployments
     ],
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
)
```

## Alternative: Deploy Backend Separately

If Vercel serverless doesn't work well for your Flask app, consider:

### Option 1: Backend on Railway/Render + Frontend on Vercel

1. **Backend**: Deploy Flask to [Railway](https://railway.app) or [Render](https://render.com)
2. **Frontend**: Deploy static files to Vercel
3. Update frontend API URLs to point to your backend URL

### Option 2: Backend on PythonAnywhere

1. Deploy Flask to [PythonAnywhere](https://www.pythonanywhere.com)
2. Deploy frontend to Vercel
3. Update CORS and API URLs

## Troubleshooting

### Issue: Database Connection Timeout

**Solution**: 
- Check Aiven firewall settings
- Increase connection timeout in `backend/db.py`
- Use connection pooling

### Issue: CORS Errors

**Solution**:
- Ensure Vercel domain is in CORS origins
- Check that credentials are properly configured
- Verify cookies are being sent with requests

### Issue: Cold Starts

**Solution**:
- Vercel serverless functions have cold starts
- Consider keeping database connections warm
- Use Vercel's Edge Functions for faster response

## Monitoring

After deployment:

1. Check Vercel Dashboard for:
   - Deployment logs
   - Function logs
   - Analytics

2. Monitor your Aiven database:
   - Connection count
   - Query performance
   - Error logs

## Custom Domain (Optional)

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update CORS configuration with new domain

## Continuous Deployment

Vercel automatically deploys when you push to your Git repository:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Vercel will automatically build and deploy your changes.

## Security Checklist

- ✅ Environment variables set in Vercel (not in code)
- ✅ JWT secret is strong and unique
- ✅ Database credentials are secure
- ✅ CORS is properly configured
- ✅ HTTPS is enabled (automatic with Vercel)
- ✅ Security headers are configured in Flask

## Support

- Vercel Docs: https://vercel.com/docs
- Vercel Community: https://github.com/vercel/vercel/discussions
- Flask on Vercel: https://vercel.com/guides/using-flask-with-vercel

---

**Note**: Vercel's free tier has limitations on serverless function execution time (10 seconds) and invocations. For production apps with high traffic, consider upgrading to a paid plan or using a dedicated Python hosting service.
