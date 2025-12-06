import datetime
import discord

from const import *
from discord.ui import Button

async def roster(client):
    alts = {904468888140537966, 879790392344731688, 646094261783363666, 690247481417531419}
    all_ids = [id_ for id_ in STAFF.values()][::-1]
    guild = client.get_guild(706632833321664564)
    memo = set()
    embed = discord.Embed(title="Diversity Staff Roster!", colour=0x01bb70).set_thumbnail(url="https://i.imgur.com/GlZttyo.gif")

    for role in all_ids[:-1]:
        final = []
        r = discord.utils.get(guild.roles, id=role)
        for member in r.members:
            if member.id not in alts and member.name not in memo:
                final.append(member.mention)
                memo.add(member.name)
        embed.add_field(name=f"__{r.name}__", value="\n".join(final) + "\n\u200b", inline=False)
    embed.set_footer(icon_url=guild.icon.url, text="The roster updates hourly!")
    embed.timestamp = datetime.datetime.utcnow()

    refresh = Button(style=discord.ButtonStyle.green, label="Update", custom_id="refresh_roster", emoji="🔄")
    return embed, refresh

# this will now assign the proper callbacks to their respective commands
mapping = {
    "roster": roster
}
