import discord
import os
import googleapiclient.discovery
import googleapiclient.errors
import pprint
import sqlite3

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


def is_valid_name(name):
    valid_characters = set('qwertyuiopasdfghjklzxcvbnm')
    return all((character.lower() in valid_characters) for character in name)


def is_valid_class(class_id):
    return sql(f'SELECT * FROM CLASSES WHERE CLASS_ID = {class_id}')


def sql(sentence):
    cursor_temp = db_connection.cursor()
    print(sentence)
    try:
        query = cursor_temp.execute(sentence).fetchall()
    except Exception as error:
        return error
    db_connection.commit()
    cursor_temp.close()
    return query


async def create_class(message):
    class_name = message.content[16:].strip()
    if is_valid_name(class_name):
        query_class = sql(f'SELECT * FROM CLASSES WHERE CLASS_NAME = "{class_name}"')
        if not query_class:
            query_class = sql(f'SELECT CLASS_ID FROM CLASSES')
            if not query_class:
                class_id = 1
            else:
                class_id = query_class[-1][0] + 1
            sql(f'INSERT INTO CLASSES (CLASS_ID, CLASS_NAME) VALUES ({class_id}, "{class_name}")')
        else:
            await message.channel.send(f'Clase {class_name} ya existe')


async def create_command(message):
    query_user = sql(f'SELECT * FROM USERS WHERE USER_NAME = "{message.author.name}"')
    if not query_user:
        await message.channel.send(f'Usuario {message.author.name} no existe, creando...')
        await create_user(message)
    else:
        user_id = query_user[0][0]
        await create_character(message, user_id)


async def create_user(message):
    query_id = sql(f'SELECT USER_ID FROM USERS')
    if not query_id:
        user_id = 1
    else:
        user_id = query_id[-1][0] + 1
    sql(f'INSERT INTO USERS (USER_ID, USER_NAME) VALUES ({user_id}, "{message.author.name}")')
    await message.channel.send(f'Usuario nuevo ({user_id}, {message.author.name})')


async def create_character(message, user_id):
    name_separator = message.content[8:].index(' ') + 8
    class_separator = name_separator + 1
    character_name = message.content[8:name_separator].strip()
    try:
        class_id = int(message.content[class_separator:])
        if is_valid_name(character_name):
            if class_id != 0 and is_valid_class(class_id):
                query_character = sql(f'SELECT * FROM CHARACTERS WHERE USER_ID = {user_id} AND CHARACTER_NAME = "{character_name}"')
                if not query_character:
                    await message.channel.send(f'Personaje {character_name} no existe, creando...')
                    query_character = sql(f'SELECT CHARACTER_ID FROM CHARACTERS')
                    if not query_character:
                        character_id = 1
                    else:
                        character_id = sql(f'SELECT CHARACTER_ID FROM CHARACTERS')[-1][0] + 1
                    sql(f'INSERT INTO CHARACTERS (USER_ID, CHARACTER_ID, CLASS_ID, CHARACTER_NAME) VALUES ({user_id}, {character_id}, {class_id},"{character_name}")')
                else:
                    await message.channel.send(
                        f'Usuario {message.author.name} ya tiene un personaje llamado {character_name}')
            else:
                await message.channel.send(f'Elija un número de clase válido')
        else:
            await message.channel.send(f'El nombre {character_name} no es válido')
    except ValueError as error:
        await message.channel.send(f'La clase no es válida')
        print(error)


async def play_video(message):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=message.content[7:]
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
            if message.author == client.user or message.author.bot:
                return
            if not message.attachments:
                if message.content[0] == '&':
                    command = message.content
                    for i, j in enumerate(command):
                        print(i, j)
                    if command[1:6] == 'admin' and message.author.name == 'Metroid':
                        if command[7:15] == 'newclass':
                            await message.channel.send(f'Creando clase...')
                            await create_class(message)
                        if command[7:11] == 'exit':
                            await message.channel.send(f'Cerrando bot...')
                            await self.close()
                        if command[7:12] == 'reset':
                            await message.channel.send(f'Reseteando bot...')
                            self.clear()
                            await self.start('NTgyNTc1OTc2MTkwNTc0NTk3.XOv1Cw.Tz2X0OzrNjK4NXB4sh6NjSD99pU', bot=True)
                        if command[7:10] == 'sql':
                            await message.channel.send(f'Ejecutando SQL...')
                            await message.channel.send(sql(f'{command[11:]}'))
                        if command[7:11] == 'spam':
                            while True:
                                await message.channel.send(command[12:])
                        if command[7:11] == 'code':
                            message_code = ''
                            for line in open('bot.py', 'r').read():
                                message_code += line
                            pprint.pprint(message_code)
                            await message.channel.send('```' + message_code[:1994] + '```')
                            await message.channel.send('```' + message_code[1997:3991] + '```')
                            await message.channel.send('```' + message_code[3994:7988] + '```')
                            await message.channel.send('```' + message_code[7991:11885] + '```')
                    if command[1:5] == 'help':
                        if command[6:13] == 'classes':
                            await message.channel.send(sql(f'SELECT * FROM CLASSES'))
                    if command[1:7] == 'create':
                        await create_command(message)
                    if command[1:5] == 'play':
                        await play_video(message)
                print(f'{message.author.name}: {message.content}')
            # else:
            #     for attachment in message.attachments:
            #         await message.channel.send(attachment.url)
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
