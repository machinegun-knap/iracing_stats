# Railway Deployment Guide for iRacing Discord Bot

## Quick Setup (5 minutes)

### Step 1: Prepare Your Files

1. **Create a GitHub account** if you don't have one: https://github.com
2. **Create a new repository** (can be private)
3. **Upload these files** to your repository:
   - `iracing_discord_bot.py`
   - `requirements.txt`
   - `README.md`

### Step 2: Create Railway Account

1. Go to https://railway.app
2. Click **"Start a New Project"** or **"Login"**
3. Sign up with your **GitHub account** (easiest method)
4. Railway will ask for GitHub permissions - approve them

### Step 3: Deploy Your Bot

1. On Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your bot repository
4. Railway will automatically detect it's a Python project

### Step 4: Add Environment Variable

1. In your Railway project, go to the **"Variables"** tab
2. Click **"New Variable"**
3. Add:
   - **Variable name:** `DISCORD_BOT_TOKEN`
   - **Value:** Your Discord bot token (from Discord Developer Portal)
4. Click **"Add"**

### Step 5: Deploy!

1. Railway will automatically build and deploy your bot
2. Check the **"Deployments"** tab to see progress
3. Once it shows **"Success"** with a green checkmark, your bot is live!
4. Go to **"Logs"** tab to see your bot running

## Verify It's Working

1. Go to your Discord server
2. Type `!help_iracing`
3. Your bot should respond!

## Managing Your Bot

### View Logs
- Go to your Railway project → **"Logs"** tab
- See real-time bot activity

### Update Your Bot
- Push changes to your GitHub repository
- Railway automatically redeploys

### Stop/Start Bot
- **Settings** tab → **"Service"** section
- You can pause or restart the service

## Free Tier Limits

Railway free tier includes:
- **$5 in credits per month** OR **500 execution hours**
- Your bot will use about **720 hours/month** if running 24/7
- **Solution:** Railway charges ~$1-3/month for a simple bot, or use the $5 credit

## Troubleshooting

### Bot shows "Deployed" but isn't online in Discord
- Check **Logs** tab for errors
- Verify `DISCORD_BOT_TOKEN` is set correctly
- Make sure bot is invited to your server with correct permissions

### "No module named discord" error
- Make sure `requirements.txt` is in your repository
- Railway should auto-install dependencies

### Bot disconnects randomly
- Check Railway credit balance
- Free tier may have limitations

### Need to see tracked drivers file
- Railway has persistent storage
- `tracked_drivers.json` is automatically created and saved

## Alternative: Deploy via Railway CLI

If you prefer command line:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variable
railway variables set DISCORD_BOT_TOKEN=your_token_here

# Deploy
railway up
```

## Next Steps

1. Test the bot with `!test_result YourName`
2. Track a driver with `!track_driver YourName`
3. When ready, implement real iRacing API in the code
4. Push updates to GitHub - Railway auto-deploys!

## Cost Estimate

- **First month:** Free (using $5 credit)
- **Ongoing:** ~$1-3/month for 24/7 uptime
- **Alternative:** Use free tier by running bot only when needed

## Support

- Railway docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Check bot logs in Railway for debugging

---

**Pro tip:** Keep your GitHub repository private if your bot code contains sensitive information!
