import discord;
from discord.ext import commands;
import json;
import aiohttp;
import os;
import re;
import time;
import io;

# Get the bot token from the config file
base_path = os.getcwd()
config_file = os.path.join(base_path, 'config.json')

smile = "\U0001F600"
frown = "\U0001F641"

with open(config_file) as config_file:
    config = json.load(config_file)
    TOKEN = config['Discord_Bot_Configuration']['discord_bot_token']
    #CHANNEL_ID = int(config['Discord_Bot_Configuration']['discord_channel_id'])
    VERSION = config['Discord_Bot_Configuration']['version']
    BOT_NAME = config['Discord_Bot_Configuration']['discord_bot_name']
    PRIMARY_EMBED_COLOR = int(config['Discord_Bot_Configuration']['primary_embed_color'],16) #convert hex to int for embed color

    OPENAI_API_KEY = config['OpenAI_Configuration']['openai_key']


    GPT_DALL_E_2_ENGINE = config['OpenAI_Configuration']['DALL-E-2-Config']['GPT_Art_Engine']
    GPT_DALL_E_2_QUALITY = config['OpenAI_Configuration']['DALL-E-2-Config']['GPT_Art_Quality']
    GPT_DALL_E_2_SIZE = config['OpenAI_Configuration']['DALL-E-2-Config']['GPT_Art_Size']
    GPT_DALL_E_2_NUMBER_OF_IMAGES = config['OpenAI_Configuration']['DALL-E-2-Config']['Number_of_GPT_Art_Images']
    GPT_DALL_E_2_MAX_NUMBER_OF_IMAGES = config['OpenAI_Configuration']['DALL-E-2-Config']['Max_IMAGES']

    GPT_DALL_E_3_ENGINE = config['OpenAI_Configuration']['DALL-E-3-Config']['GPT_Art_Engine']
    GPT_DALL_E_3_QUALITY = config['OpenAI_Configuration']['DALL-E-3-Config']['GPT_Art_Quality']
    GPT_DALL_E_3_SIZE = config['OpenAI_Configuration']['DALL-E-3-Config']['GPT_Art_Size']
    GPT_DALL_E_3_NUMBER_OF_IMAGES = config['OpenAI_Configuration']['DALL-E-3-Config']['Number_of_GPT_Art_Images']
    GPT_DALL_E_3_MAX_NUMBER_OF_IMAGES = config['OpenAI_Configuration']['DALL-E-3-Config']['Max_IMAGES']

# Create a bot instance with a command prefix
intents = discord.Intents.default()
intents.message_content =True;
intents.members = True;
bot = commands.Bot(command_prefix='.',intents=intents)
client = discord.Client (intents=intents)


def remove_special_characters(string:str):
    allowed_characters = re.compile(r'[a-zA-Z0-9_\-\.]+') #regex to allow only alphanumeric characters and _ - . characters
    #its easier to find the allowed characters than to find the disallowed characters also i hate regex with a passion

    # Use the findall method to get a list of allowed character sequences
    allowed_parts = re.findall(allowed_characters, string)

    # Join the allowed parts to form the cleaned file name
    cleaned_string = ''.join(allowed_parts)
    return cleaned_string


# Event listener for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    #print(os.getcwd())

    await bot.tree.sync()

@bot.tree.command(name="version",description="Get"+ BOT_NAME +" bot version")
async def version(interaction:discord.Interaction):
    embed = discord.Embed(title="My Version Info :D ", color=PRIMARY_EMBED_COLOR)
    embed.add_field(name="This is my Name :) ", value=BOT_NAME, inline=True)
    embed.add_field(name="Version", value=VERSION, inline=True)
    embed.add_field(name="Author", value="Scott/itachi", inline=True)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="draw", description="Ask me to draw something e.g cute anime cat with dalle 3.large,landscape and portrait. ")
