from telethon.tl.types import ChannelParticipantsAdmins

from Obito_Probot import telethn
from Obito_Probot.events import register as obito


@obito(pattern="^/tagall ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    mentions = "Hello friends How Are You All"
    chat = await event.get_input_chat()
    async for x in telethn.iter_participants(chat, 100):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()


@obito(pattern="^/users ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    mentions = "Users : "
    chat = await event.get_input_chat()
    async for x in telethn.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


__mod_name__ = "Tᴀɢ"
__help__ = """
 |• `/mention`: Mention All Members Of Group Upto 20k
 |• `/tagall`: Tag everyone in a chat
 |• `/users`: Tag all users in a chat
"""
