# Dall E Bot
A Discord bot that utilizes OpenAI's DALL-E to generate images based on user prompts and Discord's API to interact within servers. The bot features 
 commands to draw images using DALL-E 2 or DALL-E 3 based on the user's description.                                                                 
                                                                                                                                                     
 ## Features                                                                                                                                         
                                                                                                                                                     
 - Generate images based on textual descriptions using DALL-E 2 or DALL-E 3.                                                                         
 - Customizable command prefix (`/` by default).                                                                                                    
 - Commands to retrieve bot version information.                                                                                                     
 - Help command providing descriptions of available commands.                                                                                        
                                                                                                                                                     
 ## Setup                                                                                                                                            
                                                                                                                                                     
 ### Requirements                                                                                                                                    
                                                                                                                                                     
 - Python 3.8 or higher                                                                                                                              
 - `discord.py` library                                                                                                                              
 - `aiohttp` library
 - `pip`
 - `python-dotenv`                                                                                                                               
 - An OpenAI API key with access to DALL-E models                                                                                                    
                                                                                                                                                     
 ### Installation                                                                                                                                    
                                                                                                                                                     
 1. **Clone the repository or download the source code.**                                                                                            
                                                                                                                                                     
    ```bash
    git clone https://github.com/itachi1621/Dall-E-Bot.git                                                                                                                       
                                                                                                                                                     

 2. **Navigate to the bot directory.**                                                                                                                    
                                                                                                                                                     
    cd path_to_bot                                                                                                                                   
                                                                                                                                                     
 3. **Install the required libraries using pip.**                                                                                                         
                                                                                                                                                     
    pip install discord aiohttp
    or
    pip install -r requirements.txt                                                                                                           
                                                                                                                                                     
 4 Create a `config.json` file in the root directory with the following structure and fill in your values a sample file called `config_sample.json` has been included for reference:                                             
                                                                                                                                                     
     {
      "Discord_Bot_Configuration": {
        "discord_bot_name":"DEB",
        "discord_bot_token": "",
        "version": "1.0.0",
        "primary_embed_color": "0x00ff00"
    },

    "OpenAI_Configuration":{
        "openai_key": "",
        "DALL-E-2-Config": {
            "GPT_Art_Engine": "dall-e-2",
            "GPT_Art_Quality": "standard",
            "GPT_Art_Size": "large",
            "Number_of_GPT_Art_Images": 2,
            "Max_IMAGES":6
        },
        "DALL-E-3-Config": {
            "GPT_Art_Engine": "dall-e-3",
            "GPT_Art_Quality": "standard",
            "GPT_Art_Size": "large",
            "Number_of_GPT_Art_Images": 2,
            "Max_IMAGES":6
        }

    }
    }

 5 create a `.env` file using the `env_sample` a put the full path to the config file after the `CONFIG_FILE_PATH=`  e,g /home/ubuntu/..../config.json
                                                                                                                                                
                                                                                                                                                     
 6 Run the bot with:                                                                                                                                 
                                                                                                                                                     
    python your_script_name.py   

## Setting Up the Discord Bot
1. Create a Discord Bot Application and obtain a bot token.
    - Go to the Discord Developer Portal.
    - Create a new application.
2. Under the "Bot" tab, click "Add Bot" and copy the token.
    - Paste your Discord bot token into config.json under "discord_bot_token" in the Discord_Bot_Configuration section.
3. Invite your bot to your Discord server.
    - Visit the OAuth2 URL generator in the Discord Developer Portal.
    - Select the "bot" scope and copy the generated URL.
    - Permissions needed are `Slash Commands`, `Send Messages` and `Send Messages in threads`
    - Paste the URL into your browser and select the server to invite the bot.
4. Run the bot script again after setup to start your Discord bot.                                                                                                                    
                                                                                                                                                     

  ## Available Commands                                                                  

 • `/version` - Get the version information of the bot.                                                                                                
 • `/draw` - Request the bot to generate an image based on a description using DALL-E 3.                                                               
 • `/drawd2` - Request the bot to generate an image based on a description using DALL-E 2.                                                             
 • `/helpme` - Show available commands and descriptions.                                                                                               

## Customization                                                                    

 • You can customize command prefixes, embed colors, and other settings through the config.json file.                                                


## Contributing                                                                     

Feel free to contribute by creating issues or submitting pull requests. Contributions to expand the bot's functionality, improve its performance, or 
fix bugs are always welcome.                                                                                                                         


## License                                                                       

This project is licensed under the MIT License. See the LICENSE file for details.                                                                    

