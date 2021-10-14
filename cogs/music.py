import discord
from discord.ext import commands
import youtube_dl as yt
from requests import get
import asyncio


class music(commands.Cog):
    FFMPEG_OPTIONS={'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}
    YDL_OPTIONS={'format':'bestaudio'}
    songs = asyncio.Queue()
    play_next_song = asyncio.Event()

    def __init__(self,client):
        self.client=client
    
    def search(self,arg):
        with yt.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                get(arg) 
            except:
                video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            else:
                video = ydl.extract_info(arg, download=False)
            return video

    @commands.command(name="leave",
        help="Makes the bot leave the channel",
        aliases=['l'])
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name="play",
        help="Plays the given song \U0001F3B5",
        aliases=['p'])
    async def play(self, ctx, *,url):
        ctx.voice_client.stop()
        url = ''.join(url)
        info = self.search(url)
        url2=info['formats'][0]['url']
        source=await discord.FFmpegOpusAudio.from_probe(url2, **self.FFMPEG_OPTIONS)
        vc=ctx.voice_client
        vc.play(source)


    @commands.command(name="join",
        help="Invite the bot to the channel",
        aliases=['j','hop'])
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("First join a voice channel to use this command")
        voice_channel=ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

def setup(client):
    client.add_cog(music(client))