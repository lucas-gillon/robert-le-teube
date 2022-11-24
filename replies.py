from dotenv import dotenv_values
import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if "quoi" in message.content.lower():
            await message.reply("feur")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(dotenv_values()["TOKEN"])