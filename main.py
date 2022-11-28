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
        sql = f"SELECT IF ( EXISTS ( SELECT * FROM times_pwned WHERE user ='{message.author}') ,'found','not " \
              f"found') "
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

        new_times = myresult[0][1] + 1
        sql = f"UPDATE times_pwned SET times = {new_times} WHERE user ='{message.author}'"
        mycursor.execute(sql)
        mydb.commit()

        await message.reply("feur")
    if str(bot.user.id) in message.content.lower():
        await message.reply("ptdr t ki")
        print("BOT USER ----------------------\n", bot.user)


@bot.slash_command(name="feur",
                   description="Tu veux savoir combien de fois tu as été feur ?")
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

    times = result[0][1]
    embed = discord.Embed(title=f"Tu as été feur {times} fois",
                          description="Gros nul",
                          color=discord.Color.blue()
                          )
    embed.set_author(name=result[0][0])
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

bot.run(dotenv_values()["TOKEN"])
