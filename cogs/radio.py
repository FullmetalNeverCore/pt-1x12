import discord
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands,tasks
from discord.utils import get 
import requests
import nacl
import random
import yt_dlp as youtube_dl
from collections import defaultdict


class Radio(commands.Cog):

    def __init__(self,bot):
        self.sys = bot 
        self.chance = 20
        self.was_atomic = False
        self.previous = None
        self.count = 0
        self.dev_test = False
        self.voice_client = None
        self.atomic = False
        self.union = self.sys.get_guild(int('1085209458633887885'))
        self.FFMPEG_OPTIONS = {
        'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M',
        'options': '-vn'
    }
        self.atomic_playlist = {'Atomic Heart - Трава у дома' : 'https://www.youtube.com/watch?v=gKVXaMeazAQ',
                                'Atomic Heart - PT-1X12' : 'https://www.youtube.com/watch?v=AONkzY7iQtY',
                                'Atomic Heart (Original Game Soundtrack) Vol.1' : 'https://www.youtube.com/watch?v=R1eyjhTmErw',
                                'Atomic Heart - Arlekino' : 'https://www.youtube.com/watch?v=xBoBmle8d5Q'}
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
        }
        self.check_play.start()
        self.update_status.start()


    @tasks.loop(seconds=4.0)
    async def check_play(self):
         if not self.voice_client is None:
            if self.voice_client.is_playing():
                print('## RAD : Музыка играет')
            else:
                print('##RAD : Музыка не играет.')
                self.was_atomic = False
                self.atomic = False
                await self.init_radio('1',None)
         else:
              try:
                self.atomic = False
                await self.init_radio('1',None)
              except Exception as e:
                   print(e)

    
    async def atomic_heart(self):
            
            '''if not self.voice_client is None:
                ＃if self.voice_client.is_playing():
                    await self.voice_client.disconnect()'''  
            self.voice_client.pause()
            print('## RAD : Atomic heart был избран.')
            self.atomic = True
            chosen_song = random.choice(list(self.atomic_playlist.keys()))
            #print(chosen_song)
            self.previous = chosen_song
            await self.sys.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=chosen_song)) 
            voice =  discord.utils.get(self.union.voice_channels, id=1085214777246224424) 
            #self.voice_client = await voice.connect() if not self.voice_client is None else print('passing')
            #print(chosen_song)
            #print(self.atomic_playlist.get(chosen_song))
            with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(self.atomic_playlist.get(chosen_song), download = False)
                source = FFmpegPCMAudio(source=info['formats'][8]['fragments'][0]['url'],before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',options='-vn')  
                self.voice_client.play(source)

    @tasks.loop(seconds=5.0)
    async def update_status(self):
        try:
            print(self.dev_test)
            print(f'## RAD : Атомный режим - {self.atomic}')
            
            html = requests.get('http://station.waveradio.org').text
            title = [x for x in html.split('<td class="streamstats">') if 'Sovietwave' in x][2].split('</td>')[0]
            print(f'## RAD : Музыка сейчас - {title}, музыка до {self.previous}')
            if title != self.previous and not self.atomic or self.dev_test:
                print('＃＃RAD ： Выбор...')
                print(self.chance)
                if random.randint(0,100) <= self.chance and not self.was_atomic:
                    if self.voice_client is not None:
                        await self.atomic_heart()
                #else:
                    ##await self.init_radio('1',None)
            if not self.atomic:
                if title != self.previous and not self.atomic or self.dev_test:self.was_atomic = not self.was_atomic
                self.previous = title
                await self.sys.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=title)) 
            print(f'## RAD : {self.previous}')
        except Exception as e:
             print(e)


    @commands.command()
    @commands.is_owner()
    async def set_gib(self,x=None):
         self.previous = '1'

    @commands.command()
    @commands.is_owner()
    async def set_dev(self,x=None):
         self.dev_test = not self.dev_test

    @commands.command()
    @commands.is_owner()
    async def set_chance(self,ctx,x):
         self.chance = int(ctx.message.content.split()[1])
         print(self.chance)


    @commands.command()
    @commands.is_owner()
    async def get_links(self,x=None):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
              for x in list(self.atomic_playlist.keys()):  
                info = ydl.extract_info(str(self.atomic_playlist.get(x)), download=False)
                print(info['url'])
              

    @commands.command()
    async def stopRad(self,ctx):
        for x in self.sys.voice_clients:
                return await x.disconnect()
        
    async def init_radio(self,ctx,vc=None): 
            if not self.voice_client is None:
                for x in self.sys.voice_clients:
                        return await x.disconnect()
            self.atomic = False
            print('## COG: Активация радио.') 
            try:self.check_play.start()
            except Exception as e:
                 print(e)
            voice =  discord.utils.get(self.union.voice_channels, id=1085214777246224424)  if vc == None else discord.utils.get(self.union.voice_channels, id=int(vc))
            self.voice_client = await voice.connect()
            source = FFmpegPCMAudio(source='http://station.waveradio.org/soviet',before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',options='-vn')  
            self.voice_client.play(source)

    @commands.command()
    #@commands.has_permissions(administrator=True)
    async def init_r(self,ctx,vc=None):
            await self.init_radio(ctx,vc)

            
    @commands.command()
    @commands.is_owner() 
    async def init_ah(self,ctx,vc=None):
            self.voice_client.pause()
            print('## RAD : Atomic heart был избран.')
            self.atomic = True
            chosen_song = random.choice(list(self.atomic_playlist.keys()))
            #print(chosen_song)
            self.previous = chosen_song
            await self.sys.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=chosen_song)) 
            voice =  discord.utils.get(self.union.voice_channels, id=1085214777246224424) 
            self.voice_client = await voice.connect()
            #print(chosen_song)
            #print(self.atomic_playlist.get(chosen_song))
            with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(self.atomic_playlist.get(chosen_song), download = False)
                source = FFmpegPCMAudio(source=info['formats'][8]['fragments'][0]['url'],before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',options='-vn')  
                self.voice_client.play(source)

async def setup(bot):
   await bot.add_cog(Radio(bot))