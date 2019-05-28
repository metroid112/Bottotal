import discord
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pprint


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
        mes = message.content
        if mes[0] == '&':
            print(f'It\'s a command!')
            if mes[1:5] == 'play':
                request = youtube.search().list(
                    part="snippet",
                    maxResults=1,
                    q=mes[6:]
                )
                response = request.execute()
                pprint.pprint(response)
                await message.channel.send(f'Respuesta api youtube: {response}')
                await message.channel.send(f'Reproduciendo video: {mes[6:]}')
            if mes[1:5] == 'exit':
                await message.channel.send(f'Cerrando bot...')
                await self.close()
            if mes[1:6] == 'reset':
                await message.channel.send(f'Reseteando bot...')
                self.clear()
                await self.start('NTgyNTc1OTc2MTkwNTc0NTk3.XOv1Cw.Tz2X0OzrNjK4NXB4sh6NjSD99pU', bot=True)
        print(f'Message from {message.author}: {message.content}')


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client = MyClient()
client.run('NTgyNTc1OTc2MTkwNTc0NTk3.XOv1Cw.Tz2X0OzrNjK4NXB4sh6NjSD99pU')
