import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands,tasks
from discord.utils import get 
import requests
import nacl

class Radio(commands.Cog):

    def __init__(self,bot):
        self.sys = bot 
        self.union = self.sys.get_guild(int('1085209458633887885'))
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        self.update_status.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('## COG: Радио.')

    @tasks.loop(seconds=5.0)
    async def update_status(self):
        html = requests.get('http://station.waveradio.org').text
        title = [x for x in html.split('<td class="streamstats">') if 'Sovietwave' in x]
        await self.sys.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=title[2].split('</td>')[0]))

    @commands.command()
    async def stopRad(self,ctx):
        for x in self.sys.voice_clients:
                return await x.disconnect()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def init_r(self,ctx,vc=None):
            print('## COG: Активация радио.')
            voice =  discord.utils.get(ctx.guild.voice_channels, id=1085209459153973340)  if vc == None else discord.utils.get(ctx.guild.voice_channels, id=int(vc))
            voice_client = await voice.connect()
            source = FFmpegPCMAudio(source='http://station.waveradio.org/soviet',before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',options='-vn')  
            voice_client.play(source) 

async def setup(bot):
   await bot.add_cog(Radio(bot))