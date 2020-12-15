import os

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.api import functions, types

bot = Client("PyrogramJSON_bot")


@bot.on_message()
async def dump(bot: Client, message: Message):
    m_id = (
        message.reply_to_message.message_id
        if message.reply_to_message
        else message.message_id
    )
    if (message.caption and message.caption.endswith("-r")) or (
        message.text and message.text.endswith("-r")
    ):
        if message.chat.type == "supergroup":
            msg = await bot.send(
                functions.channels.GetMessages(
                    channel=await bot.resolve_peer(message.chat.id),
                    id=[types.InputMessageID(id=m_id)],
                )
            )
        elif message.chat.type in ["private", "group"]:
            msg = await bot.send(
                functions.messages.GetMessages(id=[types.InputMessageID(id=m_id)])
            )
        msg = str(msg)
    else:
        msg = str(message)
    if len(msg) > 4096:
        with open("output.txt", "w+", encoding="utf8") as f:
            f.write(msg)
        await message.reply_document("output.txt", caption="Message Output")
        os.remove("output.txt")
    else:
        await message.reply_text(f"```{msg}```")


bot.run()
