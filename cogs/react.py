import discord 
from discord.ext import commands,tasks
from discord.utils import get 




class React(commands.Cog):
    def __init__(self,bot):
        self.sys = bot 
        self.channel = 1 

    @commands.Cog.listener()
    async def on_ready(self):
        print('## COG: Реакции.')
    
    async def cog_unload(self):
        print("## COG: Отключение...")

    @commands.command()
    async def set_channel(self,ctx):
        if ctx.author.id == 224486385992728576:
            print('## COG: Смена канала.')
            self.channel = ctx.message.content.split()[1]
    
    @commands.command()
    async def print_channel(self,ctx):
        print(self.channel)    
    
    @commands.command()
    async def test_grt_msg(self,ctx):
        if ctx.author.id == 224486385992728576:
            union = self.sys.get_guild(int('1085209458633887885'))
            target_channel = get(union.text_channels,id=int(self.channel))
            embed = discord.Embed(title=f'## Авторизация',color=0xff0000)
            embed.add_field(name=f'''
Проект «Красный Рассвет» готов к защите своих интересов от внешних угроз. Нам нужны сотрудники КГБ и милиции, обученные граждане, новые каналы и научные центры. 
Мы должны быть лидерами в мире Дискорда. 
Участвуйте в укреплении нашей обороны и безопасности!
            ''',value= '\u200b')
            embed.set_footer(text='Ген.сек. ЦК КПСС Юрьевич Назар Бесько')
            moji = await target_channel.send(embed=embed)
            await moji.add_reaction('☑️')



def setup(bot):
   bot.add_cog(React(bot))