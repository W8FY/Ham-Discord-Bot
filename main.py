import discord
from discord.ext import tasks
from lib.configurationimport import load_config_params
import callsignlookuptools
import re

# Library initalizations
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
config = load_config_params("config.yml")
calllookup = callsignlookuptools.CallookSyncClient()
channels = {}

# Bot ping command to test connection
@tree.command(name = "ping", description = "Test operability of Bot.")
async def botping(interaction):
    await interaction.response.send_message("pong")

# Startup Message to Display Uptime
async def channel_setup():
    print(f'Ham Bot is Initializing Channels...')
    global channels
    channels["callsignlookup"] = client.get_channel(config["CALLSIGN_CHANNEL_ID"])
    channels["loggingchannel"] = client.get_channel(config["LOGGING_CHANNEL_ID"])
    channels["generalchannel"] = client.get_channel(config["GENERAL_CHANNEL_ID"])
    # Clean and send first message
    await client.wait_until_ready()
    await channels["callsignlookup"].purge()
    server_message = "Welcome to the " + config["CLUB_CALL"] + " server - please tell me your call sign or say 'no call'..."
    await channels["callsignlookup"].send(server_message)
    return channels

# Processing messages from the callsign lookup channel
async def callsign_processing(message):
    # Print out the message that was recieved for processing
    print("Callsign Channel: " + message.content)
    print(f'Purging and reinitailizing channels...')
    # Go ahead and clean up (purge) the channel ASAP
    await channel_setup()
    # Pull in the channels global
    global channels
    # Try to find the callsign with regex, if not found, just send a message that it could not be found
    try:
        # Regex out the callsign
        callsign = re.search("[a-zA-Z0-9]{1,3}[0-9][a-zA-Z0-9]{0,3}[a-zA-Z]", message.content).group().upper()
        # If Regex found anything, use calllookup to search any necessary details, save those off to variables
        if callsign != None:
            calllookupresults = calllookup.search(callsign)
            call_firstname = str(calllookupresults.name).split(" ")[0].title()
            call_lastname = str(calllookupresults.name).split(" ")[-1].title()
            call_city = str(calllookupresults.address.city).title()
            call_state = str(calllookupresults.address.state).upper()
            call_license = str(calllookupresults.lic_class).split(".")[1].title()
            # Create a big log message to display the information to admins and send to the logging channel
            log_message = "Processing callsign channel message:\n" + message.content +  "\n\nFound callsign: " + callsign + "\nFirstname: " + call_firstname + "\nLastname: " + call_lastname + "\nCity: " + call_city + "\nState: " + call_state + "\nLicense Class: " + call_license
            await channels["loggingchannel"].send(log_message)
        # If the regex couldn't find a callsign, just send a logging message of no callsign found
        else:
            callsign = "Callsign not found"
            await channels["loggingchannel"].send("Processing callsign channel message:\n" + message.content + "\nNO CALLSIGN FOUND")
    except:
        await channels["loggingchannel"].send("Processing callsign channel message:\n" + message.content + "\nERROR COULD NOT PROCESS")
        callsign = "Callsign not found"
    finally:
        if callsign != "Callsign not found":
            # Assign them a nickname based on their callsign results and the proper role for their license
            nickname = (call_firstname + " " + call_lastname + " - " + callsign)
            print("Assigning nickname to " + callsign + " as " + nickname) 
            member = message.author
            try:
                await member.edit(nick=str(nickname))
            except:
                print("Error - Couldn't Change Nickname")
            try:
                match call_license: 
                    case "Technician":
                        await message.author.add_roles(discord.utils.get(member.guild.roles, name="Technician"))
                    case "General":
                        await message.author.add_roles(discord.utils.get(member.guild.roles, name="General"))
                    case "Extra":
                        await message.author.add_roles(discord.utils.get(member.guild.roles, name="Extra"))
            except:
                print("Error - Couldn't Assign Role")
            # Send an announcement message in the general chat
            await channels["generalchannel"].send(f"Everyone, please welcome {member.mention} from " + call_city + ", " + call_state + " to the server!")
        else:
            # Assign them a non-licensed role
            member = message.author
            await message.author.add_roles(discord.utils.get(member.guild.roles, name="Non-Licensed"))
            # Send an announcement message in the general chat
            await channels["generalchannel"].send(f"Everyone, please welcome {member.mention} to the server!")

# On_ready performed when bot connects for the first time
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync()
    channels = await channel_setup()

# Event handling for all messages in the channel
@client.event
async def on_message(message):
    # Ignore message from the bot itself
    if message.author.id not in [client.user.id]:
        # Ignore messages that are showhow blank
        if message.content != "":
            # Processing message from the callsign channel
            if (message.channel.id == config["CALLSIGN_CHANNEL_ID"]):
                await callsign_processing(message)

# Starts bot
client.run(config["DISCORD_TOKEN"])
