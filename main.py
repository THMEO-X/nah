import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

OWNER_ID = int(os.getenv("OWNER_ID"))  # ID duy nhất điều khiển bot

# Từ khóa và phản hồi, dễ dàng thêm/xóa sửa sau này
keyword_replies = {
    "redz hub": '''local Settings = {
  JoinTeam = "Pirates"; -- Pirates/Marines
  Translator = true; -- true/false
}

loadstring(game:HttpGet("https://raw.githubusercontent.com/newredz/BloxFruits/refs/heads/main/Source.luau"))(Settings)''',

    "hello": "chao",

    "blox fruits": '''print("Welcome to Blox Fruits!")''',

    # Bạn thêm từ khóa mới như dưới đây
    # "từ khóa mới": "phản hồi tương ứng"
}

@bot.event
async def on_ready():
    print(f'Bot đã online với tên {bot.user}!')

@bot.command()
async def start(ctx, channel_id: int):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("Bạn không có quyền sử dụng lệnh này.")
    # Thêm logic lưu channel hoạt động ở đây nếu muốn
    await ctx.send(f"Bot sẽ hoạt động ở kênh ID {channel_id}.")

@bot.command()
async def stop(ctx, channel_id: int):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("Bạn không có quyền sử dụng lệnh này.")
    # Thêm logic dừng bot ở channel này
    await ctx.send(f"Bot dừng hoạt động ở kênh ID {channel_id}.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Nếu bạn dùng chức năng start/stop theo channel, kiểm tra channel ở đây

    content_lower = message.content.lower()
    for key in keyword_replies:
        if key in content_lower:
            await message.channel.send(keyword_replies[key])
            break

    await bot.process_commands(message)

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)
