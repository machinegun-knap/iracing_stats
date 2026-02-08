# iRacing Discord Bot

A Discord bot for iRacing enthusiasts to check stats, schedules, track information, and **automatically post race results**.

## Features

- 🏁 **Automatic Race Results Posting** - Bot monitors drivers and posts results automatically
- 📊 Driver statistics lookup
- 🏎️ Track information
- 📅 Weekly race schedule
- ⚔️ Driver comparisons
- 🤖 Easy-to-use commands

## Setup Instructions

### 1. Install Python
Make sure you have Python 3.8 or higher installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a Discord Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - MESSAGE CONTENT INTENT
   - SERVER MEMBERS INTENT
5. Copy your bot token (keep it secret!)

### 4. Set Up Your Bot Token
Create a `.env` file in the same directory as the bot:
```
DISCORD_BOT_TOKEN=your_token_here
```

Or set it as an environment variable:
```bash
export DISCORD_BOT_TOKEN=your_token_here
```

### 5. Invite the Bot to Your Server
1. In Discord Developer Portal, go to "OAuth2" > "URL Generator"
2. Select scopes: `bot` and `applications.commands`
3. Select permissions: `Send Messages`, `Embed Links`, `Read Message History`
4. Copy the generated URL and open it in your browser
5. Select your server and authorize

### 6. Run the Bot
```bash
python iracing_discord_bot.py
```

## Available Commands

### Auto Race Results (NEW!)
- `!track_driver [username]` - Start automatically posting race results for a driver
- `!untrack_driver [username]` - Stop tracking a driver
- `!tracked_drivers` - List all tracked drivers
- `!test_result [username]` - Post a sample race result (for testing)

### General Commands
- `!stats [username]` - Get driver statistics
- `!series` - View active racing series
- `!track [name]` - Get track information
- `!schedule` - View this week's schedule
- `!compare [driver1] [driver2]` - Compare two drivers
- `!help_iracing` - Show help message

## How Auto Race Results Work

The bot checks for new race results every 5 minutes for any tracked drivers. When a driver completes a race, the bot automatically posts:

- Finish position and starting position
- Field size
- Incidents
- iRating change (with ⬆️ or ⬇️ indicator)
- Safety Rating change
- Race time
- Championship points
- Special badges for victories and podium finishes

**Example:**
```
!track_driver JohnDoe
```
Now whenever JohnDoe finishes a race, the bot will automatically post the results to your channel!

## Example Usage

### Tracking Race Results
```
!track_driver JohnDoe
# Bot will now automatically post race results for JohnDoe

!tracked_drivers
# See who's being tracked

!test_result JohnDoe
# Post a sample result to see what it looks like

!untrack_driver JohnDoe
# Stop tracking
```

### Other Commands
```
!stats JohnDoe
!track Spa-Francorchamps
!compare Alice Bob
!schedule
```

## Note About iRacing API

This bot currently uses placeholder data. To get real iRacing data, you'll need to:

1. **Get iRacing API credentials**: iRacing requires authentication for their API
2. **Implement API calls**: The iRacing Data API is available at `https://members-ng.iracing.com`
3. **Add authentication**: You'll need to handle login and session management

### Connecting to Real iRacing Data

iRacing uses a session-based authentication system. You'll need to:
- Create an iRacing account
- Use their login endpoint to get a session cookie
- Make authenticated requests to their API endpoints

Check out the [iRacing API documentation](https://forums.iracing.com/discussion/15068/general-availability-of-data-api/) for more details.

### Implementing Auto Race Results

The bot includes a background task that checks every 5 minutes. To connect it to real data:

1. **Authenticate with iRacing API**
   ```python
   # Add authentication in fetch_latest_race() function
   async with aiohttp.ClientSession() as session:
       # Login to iRacing
       # Get session cookie
       # Query for recent races
   ```

2. **Fetch Race Results**
   - Use the `/data/results/search` endpoint to find recent races
   - Compare with stored `last_race_id` to detect new races
   - Retrieve full race details when new race is found

3. **The bot already handles**
   - Storing tracked drivers (saved to `tracked_drivers.json`)
   - Background monitoring every 5 minutes
   - Posting formatted results with embeds
   - Track/untrack commands

## Customization

Feel free to modify the bot to add:
- League-specific features
- Race result tracking
- Livery sharing
- Event notifications
- Custom commands for your community

## Support

If you encounter issues:
1. Make sure all dependencies are installed
2. Verify your bot token is correct
3. Check that the bot has proper permissions in your Discord server
4. Ensure you've enabled the required intents in the Discord Developer Portal

## License

Free to use and modify for your iRacing community!
