import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

TOKEN = os.getenv("TOKEN")
MEMBER_ROLE_ID = 1423292549392498768

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def verify(ctx):
    member = ctx.author
    role = ctx.guild.get_role(MEMBER_ROLE_ID)

    if not role:
        return await ctx.send("⚠️ Member role not found. Check the role ID.")

    try:
        global_name = member.global_name or member.name
        new_name = f"⁵⁵⁵⁵•{global_name}"
        await member.edit(nick=new_name)
        await member.add_roles(role)

        embed = discord.Embed(
            title="✅ Verification Complete!",
            description=f"Welcome **{new_name}**! You've been verified successfully.",
            color=discord.Color.green()
        )
        embed.add_field(name="Assigned Role", value=role.name, inline=True)
        embed.set_footer(text="Verification System • ⁵⁵⁵⁵")

        await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())

    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to change your nickname or add roles.")
    except Exception as e:
        await ctx.send(f"⚠️ Error: `{e}`")

keep_alive()
bot.run(TOKEN)
