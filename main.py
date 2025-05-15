import discord
from discord.ext import commands
import re
import os
from keep_alive import keep_alive

OWNER_ID = int(os.getenv("OWNER_ID"))         # ID Discord chủ bot
BOT_TOKEN = os.getenv("DISCORD_TOKEN")        # Token bot từ biến môi trường

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)

watched_channels = set()
keyword_replies = {}

@bot.event
async def on_ready():
    print(f"Bot đã đăng nhập dưới tên: {bot.user}")

@bot.command()
async def start(ctx, channel_id: int):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("Bạn không có quyền dùng lệnh này.")
    watched_channels.add(channel_id)
    await ctx.send(f"Đã bật phản hồi trong kênh `{channel_id}`.")

@bot.command()
async def stop(ctx, channel_id: int):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("Bạn không có quyền dùng lệnh này.")
    watched_channels.discard(channel_id)
    await ctx.send(f"Đã tắt phản hồi trong kênh `{channel_id}`.")

@bot.command()
async def scr(ctx, *, arg):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("Bạn không có quyền dùng lệnh này.")

    # Hỗ trợ nội dung code block nhiều dòng ```lua ... ```
    match = re.match(r"\{(.+?)\}\s*\s*```(?:lua)?\n?([\s\S]+?)\n?```\s*", arg)
    if not match:
        return await ctx.send("Sai cú pháp! Hãy dùng: !scr {từ} (```lua\n...code...\n```)")

    key, response = match.groups()
    keyword_replies[key.lower()] = response.strip()
    await ctx.send(f"Đã thêm từ khóa: `{key}` với nội dung nhiều dòng.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if message.channel.id in watched_channels:
        content = message.content.lower()
        if content in keyword_replies:
            await message.channel.send(f"```lua\n{keyword_replies[content]}\n```")

# Giữ bot sống
keep_alive()

# Chạy bot
bot.run(BOT_TOKEN)
