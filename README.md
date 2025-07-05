# Custom Services Uptime Discord Bot

A containerized service to manage an Amatuer Radio Discord Server

![Pipeline Status Badge]()

## Installation

Register at the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.

Fill out details on application to your own desire.

Add a bot in the Bot tab and reset token to get the Discord token required for operation.

Enable all privileged gateway intents on Bot page.

Go to OAuth2 -> URL Generator tab. Enable the `bot` scope and then add all permissions you feel comfortable adding for this API key. Then copy the url at the bottom and visit it with your authenticated Discord account in your browser to add the bot to your server.

Enable developer mode in your Discord client and [get the channel ID](https://turbofuture.com/internet/Discord-Channel-ID) for the dedicated channel to display the uptime dashboard.

Download and build the bot.

```bash
git clone git@https://github.com/W8FY/Ham-Discord-Bot.git`
cd Ham-Discord-Bot
cp example-config.yml config.yml
vi config.yml
```

Open config.yml and add Discord key for the bot and the channel IDs.

### Running with Python (Debugging)

Below are the commands to setup and run the bot with Python. This is great for debugging the config.yml file and testing the bot in general. You can do this to ensure that everything is working as intended before submitting an issue, and to ensure that your config.yml file is working as intended before deploying to production.

```bash
pip install -r requirements.txt
python main.py
```

### Running in Docker Container (Recommended)

The intended deployment of this bot is as a Docker container due to its non-persistent and daemon-like nature. We highly recommend using our Dockerfile to build the container once you have verified that your config.yml file works properly. In the future we hope to supply a Docker image that you can pull down and manage with a mounted config.yml instead.

```bash
docker build -t discord-uptime-bot .
docker run -d -v ./config.yml:/code/config.yml --name ham-discord-bot ham-discord-bot:latest
docker ps
```

## Usage

The config.yml file is the only necessary editing for this bot. You can place your token, channel IDs and more as shown below.

**Config.yml Example**

```yaml
---
DISCORD_TOKEN: 'SOMESUPERLONGSTRINGOFLETTERSANDMAYBENUMBERS' # Discord API key for bot created in developer portal.
CALLSIGN_CHANNEL_ID: 123456789101112 # Channel ID of dedicated channel for bot to listen for callsigns.
GENERAL_CHANNEL_ID: 123456789101112 # Channel ID of general discussion channel or anywhere you want new callsigns to be announced when people join.
LOGGING_CHANNEL_ID: 123456789101112 # Channel ID for bot logging to be send (Note: this should probably be a muted channel).
CLUB_CALL: 'W8FY'
```

## Support

Please open an [issue](https://github.com/W8FY/Ham-Discord-Bot/issues) if you have any problems. We will prioritize and help as we can.

## Roadmap

Please create issues for feature requests or any ideas. We will prioritize them and add them if they are a good fit.

## Authors and acknowledgment

### [Thad Turner](https://thadturner.com/) - Cybersecurity Practitioner

## License

MIT - please see [here](https://github.com/W8FY/Ham-Discord-Bot/blob/main/LICENSE).

## Project status

This project is not under steady development but I will add features and bugfixes as they come in or as they are requested by myself and others.
