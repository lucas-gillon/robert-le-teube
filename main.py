import discord
from discord.ext import commands
from dotenv import dotenv_values
import mysql.connector as mysql
from blagues_api import BlaguesAPI

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)
intents.message_content = True


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_message(message: discord.Message):
    if "quoi" in message.content.lower():
        mydb = mysql.connect(
            host=dotenv_values()["SQL_HOST"],
            user=dotenv_values()["SQL_USER"],
            password=dotenv_values()["SQL_PASSWORD"],
            database=dotenv_values()["SQL_DATABASE"]
        )
        mycursor = mydb.cursor()
        sql = f"SELECT IF ( EXISTS ( SELECT * FROM times_pwned WHERE user ='{message.author}') ,'found','not found') "
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        ifexists = myresult[0][0]

        if ifexists == "not found":
            mycursor = mydb.cursor()
            sql = f"insert into times_pwned(user, times) values ('{message.author}', 0)"
            mycursor.execute(sql)
            mydb.commit()

        mycursor.execute(f"SELECT * FROM times_pwned WHERE user ='{message.author}'")
        myresult = mycursor.fetchall()

        new_times = myresult[0][0] + 1
        sql = f"UPDATE times_pwned SET times = {new_times} WHERE user ='{message.author}'"
        mycursor.execute(sql)
        mydb.commit()

        await message.reply("feur")

    if str(bot.user.id) in message.content.lower():
        await message.reply("ptdr t ki")


@bot.slash_command(name="feur", description="Tu veux savoir combien de fois tu as été feur ?")
async def feur(ctx):
    mydb = mysql.connect(
        host=dotenv_values()["SQL_HOST"],
        user=dotenv_values()["SQL_USER"],
        password=dotenv_values()["SQL_PASSWORD"],
        database=dotenv_values()["SQL_DATABASE"]
    )
    mycursor = mydb.cursor()
    sql = f"SELECT IF ( EXISTS ( SELECT * FROM times_pwned WHERE user ='{ctx.author}') ,'found','not found') "
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    ifexists = myresult[0][0]

    if ifexists == "not found":
        mycursor = mydb.cursor()
        sql = f"insert into times_pwned(user, times) values ('{ctx.author}', 0)"
        mycursor.execute(sql)
        mydb.commit()

    mycursor.execute(f"SELECT * FROM times_pwned WHERE user ='{ctx.author}'")
    result = mycursor.fetchall()

    times = result[0][0]
    embed = discord.Embed(title=f"Tu as été feur {times} fois",
                          description="Gros nul",
                          color=discord.Color.blue()
                          )
    embed.set_author(name=result[0][1].split("#")[0])
    await ctx.respond(embed=embed)


@bot.slash_command(name="blague", description="blague random")
async def blague(ctx):
    blagues = BlaguesAPI(dotenv_values()["BLAGUE_TOKEN"])
    blague_random = await blagues.random()
    embed = discord.Embed(title=blague_random.joke,
                          description=blague_random.answer,
                          color=discord.Color.blue()
                          )
    embed.set_author(name="Blague Random")
    await ctx.respond(embed=embed)


@bot.slash_command(name="help", description="liste des commandes de Robert le Teubé")
async def commands(ctx):
    bot_pfp = bot.user.avatar.url
    embed = discord.Embed(title="Liste des commandes",
                          description="liste des commandes de Robert le Teubé",
                          color=discord.Color.blue()
                          )
    embed.set_author(name=bot.user.name)
    embed.set_thumbnail(url=bot_pfp)
    embed.add_field(name="`/feur`", value="Pour savoir combien de fois tu as été 'feur'",
                    inline=False)
    embed.add_field(name="`/blague`", value="Pour afficher une blague random",
                    inline=False)
    embed.set_footer(text="Et plus à venir!")
    await ctx.respond(embed=embed)


bot.run(dotenv_values()["TOKEN"])
