# Deployment Guide for Render

## Step 1: Push to GitHub
```bash
git add .
git commit -m "Add Flask backend with PostgreSQL"
git push origin main
```

## Step 2: Deploy to Render

### Create Web Service
1. Go to https://render.com
2. Click "New" → "Web Service"
3. Connect your GitHub repository (`portifolio`)
4. Fill in:
   - **Name:** `portifolio-backend` (or any name)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn server.app:app`
   - **Plan:** Free (if available) or Paid

### Add PostgreSQL Database
1. Click "New" → "PostgreSQL"
2. Name: `portifolio-db`
3. Click Create

### Connect Database
1. Go to your Web Service settings
2. Add Environment Variable:
   - **Key:** `DATABASE_URL`
   - **Value:** Copy from PostgreSQL instance "Internal Database URL"
3. Click "Save"

### Deploy
- Click "Deploy" in the Web Service

## Step 3: Update Frontend
Once deployed, Render will give you a URL like: `https://portifolio-backend.onrender.com`

Update the frontend accordingly or the JavaScript will auto-detect it.

## API Endpoints

### Submit Contact Form
```
POST /submit
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91-XXXXX-XXXXX",
  "subject": "Web Development",
  "message": "I need a website..."
}
```

Response:
```json
{
  "status": "success",
  "message": "Saved successfully",
  "id": 1
}
```

### Get All Contacts (Admin)
```
GET /contacts
```

### Export to Excel
```
GET /export
```

## Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python server/app.py

# Access at http://localhost:5000
```

## Troubleshooting

### "Database connection failed"
- Ensure DATABASE_URL env var is set
- Restart the service

### "Module not found"
- Run: `pip install -r requirements.txt`
- Check Render logs

### Form not submitting
- Check browser console for errors
- Verify backend URL is correct
