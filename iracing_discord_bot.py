import discord
from discord.ext import commands, tasks
import aiohttp
import os
import json
from datetime import datetime

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Storage for tracked drivers and channels
tracked_drivers = {}  # {driver_id: {"username": str, "channel_id": int, "last_race_id": int}}
TRACKED_DRIVERS_FILE = "tracked_drivers.json"

def load_tracked_drivers():
    """Load tracked drivers from file"""
    global tracked_drivers
    try:
        if os.path.exists(TRACKED_DRIVERS_FILE):
            with open(TRACKED_DRIVERS_FILE, 'r') as f:
                tracked_drivers = json.load(f)
    except Exception as e:
        print(f"Error loading tracked drivers: {e}")
        tracked_drivers = {}

def save_tracked_drivers():
    """Save tracked drivers to file"""
    try:
        with open(TRACKED_DRIVERS_FILE, 'w') as f:
            json.dump(tracked_drivers, f, indent=2)
    except Exception as e:
        print(f"Error saving tracked drivers: {e}")

# iRacing API base URL (note: iRacing requires authentication)
IRACING_API_BASE = "https://members-ng.iracing.com"

@bot.command(name='track_driver', help='Start tracking race results for a driver (!track_driver username)')
async def track_driver(ctx, driver_name: str):
    """Start automatically posting race results for a driver"""
    # In production, you'd validate the driver exists via iRacing API
    # For now, we'll use the driver name as a simple ID
    driver_id = driver_name.lower()
    
    tracked_drivers[driver_id] = {
        "username": driver_name,
        "channel_id": ctx.channel.id,
        "last_race_id": None
    }
    save_tracked_drivers()
    
    embed = discord.Embed(
        title="✅ Driver Tracking Enabled",
        description=f"Now tracking race results for **{driver_name}**",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Results will be posted to",
        value=ctx.channel.mention,
        inline=False
    )
    embed.add_field(
        name="Check interval",
        value="Every 5 minutes",
        inline=False
    )
    embed.set_footer(text="Use !untrack_driver to stop tracking")
    
    await ctx.send(embed=embed)

@bot.command(name='untrack_driver', help='Stop tracking race results for a driver (!untrack_driver username)')
async def untrack_driver(ctx, driver_name: str):
    """Stop automatically posting race results for a driver"""
    driver_id = driver_name.lower()
    
    if driver_id in tracked_drivers:
        del tracked_drivers[driver_id]
        save_tracked_drivers()
        await ctx.send(f"✅ Stopped tracking race results for **{driver_name}**")
    else:
        await ctx.send(f"❌ **{driver_name}** is not currently being tracked")

@bot.command(name='tracked_drivers', help='List all tracked drivers')
async def list_tracked(ctx):
    """Show all currently tracked drivers"""
    if not tracked_drivers:
        await ctx.send("No drivers are currently being tracked. Use `!track_driver [username]` to start tracking.")
        return
    
    embed = discord.Embed(
        title="📋 Tracked Drivers",
        description=f"Currently monitoring {len(tracked_drivers)} driver(s)",
        color=discord.Color.blue()
    )
    
    for driver_id, data in tracked_drivers.items():
        channel = bot.get_channel(data['channel_id'])
        channel_name = channel.mention if channel else "Unknown channel"
        embed.add_field(
            name=data['username'],
            value=f"Posting to: {channel_name}",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name='test_result', help='Post a test race result (!test_result username)')
async def test_result(ctx, driver_name: str):
    """Post a sample race result for testing"""
    # Sample race data
    sample_race = {
        'race_id': 12345,
        'series_name': 'GT3 Fixed',
        'track_name': 'Spa-Francorchamps',
        'position': 3,
        'start_position': 7,
        'field_size': 24,
        'incidents': 4,
        'irating_change': 45,
        'new_irating': 2545,
        'sr_change': 0.15,
        'new_sr': 4.50,
        'race_time': '42:15.332',
        'champ_points': 85
    }
    
    await post_race_result(ctx.channel, driver_name, sample_race)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    load_tracked_drivers()
    check_race_results.start()  # Start the background task
    print(f'Monitoring {len(tracked_drivers)} drivers for race results')

