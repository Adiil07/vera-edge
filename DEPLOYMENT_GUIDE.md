# 🚀 VERA EDGE — Deployment Guide
## From Zero to Live URL in 20 Minutes (Using FREE Groq API)

---

## ✅ STEP 1: Get Your FREE Groq API Key (3 mins)

1. Open browser → go to **console.groq.com**
2. Click **"Sign Up"** → use your Google account (fastest)
3. Once logged in, click **"API Keys"** on the left
4. Click **"Create API Key"**
5. Give it any name → click **"Submit"**
6. **COPY the key** — it starts with `gsk_...`
7. Paste it in Notes app or anywhere safe

✅ Done! This is 100% FREE. No credit card needed.

---

## ✅ STEP 2: Install Python (If Not Already)

Open **Terminal** (Mac) or **Command Prompt** (Windows):

```bash
python --version
```

If you see `Python 3.x.x` → skip this step ✅

If you see an error:
- Go to **python.org/downloads**
- Download latest version → Install
- Restart terminal and try again

---

## ✅ STEP 3: Test The Bot Locally First

Open terminal, navigate to your vera-edge folder:

```bash
# Go into the folder
cd vera-edge-groq

# Install packages
pip install -r requirements.txt

# Set your Groq API key
# On Mac/Linux:
export GROQ_API_KEY=gsk_your_key_here

# On Windows:
set GROQ_API_KEY=gsk_your_key_here

# Start the bot
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open a NEW terminal window and test:

```bash
curl http://localhost:8000/v1/healthz
```

You should see:
```json
{"status": "ok", "uptime_seconds": 5, ...}
```

If you see this → bot works locally ✅

Press `Ctrl+C` to stop the local server.

---

## ✅ STEP 4: Push To GitHub (5 mins)

In terminal, inside your vera-edge-groq folder:

```bash
git init
git add .
git commit -m "Vera Edge - magicpin AI Challenge"
```

Now on **github.com**:
1. Click **"+"** → **"New repository"**
2. Name: `vera-edge`
3. Set to **Public** ← IMPORTANT
4. Do NOT check "Add README" (we have one)
5. Click **"Create repository"**

GitHub will show you 2 commands. Copy and run them:
```bash
git remote add origin https://github.com/YOUR_USERNAME/vera-edge.git
git push -u origin main
```

Enter your GitHub username and password if asked.

✅ Your code is now on GitHub!

---

## ✅ STEP 5: Deploy on Railway (10 mins)

### 5a. Create Railway Account
1. Go to **railway.app**
2. Click **"Login"** → **"Login with GitHub"**
3. Authorize Railway

### 5b. Create New Project
1. Click **"New Project"**
2. Click **"Deploy from GitHub repo"**
3. Select your `vera-edge` repository
4. Click **"Deploy Now"**
5. Wait 2-3 minutes for build to complete

### 5c. Add Your API Key ← CRITICAL STEP
1. Click on your deployed service (the box that appeared)
2. Click **"Variables"** tab at the top
3. Click **"New Variable"**
4. Fill in:
   - **NAME:** `GROQ_API_KEY`
   - **VALUE:** paste your `gsk_...` key
5. Press **Enter**
6. Railway will automatically redeploy (1-2 mins)

### 5d. Get Your Live URL
1. Click **"Settings"** tab
2. Under **"Networking"** → **"Public Networking"**
3. Click **"Generate Domain"**
4. Copy your URL — looks like:
   `https://vera-edge-production.up.railway.app`

---

## ✅ STEP 6: Verify Everything Works

In terminal, run this (replace with YOUR Railway URL):

```bash
curl https://YOUR-RAILWAY-URL/v1/healthz
```

Expected response:
```json
{"status": "ok", "uptime_seconds": 120, "contexts_loaded": {...}}
```

Also test metadata:
```bash
curl https://YOUR-RAILWAY-URL/v1/metadata
```

If both work → **YOUR BOT IS LIVE AND READY!** 🎉

---

## ✅ STEP 7: Submit To magicpin

1. Go to **partners.magicpin.in/vera/ai-challenge**
2. Scroll down to find **"Apply Now"** or **"Submit"** button
3. Fill in:
   - Full Name: Adil
   - Email: your email
   - Phone: your number
   - Bot URL: `https://YOUR-RAILWAY-URL`
4. Click **Submit** 🏆

---

## ⚠️ KEEP YOUR BOT RUNNING

**DO NOT** close Railway or delete your project until **May 5, 2026**
The judges will test your live URL during evaluation period.

---

## 🆘 Common Problems & Fixes

### Problem: Railway build fails
**Fix:** Check logs → Click "Deployments" → "View Logs"
Usually means a package install failed. Share the error with me.

### Problem: Bot returns error when tested
**Fix:** GROQ_API_KEY is probably missing or wrong in Variables tab
Go back to Step 5c and re-add it carefully

### Problem: "Module not found" error
**Fix:** Run `pip install -r requirements.txt` again locally first

### Problem: Railway URL not working
**Fix:** Wait 3-4 minutes after deployment finishes
Then try curl again

---

## 📅 KEY DATES TO REMEMBER

| Date | What |
|------|------|
| Now | Deploy and submit |
| May 2, 11:59 PM IST | Submission deadline |
| May 2 - May 5 | Judges test your bot LIVE |
| May 5 | Results announced |

---

## 🏆 You're Ready. Let's Win This.

Once you have your Railway URL, message me.
I'll do a final verification test with you before you submit.
