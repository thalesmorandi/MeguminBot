import discord


client = None


roleset = {
    "Admin": "⚡",
    "Moderator": "⚔",
    "Supporter": "🌠"
}


async def onchange(before, after):
    try:
        if len(before.roles) < len(after.roles):
            role = list(set(after.roles) - set(before.roles))[0]
            if before.roles != after.roles and role.name in roleset.keys():
                nick = after.nick if after.nick is not None else after.name
                await client.change_nickname(after, "%s %s" % (roleset[role.name], nick))
        elif len(before.roles) > len(after.roles):
            role = list(set(before.roles) - set(after.roles))[0]
            if role.name in roleset:
                await client.change_nickname(after, after.nick[2:])
    except:
        pass
