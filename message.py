import json
import requests

def send(message="", user=""):
    message = f"{message}\nMention de l'utilisateur: {user}."
    webhook_url = 'https://discord.com/api/webhooks/843892338744754176/C--3UKf11cTkVytLfbvj3PurmxBJovkRR1uwl8zf5WCO80fgnu2V2jNqTBnKDy0F3rEx'
    discord_data = {'content': message, 'username': "Team Pêcheur | Aides/Plaintes"}
    response = requests.post(
        webhook_url, data=json.dumps(discord_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 204:
        raise ValueError(
            'Request to discord returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )

