
import discord
from discord.ext import commands
from discord import app_commands,File
import logging

logging.basicConfig(filename="log_for_srm_bot.log",format="%(message)s, %(asctime)s  ", filemode="a",datefmt="%d/%m/%Y %I:%M:%S")
logger = logging.getLogger()
logger.setLevel(logging.ERROR)


bot  = commands.Bot(command_prefix="/", intents=discord.Intents.all())
token = ""


class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
            await tree.sync(guild=discord.Object(id=908203872454062111))
            self.synced = True
            print("Bot is online !!")


bot = abot()
tree = app_commands.CommandTree(bot)


@tree.command(name="ping",description="pings the user",guild=discord.Object(id=908203872454062111))
async def self(interation: discord.Interaction):
    await interation.response.send_message(f"Pong! {round(bot.latency*100)}ms")

@tree.command(name="imp_info",description="All the important info for SRM's admission process",guild=discord.Object(id=908203872454062111))
async def self(interation: discord.Interaction):
    await interation.response.send_message('''As of now we have been given only tentative dates
                     (PHASE 1 and 2)
1) Last date for Balance tution fees is extended until further notice 
2) Online Enrollment is on 27th July 2022
3) Online hostel bookings is on 28th July 2022
4) Inauguration is on 10th August 2022

                    (PHASE 3)
1) Last date for Balance tution fees is 6th August 2022 
2) Online Enrollment is on 8th August 2022
3) Online hostel bookings is on 9th August 2022
4) Inauguration is on 10th August 2022''')

@tree.command(name="get_academic_schedule",description="Tentative academic schedule",guild=discord.Object(id=908203872454062111))
async def self(interation: discord.Interaction):
    await interation.response.send_message("here's your academic schedule",file=File("Academic_schedule.pdf"))

@tree.command(name="ask_anything",description="Ask for anything related to college",guild=discord.Object(id=908203872454062111))
async def self(interation: discord.Interaction,question:str):
    # await interation.response.send_message()
    query = question.lower()
    # query_fin = query.split(" ")
    if "hostel booking"in query:
        await interation.response.send_message("28th of August for phase 1 and 2 and 9th of August for phase 3 (ALL DATES ARE TENTATIVE)")
    elif "start" in query:
        await interation.response.send_message("Its 10th of August but its tentative for now")  
    elif "phase 3" in query:
        await interation.response.send_message("Yes, dates for phase 3 are different from 1 and 2")
    elif "payment"  in query:
        await interation.response.send_message("Date for all the phases to submit the fees is extended until further notice")              
    else:
        await interation.response.send_message("will tell you soon")
        print(question+" - "+str(interation.user))
        logger.error(question+" - "+str(interation.user))
        

bot.run(token)