import aiosqlite
import discord
import os

from callbacks import mapping

from discord.ui import View
from discord.ext import commands

client = commands.Bot(
    command_prefix="d!",
    help_command=None,
    case_insensitive=True,
    strip_after_prefix=True,
    intents=discord.Intents(guilds=True, members=True, messages=True, message_content=True),
    allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True),
)

@client.listen()
async def on_ready():
    async with aiosqlite.connect("main.db") as main:
        async with main.execute("SELECT * FROM views") as cursor:
            res = await cursor.fetchall()

        for item in res:
            async def callback(inter):
                resp, ui = await mapping[item[0]](client)
                if type(resp) is discord.Embed:
                    await inter.response.edit_message(embed=resp)
                else:
                    await inter.response.edit_message(content=resp)

            pair = await mapping[item[0]](client)
            pair[-1].callback = callback
            client.add_view(View(pair[-1], timeout=None), message_id=int(item[-1]))

    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"With DVY members!"))
    print(f"{client.user.name} (ID: {client.user.id}) is ready!")

@client.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    await ctx.message.add_reaction("<:RedTick:800399301980323840>")

@client.listen()
async def on_message(message: discord.Message):
    if client.user.display_name in message.clean_content and not message.author.bot:
        await message.channel.send("#StayDvystic <:LeonLul:762367743001362473>")

@client.listen()
async def on_raw_reaction_add(payload):
    try:
        if payload.channel_id == 762646267511439420:
            async with aiosqlite.connect("main.db") as main:
                async with main.execute(f"SELECT suggestion_id FROM suggestions") as cursor:
                    res = await cursor.fetchall()

                sug_chn = await client.fetch_channel(payload.channel_id)
                suggestion = await sug_chn.fetch_message(payload.message_id)
                send_to = await client.fetch_channel(832644572169502730)

                downvotes = suggestion.reactions[1].count
                if suggestion.reactions[0].emoji.id == 762658293407154196:
                    downvotes = suggestion.reactions[0].count
                if downvotes >= 15:
                    await suggestion.delete(reason="Non acceptable suggestion - 15 downvotes")

                for item in res:
                    if payload.message_id == item[0]:
                        async with main.execute(f"SELECT sent_id FROM suggestions WHERE suggestion_id={payload.message_id}") as cur:
                            sent = await cur.fetchone()

                        for reaction in suggestion.reactions:
                            if reaction.emoji.id == 762658222963556402 and reaction.count >= 10 and downvotes > 0:
                                embed = discord.Embed(title=f"Suggestion by {suggestion.author}", description=f"> {suggestion.content}\n\n**{reaction.count}** upvotes | **{downvotes}** downvotes\n[Jump to suggestion!]({suggestion.jump_url})", colour=0x01bb70).set_thumbnail(url=suggestion.author.display_avatar.url)
                                embed.set_footer(icon_url=suggestion.author.guild.icon.url, text=f"User ID: {suggestion.author.id}")
                                p = await client.fetch_channel(832644572169502730)
                                m = await p.fetch_message(sent[0])
                                await m.edit(embed=embed)
                                break
                        break
                else:
                    for reaction in suggestion.reactions:
                        if reaction.emoji.id == 762658222963556402 and reaction.count >= 10 and downvotes > 0:
                            embed = discord.Embed(title=f"Suggestion by {suggestion.author}", description=f"> {suggestion.content}\n\n**{reaction.count}** upvotes | **{downvotes}** downvotes\n[Jump to suggestion!]({suggestion.jump_url})", colour=0x01bb70).set_thumbnail(url=suggestion.author.display_avatar.url)
                            embed.set_footer(icon_url=suggestion.author.guild.icon.url, text=f"User ID: {suggestion.author.id}")
                            s = await send_to.send(embed=embed)
                            await main.execute("INSERT INTO suggestions(user_id, suggestion_id, sent_id) VALUES(?, ?, ?)", (suggestion.author.id, suggestion.id, s.id))
                            await main.commit()
                            break
    except IndexError:
        pass

@client.listen()
async def on_raw_reaction_remove(payload):
    try:
        if payload.channel_id == 762646267511439420:
            async with aiosqlite.connect("main.db") as main:
                async with main.execute(f"SELECT suggestion_id FROM suggestions") as cursor:
                    res = await cursor.fetchall()

                sug_chn = await client.fetch_channel(payload.channel_id)
                suggestion = await sug_chn.fetch_message(payload.message_id)

                downvotes = suggestion.reactions[1].count
                if suggestion.reactions[0].emoji.id == 762658293407154196:
                    downvotes = suggestion.reactions[0].count
                if downvotes >= 15:
                    await suggestion.delete(reason="Non acceptable suggestion - 15 downvotes")

                for item in res:
                    if payload.message_id == item[0]:
                        async with main.execute(f"SELECT sent_id FROM suggestions WHERE suggestion_id={payload.message_id}") as cur:
                            sent = await cur.fetchone()

                        for reaction in suggestion.reactions:
                            if reaction.emoji.id == 762658222963556402:
                                embed = discord.Embed(title=f"Suggestion by {suggestion.author}", description=f"> {suggestion.content}\n\n**{reaction.count}** upvotes | **{downvotes}** downvotes\n[Jump to suggestion!]({suggestion.jump_url})", colour=0x01bb70).set_thumbnail(url=suggestion.author.display_avatar.url)
                                embed.set_footer(icon_url=suggestion.author.guild.icon.url, text=f"User ID: {suggestion.author.id}")
                                p = await client.fetch_channel(832644572169502730)
                                m = await p.fetch_message(sent[0])
                                await m.edit(embed=embed)
    except IndexError:
        pass

extensions = [extension for extension in os.listdir("./extensions") if extension.endswith(".py")]
for ext in extensions:
    client.load_extension(f"extensions.{ext[:-3]}")

client.run(open("./tokens/discord.txt", "r", encoding="UTF-8").readline())
