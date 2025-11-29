# Streamlit Cloud Deployment Troubleshooting Guide

## 🔴 Connection Error: Cannot connect to https://youtoubeseo.streamlit.app

### Possible Causes

1. **App Not Deployed**
   - The app might not have been successfully deployed to Streamlit Cloud
   - The deployment might have failed during the build process

2. **App Crashed**
   - The app might have crashed after deployment
   - Check Streamlit Cloud logs for errors

3. **Incorrect URL**
   - The URL might be incorrect or the app might have been deleted
   - Verify the URL in Streamlit Cloud dashboard

4. **Configuration Issues**
   - Missing or incorrect configuration files
   - Dependency issues in requirements.txt

5. **Repository Issues**
   - Repository might not be public (Streamlit Cloud requires public repos for free tier)
   - Repository might not be connected to Streamlit Cloud

---

## ✅ Step-by-Step Troubleshooting

### Step 1: Verify Streamlit Cloud Deployment

1. **Go to Streamlit Cloud Dashboard**
   - Visit: https://share.streamlit.io
   - Sign in with your GitHub account

2. **Check Your Apps**
   - Look for an app named "youtoubeseo" or similar
   - Check the deployment status:
     - ✅ **Running** - App is deployed and running
     - ⚠️ **Error** - Deployment failed or app crashed
     - 🔄 **Deploying** - Currently deploying

3. **Check App Logs**
   - Click on your app
   - Go to "Logs" or "View logs"
   - Look for error messages

### Step 2: Verify Repository Connection

1. **Check GitHub Repository**
   - Repository: `MoriGrey/-YouTube-SEO-Tool`
   - Ensure it's **public** (Streamlit Cloud free tier requires public repos)
   - Verify the repository exists and is accessible

2. **Check Repository Settings**
   - Go to: https://github.com/MoriGrey/-YouTube-SEO-Tool
   - Settings → General → Scroll to bottom
   - Ensure "Repository visibility" is set to **Public**

### Step 3: Verify Configuration Files

Check that these files exist and are correct:

1. **Procfile** (must exist in root)
   ```
   web: streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **requirements.txt** (must exist in root)
   - Should contain all dependencies
   - No syntax errors

3. **.streamlit/config.toml** (optional but recommended)
   - Should exist in `.streamlit/` directory

4. **dashboard.py** (main file)
   - Should be in root directory
   - Should be the entry point

### Step 4: Check Common Deployment Errors

#### Error: ModuleNotFoundError
**Cause:** Missing dependency in requirements.txt
**Solution:** Add missing package to requirements.txt and redeploy

#### Error: Import Error
**Cause:** Incorrect import paths or missing __init__.py files
**Solution:** Check all import statements and ensure __init__.py files exist

#### Error: Port Already in Use
**Cause:** Procfile configuration issue
**Solution:** Procfile should use `$PORT` environment variable (already correct)

#### Error: API Key Not Found
**Cause:** This is normal - users must enter their own API keys
**Solution:** Not an error - this is expected behavior

### Step 5: Redeploy the App

If the app is not running, try redeploying:

1. **In Streamlit Cloud Dashboard:**
   - Click on your app
   - Click "⋮" (three dots) → "Redeploy"
   - Or delete and recreate the app

2. **Or Create New App:**
   - Click "New app"
   - Select repository: `MoriGrey/-YouTube-SEO-Tool`
   - Branch: `main` or `master`
   - Main file path: `dashboard.py`
   - App URL: Choose a new URL (e.g., `youtube-seo-agi-tool`)
   - Click "Deploy"

### Step 6: Verify Deployment Success

After redeploying:

1. **Wait 2-3 minutes** for deployment to complete
2. **Check the app URL** - it should load
3. **Check logs** - should show "Running on http://0.0.0.0:PORT"
4. **Test the app** - try accessing it in a browser

---

## 🔧 Quick Fixes

### Fix 1: Update Extension URLs

If you redeploy with a new URL, update the extension files:

1. **extension/background.js**
   ```javascript
   const API_BASE_URL = 'https://YOUR-NEW-URL.streamlit.app';
   ```

2. **extension/content.js**
   ```javascript
   apiBaseUrl: 'https://YOUR-NEW-URL.streamlit.app',
   ```

3. **extension/popup.js**
   ```javascript
   const API_BASE_URL = 'https://YOUR-NEW-URL.streamlit.app';
   ```

### Fix 2: Check Python Version

Streamlit Cloud uses Python 3.11 by default. Ensure your code is compatible.

### Fix 3: Verify Dependencies

Run locally to ensure all dependencies work:
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

If it works locally, it should work on Streamlit Cloud.

---

## 📋 Deployment Checklist

Before deploying, ensure:

- [ ] Repository is **public**
- [ ] `Procfile` exists in root
- [ ] `requirements.txt` exists and is up-to-date
- [ ] `dashboard.py` exists in root
- [ ] `.streamlit/config.toml` exists (optional)
- [ ] All imports are correct
- [ ] No hardcoded paths (use relative paths)
- [ ] No local file dependencies (use environment variables or Streamlit Secrets)

---

## 🆘 Still Having Issues?

### Check Streamlit Cloud Status
- Visit: https://status.streamlit.io
- Check if there are any service outages

### Contact Support
- Streamlit Community: https://discuss.streamlit.io
- GitHub Issues: Create an issue in your repository

### Alternative Deployment Options

If Streamlit Cloud continues to have issues, consider:

1. **Railway** (https://railway.app)
   - Free tier available
   - Easy GitHub integration

2. **Render** (https://render.com)
   - Free tier available
   - Good for Streamlit apps

3. **Fly.io** (https://fly.io)
   - Free tier available
   - More control

---

## 📝 Notes

- **Streamlit Cloud Free Tier:**
  - Only supports public GitHub repositories
  - Apps may sleep after inactivity
  - Limited resources

- **App URL:**
  - Format: `https://YOUR-APP-NAME.streamlit.app`
  - Must be unique
  - Cannot be changed after creation (must delete and recreate)

- **Deployment Time:**
  - First deployment: 2-5 minutes
  - Updates: 1-3 minutes
  - Depends on app size and dependencies

---

**Last Updated:** 2025-01-26