@tasks.loop(minutes=5)  # Check every 5 minutes
async def check_race_results():
    """Background task to check for new race results"""
    if not tracked_drivers:
        return
    
    for driver_id, data in list(tracked_drivers.items()):
        try:
            # Get the channel
            channel = bot.get_channel(data['channel_id'])
            if not channel:
                continue
            
            # Simulate fetching latest race result
            # In production, you'd call the iRacing API here
            new_race = await fetch_latest_race(driver_id, data.get('last_race_id'))
            
            if new_race:
                # Post the race result
                await post_race_result(channel, data['username'], new_race)
                # Update last race ID
                tracked_drivers[driver_id]['last_race_id'] = new_race['race_id']
                save_tracked_drivers()
                
        except Exception as e:
            print(f"Error checking results for {data.get('username')}: {e}")

async def fetch_latest_race(driver_id, last_race_id):
    """
    Fetch the latest race result for a driver
    Replace this with actual iRacing API calls
    """
    # This is a placeholder that simulates finding a new race
    # In production, you'd make an API call to iRacing here
    
    # Example: Return None (no new race) or a race dict
    # For demo purposes, this returns None
    # When you connect to the real API, return race data when found
    return None

async def post_race_result(channel, username, race_data):
    """Post a formatted race result to Discord"""
    embed = discord.Embed(
        title=f"🏁 Race Results: {username}",
        description=f"**{race_data['series_name']}** at {race_data['track_name']}",
        color=discord.Color.green() if race_data['position'] <= 3 else discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    # Main results
    embed.add_field(name="Finish Position", value=f"**{race_data['position']}** / {race_data['field_size']}", inline=True)
    embed.add_field(name="Starting Position", value=str(race_data['start_position']), inline=True)
    embed.add_field(name="Incidents", value=str(race_data['incidents']), inline=True)
    
    # iRating change
    ir_change = race_data['irating_change']
    ir_emoji = "📈" if ir_change > 0 else "📉" if ir_change < 0 else "➡️"
    embed.add_field(
        name="iRating Change",
        value=f"{ir_emoji} {ir_change:+d} → {race_data['new_irating']}",
        inline=True
    )
    
    # Safety Rating change
    sr_change = race_data['sr_change']
    sr_emoji = "📈" if sr_change > 0 else "📉" if sr_change < 0 else "➡️"
    embed.add_field(
        name="Safety Rating",
        value=f"{sr_emoji} {sr_change:+.2f} → {race_data['new_sr']}",
        inline=True
    )
    
    # Race time
    embed.add_field(name="Race Time", value=race_data['race_time'], inline=True)
    
    # Add championship points if applicable
    if race_data.get('champ_points'):
        embed.add_field(name="Championship Points", value=str(race_data['champ_points']), inline=True)
    
    # Performance summary
    if race_data['position'] == 1:
        embed.set_footer(text="🏆 Victory!")
    elif race_data['position'] <= 3:
        embed.set_footer(text="🥉 Podium finish!")
    elif race_data['position'] <= 5:
        embed.set_footer(text="Top 5 finish!")
    
    await channel.send(embed=embed)

@bot.command(name='stats', help='Get iRacing stats for a driver (!stats username)')
async def get_stats(ctx, driver_name: str):
    """Fetch and display driver statistics"""
    embed = discord.Embed(
        title=f"📊 iRacing Stats: {driver_name}",
        description="Driver statistics overview",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    # Placeholder - you'll need to implement actual iRacing API calls
    embed.add_field(name="iRating", value="2500", inline=True)
    embed.add_field(name="Safety Rating", value="A 4.50", inline=True)
    embed.add_field(name="Wins", value="15", inline=True)
    embed.add_field(name="Top 5s", value="42", inline=True)
    embed.add_field(name="Races", value="150", inline=True)
    embed.add_field(name="Win Rate", value="10%", inline=True)
    
    embed.set_footer(text="Note: Connect to iRacing API for live data")
    
    await ctx.send(embed=embed)

@bot.command(name='series', help='Show current iRacing series')
async def get_series(ctx):
    """Display active racing series"""
    embed = discord.Embed(
        title="🏁 Active iRacing Series",
        description="Current racing series this week",
        color=discord.Color.green()
    )
    
    series_list = [
        "GT3 Fixed",
        "Formula Vee",
        "NASCAR Cup Series",
        "IMSA Michelin Pilot Challenge",
        "Porsche Cup",
        "Advanced Mazda MX-5 Cup"
    ]
    
    embed.add_field(
        name="Popular Series",
        value="\n".join([f"• {series}" for series in series_list]),
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='track', help='Get info about a track (!track [track name])')
async def get_track(ctx, *, track_name: str):
    """Display track information"""
    embed = discord.Embed(
        title=f"🏎️ Track Info: {track_name}",
        color=discord.Color.orange()
    )
    
    embed.add_field(name="Type", value="Road Course", inline=True)
    embed.add_field(name="Length", value="3.74 miles", inline=True)
    embed.add_field(name="Turns", value="14", inline=True)
    embed.add_field(name="Configuration", value="Full Course", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='schedule', help='Show this week\'s race schedule')
async def get_schedule(ctx):
    """Display weekly race schedule"""
    embed = discord.Embed(
        title="📅 This Week's Schedule",
        description="Upcoming race sessions",
        color=discord.Color.purple(),
        timestamp=datetime.now()
    )
    
    schedule_items = [
        "**Monday 8:00 PM** - GT3 Fixed @ Spa",
        "**Tuesday 7:30 PM** - NASCAR @ Daytona",
        "**Wednesday 9:00 PM** - Formula Vee @ Laguna Seca",
        "**Friday 8:00 PM** - IMSA @ Road Atlanta",
        "**Saturday 3:00 PM** - Porsche Cup @ Nürburgring"
    ]
    
    embed.add_field(
        name="Featured Events",
        value="\n".join(schedule_items),
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='compare', help='Compare two drivers (!compare driver1 driver2)')
async def compare_drivers(ctx, driver1: str, driver2: str):
    """Compare statistics between two drivers"""
    embed = discord.Embed(
        title=f"⚔️ Driver Comparison",
        description=f"{driver1} vs {driver2}",
        color=discord.Color.red()
    )
    
    embed.add_field(name=f"{driver1} iRating", value="2500", inline=True)
    embed.add_field(name=f"{driver2} iRating", value="2350", inline=True)
    embed.add_field(name="—", value="", inline=False)
    
    embed.add_field(name=f"{driver1} SR", value="A 4.50", inline=True)
    embed.add_field(name=f"{driver2} SR", value="B 3.89", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='help_iracing', help='Show all available commands')
async def help_command(ctx):
    """Display help information"""
    embed = discord.Embed(
        title="🤖 iRacing Bot Commands",
        description="Available commands for the iRacing Discord bot",
        color=discord.Color.gold()
    )
    
    # Auto-posting commands
    embed.add_field(
        name="📊 Auto Race Results",
        value=(
            "`!track_driver [username]` - Auto-post race results\n"
            "`!untrack_driver [username]` - Stop auto-posting\n"
            "`!tracked_drivers` - List tracked drivers\n"
            "`!test_result [username]` - Post sample result"
        ),
        inline=False
    )
    
    # General commands
    embed.add_field(
        name="🏁 General Commands",
        value=(
            "`!stats [username]` - Get driver statistics\n"
            "`!series` - View active racing series\n"
            "`!track [name]` - Get track information\n"
            "`!schedule` - View this week's schedule\n"
            "`!compare [driver1] [driver2]` - Compare two drivers"
        ),
        inline=False
    )
    
    embed.set_footer(text="Race results are checked every 5 minutes for tracked drivers")
    
    await ctx.send(embed=embed)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument. Use !help_iracing for command info.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Command not found. Use !help_iracing to see available commands.")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")

# Run the bot
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        print("Error: Please set DISCORD_BOT_TOKEN environment variable")
    else:
        bot.run(TOKEN)
