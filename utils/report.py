import discord


client = None
server = None
rep_channel = None

curr = {}


class Report:
    def __init__(self, message):
        self.stage = 0
        self.message = message
        self.author = message.author
        self.victim = None
        self.description = None
        self.messages = None


async def get_msg(server, mid):
    for c in server.channels:
        try:
            return await client.get_message(c, mid)
        except:
            pass
    return None


async def send_report(report):
    vic = report.victim
    author = report.author
    msgs = report.messages

    emb = discord.Embed(color=discord.Color.orange(), title="[REPORT]")
    emb.set_thumbnail(url=vic.avatar_url)
    emb.add_field(name="Victim", value="%s (%s)" % (vic.mention, vic.name), inline=False)
    emb.add_field(name="Author", value="%s (%s)" % (author.mention, author.name), inline=False)
    emb.add_field(name="Description", value=report.description, inline=False)

    count = 0
    if len(msgs) > 0:
        for msg in msgs:
            count += 1
            emb.add_field(name="Attached Message #" + str(count), value="```\nAuthor: %s\nChannel: %s```\n\"%s\"" % (msg.author.name, msg.channel.name, msg.content), inline=False)

    await client.send_message(rep_channel, embed=emb)
    del curr[author]


async def handle(message):
    global server
    global rep_channel
    server = [s for s in client.servers if s.id == "307084334198816769"][0]
    rep_channel = [c for c in server.channels if c.id == "342627519825969172"][0]

    content = message.content
    author = message.author
    channel = message.channel

    if curr.__contains__(author):
        report = curr[author]

        if content.startswith("cancel"):
            del curr[author]
            await client.send_message(channel, embed=discord.Embed(color=discord.Color.red(), description="Canceled report."))
            return

        if report.stage == 1:
            victim = discord.utils.get(server.members, id=content)
            if victim is None:
                await client.send_message(channel, embed=discord.Embed(color=discord.Color.red(), description="This user is not on this guild! Please enter a valid ID!"))
                return
            else:
                report.victim = victim
                report.stage = 2
                await client.send_message(channel, embed=discord.Embed(description="Set victim to `%s`.\n\nPlease now enter a description for your report." % victim.name))

        elif report.stage == 2:
            report.description = message.content
            report.stage = 3
            await client.send_message(channel, embed=discord.Embed(description="Successfully set description for your report.\n\nNow, you can enter message ID's *(seperate them like this: `<id 1>, <id 2>, ...`)* to prove the violation of the rules.\nEnter `none` to attach no message."))

        elif report.stage == 3:
            message_ids = content.split(", ")
            messages = []
            for mid in message_ids:
                msg = await get_msg(server, mid)
                if msg is not None:
                    messages.append(msg)
            await client.send_message(channel, embed=discord.Embed(description="Attached ``%s`` message(s) to report.\n\nReport successfully send to channel %s.\nThanks for your report!" % (len(messages), rep_channel.mention)))
            report.messages = messages
            await send_report(report)

    if content.startswith("report"):
        report = Report(message)
        report.stage = 1
        curr[author] = report
        await client.send_message(channel, embed=discord.Embed(description="Please enter the ID of the user you want to report.\n\n*You can get the ID by right-clicking on the user -> Copy ID. For that, you need to enable the developer mode in the didscord settings -> `Appearance` -> `Developer Mode`*\n\n**Hint:** You can always cancel the report formular with entering `cancel`"))