async def drawpic(interaction:discord.Interaction, *, what_to_draw: str,number_of_pics:int=GPT_DALL_E_3_NUMBER_OF_IMAGES,pic_size:str=GPT_DALL_E_3_SIZE):
    #defer the response so we can get the image and then send it later, by default the response is sent after 3 seconds if we dont defer it
    # if the defer is not used then the response will be sent before the image is retrieved and we get an error
    await interaction.response.defer()
    try:

        # Retrieve the API key from the environment variable.
        #Loading local variables is supposed to be faster than loading global variables
        api_key = OPENAI_API_KEY
        size = pic_size
        title = what_to_draw
        DALL_E_3_ENGINE = GPT_DALL_E_3_ENGINE
        DALE_E_3_QUALITY = GPT_DALL_E_3_QUALITY
        NUMBER_OF_IMAGES = number_of_pics
        useRevised = False
        location = 0
        response = ""

        if not api_key:
            return await interaction.followup.send('API key not set.')

        if DALL_E_3_ENGINE == 'dall-e-3':
            if size == "large":
                size = "1024x1024"

            elif size == "portait":
                size = "1024x1792"

            elif size == "landscape":
                size = "1792x1024"

            else:
                size = "1024x1024"
        else:
             return await interaction.followup.send('Invalid Engine Configured')

        if len(what_to_draw) >= 256 :
            title = what_to_draw[:128] + "..."



        async with aiohttp.ClientSession() as session:

                if NUMBER_OF_IMAGES >= 1 and NUMBER_OF_IMAGES <= GPT_DALL_E_3_MAX_NUMBER_OF_IMAGES:

                        #now i send the revised prompt too the api n times and get the images dalle 3 doesnt support multiple images in one request
                         #add the first image to the list
                    image_urls =[]
                    revised_prompts = []
                    for i in range(NUMBER_OF_IMAGES): # -1 because we already have the first image
                        async with session.post('https://api.openai.com/v1/images/generations',headers={'Authorization': 'Bearer '+ api_key},
                                json={
                                    'model': DALL_E_3_ENGINE,
                                    'prompt': what_to_draw,
                                    'n':1, # Only 1 allowed for dalle 3 for now
                                    'size':size,
                                    'quality': DALE_E_3_QUALITY,
                                    }) as resp:
                            if resp.status == 400 and i == 0: #if the first request fails then we just stop
                                print(resp._body)
                                return await interaction.followup.send('Im not allowed to draw that' + frown)
                            elif resp.status != 200 and i == 0:
                                return await interaction.followup.send('Could not get image... ' + frown)

                            if resp.status != 200:
                                continue
                            response = await resp.json()
                            revised_prompts.append(response['data'][0]['revised_prompt'])
                            image_urls.append(response['data'][0]['url'])
                            if useRevised:
                                what_to_draw = response['data'][0]['revised_prompt']#gpt will keep this prompt for all images and will not generate a new one
                    #we need to download the images and send them as files in the embed
                    files = []
                    embed = discord.Embed(title="Here is your image of : " + title , color=PRIMARY_EMBED_COLOR)
                    #now we get the url for each image and download it
                    for image in image_urls:
                        image_url = image
                        async with session.get(image_url) as resp:
                            if resp.status != 200:
                                return await interaction.followup.send('Could not get image...')
                            data = io.BytesIO(await resp.read())
                            title = remove_special_characters(title) #Magic Stuff happens here
                            #random file name with unix the timestamp this is to prevent the same file name being used by multiple users
                            file_name = str(int(time.time()))+"_"+ title + ".png"
                            files.append(discord.File(data, filename=file_name,description=revised_prompts[location])) # Description is for the ALT text for the image to see it it needs to be  enabled on the account
                            location = location + 1
                    #now we send the files another way would have been to use the embed.set_image(url=image_url) mutiple times but that would have been a waste of bandwidth
                    await interaction.followup.send(embed=embed,files=files)
                else:
                    return await interaction.followup.send('Invalid Number of Images Configured in the config file')

    except Exception as e:
        # Handle exceptions and provide feedback to the user.
        print(e)
        await interaction.followup.send('Sorry, something went horribly wrong try again later or try something else.')


