from pyrogram import Client, filters
import subprocess
import os

api_id = 24322144          # Replace with your API ID
api_hash = "2b3a4e84eab9c466d1d903178ebb931f"    # Replace with your API HASH
bot_token = "8126645456:AAFDw2c2_tHEoT1esT1WGO8kOL1TBqOQNjE"  # Replace with your BotFather token

app = Client("streambot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.document | filters.video)
async def handle_file(client, message):
    msg = await message.reply("Downloading your file...")
    file_path = await message.download()

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_file = f"{base_name}_streamable.mp4"

    await msg.edit("Converting to streamable format...")

    subprocess.run([
        "ffmpeg", "-i", file_path,
        "-c:v", "libx264", "-c:a", "aac",
        "-movflags", "+faststart",
        output_file
    ])

    await msg.edit("Uploading converted file...")
    await message.reply_document(output_file)

    os.remove(file_path)
    os.remove(output_file)
    await msg.delete()

app.run()