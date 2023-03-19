import discord 
from discord.ext import commands,tasks
from discord.utils import get 


intents = discord.Intents.all()
intents.members = True 
intents.messages = True
sys = commands.Bot(command_prefix=">",intents=intents)


@sys.event
async def on_ready():
    print(f'Система PT-1X12 готова.')

@sys.command()
async def load(ctx,extension):
    print(ctx.author.id)
    if ctx.author.id == 224486385992728576:
        await sys.load_extension(f'cogs.{extension}')
        await ctx.send(f'Модуль {extension} загружен.')


@sys.command()
async def unload(ctx,extension):
    if ctx.author.id == 224486385992728576:
        await sys.load_extension(f'cogs.{extension}')
        await ctx.send(f'Модуль {extension} отключен.')

@sys.event
async def on_raw_reaction_add(payload):
    print('＃＃ ORRA: обнаружена реакция')
    union = sys.get_guild(1085209458633887885)
    roles = [get(union.roles,id=int('1085998154182299718')),get(union.roles,id=int('1085977925590982656'))]
    if payload.channel_id == 1085209459153973339:
        if any(x in payload.member.roles for x in roles):
            print("## ORRA: Пользователь уже имеет роль.")
        else:
            if payload.member != sys.user:
                if payload.emoji.name == '☑️': await payload.member.add_roles(roles[0])


sys.run('..')
