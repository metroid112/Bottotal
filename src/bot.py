import discord


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
        if mes[0] == '&' and message.channel == 'bot_pato':
            print(f'It\'s a command!')
            if mes[1:5] == 'play':
                await message.channel.send(f'Reproduciendo video: {mes[6:]}')
            if mes[1:5] == 'exit':
                await message.channel.send(f'Cerrando bot...')
                await self.close()
            if mes[1:6] == 'reset':
                await message.channel.send(f'Reseteando bot...')
                self.clear()
                await self.start('NTgyNTc1OTc2MTkwNTc0NTk3.XOv1Cw.Tz2X0OzrNjK4NXB4sh6NjSD99pU', bot=True)
        print(f'Message from {message.author}: {message.content}')


client = MyClient()
client.run('NTgyNTc1OTc2MTkwNTc0NTk3.XOv1Cw.Tz2X0OzrNjK4NXB4sh6NjSD99pU')
