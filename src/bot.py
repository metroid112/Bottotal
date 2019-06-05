import discord
import os
import googleapiclient.discovery
import googleapiclient.errors
import pprint
import sqlite3
import json

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


def is_valid_character_name(name):
    valid_characters = set('qwertyuiopasdfghjklzxcvbnm')
    if all((character.lower() in valid_characters) for character in name):
        return True
    else:
        return False


def sql(sentence):
    cursor_temp = db_connection.cursor()
    print(sentence)
    try:
        query = cursor_temp.execute(sentence).fetchall()
    except (sqlite3.Warning, sqlite3.Error) as error:
        return error
    db_connection.commit()
    cursor_temp.close()
    return query


async def create_command(message):
    query_user = sql(f'SELECT * FROM USERS WHERE USER_NAME = "{message.author.name}"')
    print(query_user)
    if not query_user:
        await message.channel.send(f'Usuario {message.author.name} no existe, creando...')
        await create_user(message)
    else:
        user_id = query_user[0][0]
        await create_character(message, user_id)


async def create_user(message):
    query_id = sql(f'SELECT USER_ID FROM USERS')
    print(query_id)
    if not query_id:
        user_id = 1
    else:
        user_id = query_id[-1][0] + 1
    sql(f'INSERT INTO USERS (USER_ID, USER_NAME) VALUES ({user_id}, {message.author.name})')
    await message.channel.send(f'Usuario nuevo ({user_id}, {message.author.name})')


async def create_character(message, user_id):
    if is_valid_character_name(message.content[8:]):
        character_name = message.content[8:].strip()
        query_character = sql(f'SELECT * FROM CHARACTERS WHERE USER_ID = {user_id} AND CHARACTER_NAME = "{character_name}"')
        print(query_character)
        if not query_character:
            await message.channel.send(f'Personaje {character_name} no existe, creando...')
            query_character = sql(f'SELECT CHARACTER_ID FROM CHARACTERS')
            print(query_character)
            if not query_character:
                character_id = 1
            else:
                character_id = query_character[-1][0]
            sql(f'INSERT INTO CHARACTERS (USER_ID, CHARACTER_ID, CHARACTER_NAME) VALUES ({user_id}, {character_id}, "{character_name}")')
        else:
            await message.channel.send(f'Usuario {message.author.name} ya tiene un personaje llamado {character_name}')
    else:
        await message.channel.send(f'El nombre {message.content[8:]} no es válido')


async def play_video(message):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=message.content[6:]
    )
    json_response = request.execute()
    pprint.pprint(json_response)
    video_title = json_response['items'][0]['snippet']['title'].replace('&amp;', '&')
    video_id = json_response['items'][0]['id']['videoId']
    video_link = 'https://youtu.be/' + video_id
    await message.channel.send(f'Reproduciendo video: {video_link} - {video_title}')


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        for chan in self.get_all_channels():
            if chan.name == 'bot_pato':
                await chan.send(f'Inicializando SGR...')
                await chan.send(f'Explotando el servidor de fuentes...')
                await chan.send(f'Tirando los ambientes de argentina...')

    async def on_message(self, message):
        try:
            if message.author == client.user:
                return
            if isinstance(message.content, str):
                if message.content[0] == '&':
                    print(f'It\'s a command!')
                    if message.content[1:7] == 'create':
                        await create_command(message)
                    if message.content[1:5] == 'play':
                        await play_video(message)
                    if message.content[1:5] == 'exit' and message.author.name == 'Metroid':
                        await message.channel.send(f'Cerrando bot...')
                        await self.close()
                    if message.content[1:6] == 'reset' and message.author.name == 'Metroid':
                        await message.channel.send(f'Reseteando bot...')
                        self.clear()
                        await self.start('NTgyNTc1OTc2MTkwNTc0NTk3.XOv1Cw.Tz2X0OzrNjK4NXB4sh6NjSD99pU', bot=True)
                    if message.content[1:4] == 'sql' and message.author.name == 'Metroid':
                        await message.channel.send(f'Ejecutando SQL...')
                        await message.channel.send(sql(f'{message.content[5:]}'))
                    if message.content[1:5] == 'spam' and message.author.name == 'Metroid':
                        while True:
                            await message.channel.send(message.content[6:])
                if 'Maestruleitor' in message.author.name:
                    await message.channel.send(f'Bot gil, mira las boludeces que decis "{message.content}"')
            print(f'Message from {message.author.name}: {message.content}')
        except Exception as error:
            await message.channel.send(error)


db_connection = sqlite3.connect('bot.db')
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"
credential_path = os.path.join('credential_sample.json')
store = Storage(credential_path)
credentials = store.get()
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(client_secrets_file, scopes)
    credentials = tools.run_flow(flow, store)
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)
client = MyClient()
client.run('NTgyNTc1OTc2MTkwNTc0NTk3.XOv1Cw.Tz2X0OzrNjK4NXB4sh6NjSD99pU')