@bot.tree.command(name="drawd2", description="Ask me to draw something with dalle 2. e.g toaster monster. Image sizes are small,medium and large")#really badly drawn stuff lol
async def drawpic(interaction:discord.Interaction, *, what_to_draw: str,number_of_pics:int=GPT_DALL_E_2_NUMBER_OF_IMAGES,pic_size:str=GPT_DALL_E_2_SIZE):
    #defer the response so we can get the image and then send it later, by default the response is sent after 3 seconds if we dont defer it
    # if the defer is not used then the response will be sent before the image is retrieved and we get an error
    await interaction.response.defer()
    try:

        # Retrieve the API key from the environment variable.
        api_key = OPENAI_API_KEY
        size = pic_size
        DALL_E_2_ENGINE = GPT_DALL_E_2_ENGINE
        NUMBER_OF_IMAGES = number_of_pics
        DALL_E_2_QUALITY = GPT_DALL_E_2_QUALITY

        if number_of_pics > GPT_DALL_E_2_MAX_NUMBER_OF_IMAGES:
             await interaction.followup.send('Cannot produce more than ' + str(GPT_DALL_E_2_MAX_NUMBER_OF_IMAGES) + ' images. Please try a smaller number.')
             return


        response = ""
        title = what_to_draw

        if not api_key:
            return await interaction.followup.send('API key not set.')

        if GPT_DALL_E_2_ENGINE == 'dall-e-2':

            if size == "small":
                size = "256x256"
            elif size == "medium":
                size = "512x512"
            elif size == "large":
                size = "1024x1024"
            else:
                size = "256x256"
        else:
             return await interaction.followup.send('Invalid Engine Configured')


        if len(what_to_draw) >= 256 :
            title = what_to_draw[:128] + "..."


        async with aiohttp.ClientSession() as session:
            async with session.post('https://api.openai.com/v1/images/generations',headers={'Authorization': 'Bearer '+ OPENAI_API_KEY},
                                    json={
                                        'model': DALL_E_2_ENGINE,
                                        'prompt': what_to_draw,
                                        'n':NUMBER_OF_IMAGES, # Only 1 allowed for dalle 3 for now
                                        'size':size,
                                        'quality': DALL_E_2_QUALITY,
                                        }) as resp:
                if resp.status == 400:
                    print(resp._body)
                    return await interaction.followup.send('Im not allowed to draw that' + frown)
                elif resp.status != 200:
                    #print("hi")
                    return await interaction.followup.send('Could not get image... ' + frown)
                response = await resp.json()

                if NUMBER_OF_IMAGES >= 1 and NUMBER_OF_IMAGES <= 4:
                    #we need to download the images and send them as files in the embed
                    image_urls = response['data']
                    files = []
                    embed = discord.Embed(title="Here is your image of : " + title , color=PRIMARY_EMBED_COLOR)
                    #now we get the url for each image and download it
                    for image in image_urls:
                        image_url = image['url']
                        async with session.get(image_url) as resp:
                            if resp.status != 200:
                                return await interaction.followup.send('Could not get image...')
                            data = io.BytesIO(await resp.read())
                            #need to check for special characters in the title

                            title = remove_special_characters(title)
                            #random file name with unix the timestamp this is to prevent the same file name being used by multiple users
                            file_name = str(int(time.time()))+"_"+ title + ".png"
                            files.append(discord.File(data, filename=file_name,description=what_to_draw))

                    #now we send the files another way would have been to use the embed.set_image(url=image_url) mutiple times but that would have been a waste of bandwidth
                    await interaction.followup.send(embed=embed,files=files)

    except Exception as e:
        # Handle exceptions and provide feedback to the user.
        print(e)
        await interaction.followup.send('Sorry, something went horribly wrong try again later or try something else.')

@bot.tree.command(name="helpme",description="Get some help")
async def helpme(interaction:discord.Interaction):
    embed = discord.Embed(title="Help", color=PRIMARY_EMBED_COLOR)
    embed.add_field(name="Version", value="Get the version of the bot", inline=True)
    embed.add_field(name="draw", value="Ask me to draw something e.g cute anime cat with dalle 3. Images sizes are large,landscape and portrait, large is selected by default.", inline=True)
    embed.add_field(name="drawd2", value="Ask me to draw something with dalle 2. e.g toaster monster. Images sizes are small,medium and large, large is selected by default.", inline=True)

    await interaction.response.send_message(embed=embed)


# Run the bot with the token
bot.run(TOKEN)
