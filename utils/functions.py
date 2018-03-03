import discord
from os import path
import os
from time import gmtime, strftime
import json


def get_members_msg(client):
    """
    Returns game string with current member count and online member count.
    """
    server = list(client.servers)[0]
    members = str(len([m for m in server.members if not m.bot]))
    online_members = str(len([m for m in server.members if not m.bot and not str(m.status) == "offline"]))
    return "%s members (%s online) | !help" % (members, online_members)


async def send_join_pm(member, client):
    """
    |coro|
    Sends a welcome private message to joined members.
    """

    if member.bot:
        return

    currently_online = ""
    for m in member.server.members:
        if not m.status.__str__() == "offline":
            if m.roles.__contains__(discord.utils.get(m.server.roles, name="Supporter")):
                currently_online += ":white_small_square:  " + m.mention + "\n"

    super_bots = ""
    user_bots = ""
    for b in member.server.members:
        if b.roles.__contains__(discord.utils.get(m.server.roles, name="Super Bots (zekro)")):
            super_bots += ", " + b.mention
        elif b.roles.__contains__(discord.utils.get(m.server.roles, name="User Bots")):
            user_bots += ", " + b.mention

    await client.send_message(member,
                              "**Hey, " + member.name + "! Welcome on zekro's Dev Discord! :)**\n\n"
                              "You automatically got assigned the role `Dev` by %s, I hope ^^\n"
                              "Please now, go into the **%s** channel and type in `!dev` to get the roles witch languages you are writing in. The purpose behind that is that other users can "
                              "directly see witch languages you are familiar with and on the other side to mention the role to speak to the members in this role in the chats. Also please link your github "
                              "profile (if existing) with the command `!github add <link or username>`.\n\n"
                              "If you have some questions, look for online supporters or admins to ask for or ask the server owner (zekro) directly ;)\n\n"
                              "**Currently online supporters:**\n\n%s\n\n"
                              "Some information about the bots on this server:\n\n"
                              "**Super bots:**  %s\n"
                              "**User bots:**  %s\n\n"
                              "Use command `-help` to get command list from **zekroBot** and use `!help` to get information about **me (Knecht)**.\n\n\n"
                              "Now, have a lot fun on the server! :)"
                              % (discord.utils.get(member.server.members, id="272336949841362944").mention,
                                 discord.utils.get(member.server.channels, id="358364792614027265").mention,
                                 discord.utils.get(member.server.channels, id="309805161193406465").mention,
                                 currently_online,
                                 super_bots[2:],
                                 user_bots[2:]))


async def supp_add(before, after, client):
    """
    |coro|
    Edits a message in the welcome channel to list all current moderators and suppoerters names.
    """

    message_id = "334305867031904257"
    channel = discord.utils.get(list(client.servers)[0].channels, name="welcome")
    message = await client.get_message(channel, message_id)

    if len(list(filter(lambda r: r.name == "Supporter", before.roles))) == 0 and len(list(filter(lambda r: r.name == "Supporter", after.roles))) == 1:
        content = ":bookmark:   **Supporters**\n\n"
        for m in after.server.members:
            if len(list(filter(lambda r: r.name == "Supporter", m.roles))) == 1:
                content += ":white_small_square:  " + m.mention + "\n"
        await client.edit_message(message, content)


def logcmd(message):
    """
    Logs command out of message in a file.
    """
    if not path.isdir("SAVES"):
        os.mkdir("SAVES")
    with open("SAVES/cmdlog.txt", "a") as fw:
        time = strftime("%d.%m.%Y %H:%M:%S", gmtime())
        fw.write("[%s] [%s (%s)] [%s (%s)] '%s'\n" % (time, message.server.name, message.server.id, message.author.name, message.author.id, message.content))


def get_settings():
    """
    Get all settings out of the settings list as json object
    """
    if path.isfile("general_settings.json"):
        with open("general_settings.json") as f:
            return json.load(f)
    else:
        return None