import os

from discord import FFmpegOpusAudio, FFmpegPCMAudio
from discord.ext.commands import Bot
from discord.ext.commands.errors import CommandInvokeError


TOKEN = os.getenv("DISCORD_ANYPLAYER_TOKEN")         # collected from Discord Bot setup process.
PREFIX = os.getenv("DISCORD_ANYPLAYER_PREFIX")       # recommended: ">"
ENCODING = "ogg"                                     # options: ogg, mp3  (default: ogg)

client = Bot(command_prefix=list(PREFIX))

player = None


@client.event
async def on_ready():
    print('AnyPlayer Ready')


@client.command(name="menu")
async def menu(ctx):
    out = "Commands:\n\n"
    out += f"{PREFIX}play [filename]\n"
    out += f"{PREFIX}play [http(s) source]\n"
    await ctx.send(out)


async def do_play(ctx, src):
    global player
    try:
        channel = ctx.message.author.voice.channel
    except AttributeError:
        # user is not in a Voice Channel
        await ctx.send(f"You need to join a Voice Channel first!")
        return

    try:
        player = await channel.connect()
    except CommandInvokeError:
        print("Attempt to play without user in channel")
    except Exception as err:
        print(err)
        pass
    if player:
        if ENCODING == "mp3":
            player.play(FFmpegPCMAudio(src))
        else:
            player.play(FFmpegOpusAudio(src))
    else:
        print("Could not initialize player.")


@client.command(aliases=['p', 'pl'])
async def play(ctx, path):
    await do_play(ctx, path)



# Remove bot from channel if it's sitting unused.
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    # Checking if the bot is connected to a channel and if there is only 1 member connected to it (the bot itself)
    if voice_state is not None and len(voice_state.channel.members) == 1:
        # You should also check if the song is still playing
        await voice_state.disconnect()


client.run(TOKEN)

