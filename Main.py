from os import name
import os
import discord
from discord import colour
from discord import voice_client
from discord.ext import commands
from discord import client
from discord import member
import typing
import datetime
intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix = "?", intents=intents, help_command=None)
@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Over The Boys"))
	print(f'{client.user} is ready!')

@client.command()
async def purge(ctx, amount=5):
	deleted = await ctx.channel.purge(limit=amount+1)
	await ctx.send("**Successfully deleted ** `{}` **messages!**".format(len(deleted) - 1))

@client.command()
async def setnick(ctx, member: discord.Member, nick):
	await member.edit(nick=nick)
	await ctx.send(f"Nickname was changed for {member.mention}")


@client.command()
async def hug(ctx, *, member):
	author_name = ctx.message.author.name
	await ctx.send(f"{author_name} has hugged! {member}")

@client.command()
async def kiss(ctx, *, member):
	author_name = ctx.message.author.name
	await ctx.send(f"{author_name} has kissed! {member}")

@client.command()
async def avatar(ctx, member: discord.Member=None):
	if member == None:
		member = ctx.author
	
	icon_url = member.avatar_url

	avatarEmbed = discord.Embed(title = f"{member.name}\'s Avatar", color = 0xFFA500)
	avatarEmbed.set_image(url = f"{icon_url}")

	avatarEmbed.timestamp = ctx.message.created_at

	await ctx.send(embed = avatarEmbed)


@client.command()
async def userinfo(ctx, member: discord.Member):

    roles = [role for role in member.roles]
    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild name:", value=member.display_name)

    embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d, %B, %Y, %I:%M %p UTC" ))
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d, %B, %Y, %I:%M %p UTC"))

    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role:", value=member.top_role.mention)
	
    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)

@client.command()
async def kick(ctx, member: discord.Member=None, *, reason=None):
	await member.kick(reason=reason)
	await ctx.send(f"✅ {member} has been kicked!\n**Reason:** {reason}")


@client.command()
async def ban(ctx, member: discord.Member=None, *, reason=None):
	await member.ban(reason=reason)
	await ctx.send(f"✅ {member} has been banned!\n**Reason:** {reason}")

@client.command()
async def unban(ctx, id:typing.Union[int, None]):
	if id == None:
		await ctx.send("⚠ Please provide user ID!")
		return
	if id is not None:
		member = await client.fetch_user(id)
		await ctx.guild.unban(member)
		await ctx.send(f"✅ {member} is unbanned from the server!")
	else:
		await ctx.send("⚠ The member isn't banned from the server.")

@client.command()
async def mute(ctx, member: discord.Member=None):
	if member == None:
		await ctx.send("⚠Please mention a user to mute!")
		return

	guild = ctx.guild
	mutedRole = discord.utils.get(guild.roles, name='Muted')
	if not mutedRole:
		mutedRole = await guild.create_role(name='Muted')

		for channel in guild.channels:
			await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

		await member.add_roles(mutedRole)
		await ctx.send(f"🔇 {member} has been muted!")

@client.command()
async def say(ctx, *, text):
	message = ctx.message
	await message.delete()
	await ctx.send(f"{text}")

@client.command()
async def unmute(ctx, member: discord.Member=None):
    if member == None:
        await ctx.send("⚠ Please mention a user to unmute!")
        return

    guild = ctx.guild
    Role = discord.utils.get(guild.roles, name='Muted')

    await member.remove_roles(Role)
    await ctx.send(f"✅ {member} has been unmuted!")

@client.command()
async def join(ctx):
    await ctx.author.voice.channel.connect()
    await ctx.send('Joined your voice channel.')

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send('Left your voice channel.')

@client.command(name='help')
async def help(ctx):
    embed = discord.Embed(
        title = 'Help',
        description = 'Help For You!',
        color = discord.Color.red()
    )
    embed.set_footer(text=f'Requested by - {ctx.author}', icon_url=ctx.author.avatar_url)
    embed.add_field(name='General', value='`credits`')
    embed.add_field(name='Moderation', value='`Say`, `Dm`, `Kick`, `Ban`, `Unban`, `Mute`, `Unmute`, `Warn`, `Purge`, `Nick`', inline=False)
    await ctx.send (embed = embed)

@client.command()
async def slowmode(ctx, time: typing.Union[int, str, None]):
	if time == None:
		await ctx.send("⚠ Please provide time")
		return
	if time == 0:
		await ctx.send("Slowmode off, It'll be better if you do `slowmode off`")
		await ctx.channel.edit(slowmode_delay=0)
		return
	if time == "off":
		await ctx.send("Slowmode has been turned off!")
		return
	if time > 21600:
		await ctx.send("⚠ You can't set slowmode above 6 hours!")
		return
	if time >= 3600:
		await ctx.channel.edit(slowmode_delay=time)
		time2 = time%3600
		hours = time//3600
		minutes = time2//60
		seconds = time2%60
		await ctx.send(f"Slowmode set to `{hours}` hours, `{minutes}` minutes and `{seconds}` seconds!")
		return
	if time >= 60:
		await ctx.channel.edit(slowmode_delay=time)
		time2 = time%3600
		minutes = time2//60
		seconds = time2%60
		await ctx.send(f"Slowmode set to `{minutes}` minutes and `{seconds}` seconds!")
		return
	if time < 60:
		await ctx.channel.edit(slowmode_delay=time)
		await ctx.send(f"Slowmode set to, `{time}` seconds")

@client.event
async def on_member_join(member):
	await client.get_channel(951531505434386497).send("Welcome to the server! {}".format(member.mention))

with open("token.0", "r", encoding="utf-8") as f:
	TOKEN = f.read()
#----------------------Bot Run-------------------------------------------
client.run(TOKEN)
