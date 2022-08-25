
import discord, asyncio
from discord.ext import commands
from discord import app_commands,File
import logging
import random
import math
import smtplib
from email.message import EmailMessage
import keyring
import mysql.connector

db = mysql.connector.connect(
    host= "l",
    user = "",
    passwd = "",
    auth_plugin='mysql_native_password',
    db = "srm_discord_email_verifier"
    )

mycursor = db.cursor()


guild_id = ""


logging.basicConfig(filename="log_for_srm_bot.log",format="%(message)s, %(asctime)s  ", filemode="a",datefmt="%d/%m/%Y %I:%M:%S")
logger = logging.getLogger()
logger.setLevel(logging.ERROR)


bot  = commands.Bot(command_prefix="/", intents=discord.Intents.all())
token = "MTAwMDcwMTExMzEyMjY5NzI4Ng.GMCKc6.LmQFw0XZ-CHTagTSMXThBZOa7izWnft69lMAQ0"


class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=guild_id))
        self.synced = True
        print("Bot is online !!")


bot = abot()
tree = app_commands.CommandTree(bot)

@tree.command(guild=discord.Object(id=guild_id),name='ping',description='pings the user')#guild specific slash command
async def defer(Interaction:discord.Interaction):
    await Interaction.response.defer(ephemeral=True)
    await asyncio.sleep(4)
    await Interaction.followup.send(f"Pong! {round(bot.latency*100)}ms")
    



# @tree.command(name="ping",description="pings the user",guild=discord.Object(id=guild_id))
# async def self(interation: discord.Interaction):
#     await interation.response.send_message(f"Pong! {round(bot.latency*100)}ms")

@tree.command(name="imp_info",description="All the important info for SRM's admission process",guild=discord.Object(id=guild_id))
async def self(interation: discord.Interaction):
    await interation.response.send_message('''The updated info is given below 
                    (PHASE 1, 2 and 3)
1) Last date for Balance tution fees is 16th Aug 2022 
2) Online Enrollment is on 17th Aug 2022
3) Online hostel bookings is on 18th Aug 2022
4) Inauguration is on 1st Sep 2022
5) Orientation is from 2nd to 8th september
6) Commencement of classes is on 9th Sep 2022''')


@tree.command(name="get_academic_schedule",description="Tentative academic schedule",guild=discord.Object(id=guild_id))
async def self(interation: discord.Interaction):
    await interation.response.send_message("here's your academic schedule",file=File("Academic_schedule.pdf"))

@tree.command(name="ask_anything",description="Ask for anything related to college",guild=discord.Object(id=guild_id))
async def self(interation: discord.Interaction,question:str):
    # await interation.response.send_message()
    query = question.lower()
    # query_fin = query.split(" ")
    if "hostel booking"in query:
        await interation.response.send_message("Online Hostel booking is on 18th Aug 2022")
    elif "start" in query:
        await interation.response.send_message("Commencement of classes is on 9th Sep 2022 ")  
    elif "enrol" in query:
        await interation.response.send_message("Online Enrollment is on 17th Aug 2022 ")   
    elif "inauguration" in query:
        await interation.response.send_message("Inauguration is on 1st Sep 2022")      
    elif "phase 3" in query:
        await interation.response.send_message("Same dates as phase 1 and phase 2")
    elif "payment"  in query:
        await interation.response.send_message("Last date for Balance tuition fees is 16th Aug 2022") 
    elif "balance"  in query:
        await interation.response.send_message("Last date for Balance tuition fees is 16th Aug 2022")     
    elif "orientation" in query:
        await interation.response.send_message("Orientation is from 2nd to 8th September")     
    else:
        await interation.response.send_message("will tell you soon")
        print(question+" - "+str(interation.user))
        logger.error(question+" - "+str(interation.user))


@tree.command(name="verify",description="Verifies you into the server (sends otp)",guild=discord.Object(id=guild_id))
async def new(interation: discord.Interaction, mail:str):
    id_nam = interation.user.id
    query_ini = ("SELECT EXISTS(SELECT * FROM mailverifier WHERE name_id ='%s')"%id_nam)
    mycursor.execute(query_ini)
    res = mycursor.fetchall()
    if res[0][0] ==0:
        await interation.response.send_message(f"Hi {interation.user}. Sending your mail..")
        digits="0123456789"
        OTP=""
        for i in range(6):
            OTP+=digits[math.floor(random.random()*10)]
        otp = OTP 
        msg= otp
        Sender_Email = "verifyyourmail2324@gmail.com"
        Reciever_Email = mail
        # if "@srmist.edu.in" in mail:
        mail_ini = mail.split("@")
        nam = str(interation.user)
        
        Password = "rnpxaawuenvyqilr"
        add_details = ("INSERT INTO mailverifier "
                "(name_id,name, email, otp) "
                "VALUES (%s, %s, %s, %s)")
        data_details= (id_nam,nam,mail_ini[0],otp)              
        mycursor.execute(add_details,data_details)
        db.commit()  
        newMessage = EmailMessage()                         
        newMessage['Subject'] = "SRM'26 server" 
        newMessage['From'] = Sender_Email                   
        newMessage['To'] = Reciever_Email                   
        newMessage.set_content(f'Here is your otp, use it to verify {msg}') 

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            
            smtp.login(Sender_Email, Password)              
            smtp.send_message(newMessage)
        await interation.followup.send('''OTP sent !! Check your mail
now use /otp command to verify yourself''')
        # else: 
        # await interation.response.send_message("Wrong mail!!")
        # logger.error(f"{interation.user} Using wrong mail reason: non-srm mail!!")   
    else:
        await interation.response.send_message("You have already been verified and if you aren't try using the /otp command.")
        logger.error(f"{interation.user} mail already sent reason: trying to use ver_block 2!!")           


######### 2 #########
@tree.command(name="otp",description="Verifies you into the server(enter otp) ",guild=discord.Object(id=guild_id))
async def new(interation: discord.Interaction,otp:int):
    id_nam = interation.user.id
    query_ini = ("SELECT EXISTS(SELECT * FROM mailverifier WHERE name_id ='%s' and verified = 1)"%id_nam)
    mycursor.execute(query_ini)
    res = mycursor.fetchall()
    if res[0][0]==0:
        role = "Verified"
        query_ini = ("select otp from mailverifier where name_id ='%s'"%id_nam)
        mycursor.execute(query_ini)
        fin_otp = mycursor.fetchone()
        if fin_otp[0]==otp:

            update_table = ("""UPDATE mailverifier 
                        SET verified = %s
                        WHERE name_id = '%s' and otp = %s """)
            mycursor.execute(update_table%(1,id_nam,otp))    
            db.commit()                   
            await interation.user.add_roles(discord.utils.get(interation.user.guild.roles, name=role))
            await interation.response.send_message("Verified, you have been given your verified role too :) ")
        else:
            await interation.response.send_message("not verified") 
            logger.error(f"{interation.user} not verified reason: wrong otp!!")    
    else:
        await interation.response.send_message("you are already verified!! but if you haven't gotten the role yet contact dev team :))")
        logger.error(f"{interation.user} already verified reason: already exists!!")    


    
bot.run(token)
