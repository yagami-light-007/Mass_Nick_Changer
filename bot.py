import discord
from discord.ext import commands

# ==============================
# CONFIGURATION
# ==============================

TOKEN = input("Enter your Discord Bot Token: ").strip()

if not TOKEN:
    print("Bot token cannot be empty.")
    exit()

TAG = "FK | "   # Change this if you ever want another tag

# ==============================
# BOT SETUP
# ==============================

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# ==============================
# EVENTS
# ==============================

@bot.event
async def on_ready():
    print("=" * 40)
    print(f"Logged in as: {bot.user}")
    print(f"Servers: {len(bot.guilds)}")
    print("Bot is Online!")
    print("=" * 40)

# ==============================
# HELP COMMAND
# ==============================

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="FK Renamer Bot",
        description="Bulk nickname renamer.",
        color=0x5865F2
    )

    embed.add_field(
        name="Command",
        value="`!renameall` - Rename everyone to `FK | Username`",
        inline=False
    )

    await ctx.send(embed=embed)

# ==============================
# RENAME COMMAND
# ==============================

@bot.command()
@commands.has_permissions(administrator=True)
async def renameall(ctx):

    await ctx.send("Starting nickname update...")

    success = 0
    failed = 0

    me = ctx.guild.me

    for member in ctx.guild.members:

        if member.bot:
            continue

        if member == ctx.guild.owner:
            failed += 1
            continue

        if member.top_role >= me.top_role:
            failed += 1
            continue

        new_name = f"{TAG}{member.name}"

        if len(new_name) > 32:
            new_name = new_name[:32]

        try:
            await member.edit(nick=new_name)
            success += 1

        except Exception as e:
            print(f"Failed: {member} -> {e}")
            failed += 1

    embed = discord.Embed(
        title="Rename Complete",
        color=0x57F287
    )

    embed.add_field(name="Renamed", value=str(success))
    embed.add_field(name="Failed", value=str(failed))

    await ctx.send(embed=embed)

# ==============================
# ERROR HANDLING
# ==============================

@renameall.error
async def rename_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You must be an Administrator to use this command.")

    else:
        await ctx.send(f"Error: {error}")

# ==============================
# START BOT
# ==============================

try:
    bot.run(TOKEN)

except discord.LoginFailure:
    print("Invalid Bot Token.")

except Exception as e:
    print(e)
