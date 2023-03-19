import discord 
from discord.ext import commands,tasks
from discord.utils import get 


intents = discord.Intents.all()
intents.members = True 
intents.messages = True
owner_id=224486385992728576
sys = commands.Bot(command_prefix=">",owner_id=owner_id,intents=intents)


@sys.event
async def on_ready():
    print(f'Система PT-1X12 готова.')

@sys.command()
@commands.is_owner()
async def load(ctx,extension):
    print(ctx.author.id)
    sys.load_extension(f'cogs.{extension}')
    await ctx.send(f'Модуль {extension} загружен.')


@sys.command()
@commands.is_owner()
async def unload(ctx,extension):
    sys.load_extension(f'cogs.{extension}')
    await ctx.send(f'Модуль {extension} отключен.')

@sys.command()
@commands.is_owner()
async def owner(ctx):
    print(ctx)
    user = get(sys.get_all_members(), id=owner_id)
    print(dir(user))
    print(f'Owner - {owner_id}')
    await ctx.send(f'Администратор подтвержден - {user.name}')

@owner.error 
async def owner_error(ctx,error):
       print(error)
       user = get(sys.get_all_members(), id=owner_id)
       await ctx.send(f'Вы не являетесь администратором.Администратор - {user.name}') 


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


sys.run('MTA4NTk5MzY5NDU3NTk5Njk1OA.G-eMnF.94R5zXT_4jdxrEOKm04aLDN3Uo3yM2tUtI5bxc')
