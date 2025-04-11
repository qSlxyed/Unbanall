import discord
from discord import app_commands
from discord.ext import commands
import json


with open('config.json') as f:
    config = json.load(f)
token = config['token']


intents = discord.Intents.default()
intents.guilds = True
intents.bans = True


bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')


@bot.tree.command(name="unbanall", description="Unbans all users from the server")
@app_commands.checks.has_permissions(ban_members=True)
async def unbanall(interaction: discord.Interaction):
    await interaction.response.send_message("Fetching ban list...", ephemeral=True)
    try:
        bans = await interaction.guild.bans()
        if not bans:
            await interaction.followup.send("No users are banned in this server.")
            return

        total = len(bans)
        await interaction.followup.send(f"Found {total} banned user(s). Starting to unban...")
        
        for entry in bans:
            await interaction.guild.unban(entry.user)

        await interaction.followup.send(f"✅ Successfully unbanned {total} user(s).")
    except Exception as e:
        await interaction.followup.send(f"⚠️ Error while unbanning: `{str(e)}`")


@unbanall.error
async def unbanall_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("🚫 You do not have permission to use this command.", ephemeral=True)


bot.run(token)
