from octorest import OctoRest
import config
import discord
from discord.ext.commands import Bot
from discord.ext import tasks, commands
from printer_functions import make_client, get_printer_info, get_extruder_temp, get_bed_temp
from discord.utils import get
import os
import datetime


discord_client = Bot(command_prefix=config.BOT_PREFIX)
octo_client = make_client(config.URL, config.API_KEY)
try:
    LAST_TEMP = get_extruder_temp(octo_client)
except:
    LAST_TEMP = 0


@discord_client.command(
    name='temperatures',
    description='Prints the current printer temps.',
    pass_context=True,
)
async def temperatures(context):
    await context.message.channel.send("Extruder Temperature: " + str(get_extruder_temp(octo_client)))
    await context.message.channel.send("Bed Temperature: " + str(get_bed_temp(octo_client)))


@discord_client.command(
    name='ping',
    description='Ping me.',
    pass_context=True,
)
async def ping(context):
    await context.send(f'Pong! `{discord_client.latency * 1000}`ms')
    return


@discord_client.command(
    name='pic',
    description='Takes a picture using the webcam',
    pass_context=True,
)
async def pic(context):
    os.system('fswebcam image.jpg')
    msg = 'Picture taken at ' + str(datetime.datetime.now())
    await context.message.channel.send(content=msg, file=discord.File('image.jpg'))
    return


@tasks.loop(seconds=10.0)
async def check_printer():
    global LAST_TEMP
    current_temp = get_extruder_temp(octo_client)
    if current_temp < 100 <= LAST_TEMP:
        #ping me
        user = await discord_client.fetch_user(config.USER)
        await user.send('Print Done')
    else:
        LAST_TEMP = current_temp
    return


@discord_client.event
async def on_ready():
    """
    Displays a short message in the console when the bot is initially run
    :return:
    """
    print('Logged in as')
    print(discord_client.user.name)
    print(discord_client.user.id)
    print('------')
    check_printer.start()


discord_client.run(config.TOKEN)
