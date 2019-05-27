import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        for chan in self.get_all_channels():
            if chan.name == 'general':
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
                await message.channel.send(f'Reproduciendo video: {mes[6:]}')
            if mes[1:] == 'reset' and message.author == 'Metroid#4781':
                await message.channel.send('Reseteando bot..')
        print(f'Message from {message.author}: {message.content}')


client = MyClient()
client.run('NTgyNTc1OTc2MTkwNTc0NTk3.XOv1Cw.Tz2X0OzrNjK4NXB4sh6NjSD99pU')
