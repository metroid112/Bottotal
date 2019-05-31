import discord
import os
import googleapiclient.discovery
import googleapiclient.errors
import pprint
import sqlite3

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


def sql(sentence):
    cursor_temp = db_connection.cursor()
    query_user = cursor_temp.execute(sentence).fetchall()
    cursor_temp.close()
    return query_user


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        for chan in self.get_all_channels():
            if chan.name == 'bot_pato':
                await chan.send(f'Inicializando SGR...')
                await chan.send(f'Explotando el servidor de fuentes...')
                await chan.send(f'Tirando los ambientes de argentina...')

    async def on_message(self, message):
        if message.author == client.user:
            return
        print(message)
        print(message.channel)
        print(message.content)
        if isinstance(message.content, str):
            if message.content[0] == '&':
                print(f'It\'s a command!')
                if message.content[1:7] == 'create':
                    await self.create_command(message)
                if message.content[1:5] == 'play':
                    request = youtube.search().list(
                        part="snippet",
                        maxResults=1,
                        q=message.content[6:]
                    )
                    response = request.execute()
                    pprint.pprint(response)
                    await message.channel.send(f'Respuesta api youtube: {response}')
                    await message.channel.send(f'Reproduciendo video: {message.content[6:]}')
                if message.content[1:5] == 'exit' and message.author.name == 'Metroid':
                    await message.channel.send(f'Cerrando bot...')
                    await self.close()
                if message.content[1:6] == 'reset' and message.author.name == 'Metroid':
                    await message.channel.send(f'Reseteando bot...')
                    self.clear()
                    await self.start('NTgyNTc1OTc2MTkwNTc0NTk3.XOv1Cw.Tz2X0OzrNjK4NXB4sh6NjSD99pU', bot=True)
            print(f'Message from {message.author.name}: {message.content}')

    async def create_command(self, message):
        query_user = sql(f'SELECT * FROM USERS WHERE USER_NAME = "{message.author.name}"')
        print(query_user)
        if len(query_user) == 0:
            query_id = sql(f'SELECT USER_ID FROM USERS')
            if len(query_id) == 0:
                user_id = 1
            else:
                user_id = query_id[len(query_id)][0]
            sql(f'INSERT INTO USERS VALUES({user_id}, "{message.author.name}")')
            await message.channel.send(f'Usuario nuevo, creando...')
        await create_character()




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
