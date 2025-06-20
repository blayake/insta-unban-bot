import discord
from discord.ext import commands, tasks
from discord import app_commands
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
watching = {}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"❌ Sync failed: {e}")
    check_unban.start()

@app_commands.command(name="watch", description="Watch an Instagram username for unban")
@app_commands.describe(username="Instagram username to monitor")
async def watch(interaction: discord.Interaction, username: str):
    watching[username] = interaction.user.id
    await interaction.response.send_message(f"👀 Now watching @{username} for unban updates.")
@tasks.loop(seconds=60)
async def check_unban():
    to_remove = []
    for username, user_id in watching.items():
        try:
            url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers)

            if res.status_code == 200 and '"is_private"' in res.text:
                data = res.json()
                followers = data.get('graphql', {}).get('user', {}).get('edge_followed_by', {}).get('count', 'N/A')
                bio = data.get('graphql', {}).get('user', {}).get('biography', 'N/A')

                msg = (
                    f"✅ @{username} is UNBANNED!\n"
                    f"👥 Followers: {followers}\n"
                    f"📝 Bio: {bio}\n"
                    f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )

                user = await bot.fetch_user(user_id)
                await user.send(msg)

                channel = bot.get_channel(CHANNEL_ID)
                if channel:
                    await channel.send(msg)

                with open("unban_log.txt", "a") as log:
                    log.write(f"{datetime.now()} - @{username} unbanned. Followers: {followers}\n")

                to_remove.append(username)

        except Exception as e:
            print(f"❌ Error checking @{username}: {e}")

    for username in to_remove:
        watching.pop(username, None)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")
    check_unban.start()

@bot.tree.command(name="watch", description="Start watching an Instagram username")
async def watch(interaction: discord.Interaction, username: str):
    watching[username] = interaction.user.id
    await interaction.response.send_message(f"👁 Now watching @{username} for unban!", ephemeral=True)

if __name__ == "__main__":
    bot.run(TOKEN)

