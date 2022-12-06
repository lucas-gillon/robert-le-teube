import discord
import wikipedia
import pymongo
from blagues_api import BlaguesAPI
from discord.ext import commands
from dotenv import dotenv_values

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)
intents.message_content = True

client = pymongo.MongoClient(dotenv_values()["MONGODB_URL"])
db = client[dotenv_values()["MONGODB_DATABASE"]]
col = db[dotenv_values()["MONGODB_COLLECTION"]]


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.event
async def on_message(message: discord.Message):
    if "quoi" in message.content.lower():
        user: object = {}
        for x in col.find({}, {"name": str(message.author), "times_pwned": 1}):
            x.pop("_id")
            user = x
        is_user: bool = False

        try:
            if user["name"] == str(message.author):
                is_user = True
        except KeyError:
            user = {"name": "", "times_pwned": 0}

        if not is_user:
            new_user = {"name": str(message.author), "times_pwned": 0}
            col.insert_one(new_user)
            myquery = {"name": str(message.author)}
            new_values = {"$set": {"times_pwned": user["times_pwned"] + 1}}

            col.update_one(myquery, new_values)
        else:
            myquery = {"name": str(message.author)}
            new_values = {"$set": {"times_pwned": user["times_pwned"] + 1}}

            col.update_one(myquery, new_values)

        await message.reply("feur")

    if str(bot.user.id) in message.content.lower():
        await message.reply("ptdr t ki")


@bot.slash_command(name="feur", description="Tu veux savoir combien de fois tu as été feur ?")
async def feur(ctx):
    user: object = {}
    for x in col.find({}, {"name": str(ctx.author), "times_pwned": 1}):
        x.pop("_id")
        user = x

    is_user: bool = False

    try:
        if user["name"] == str(ctx.author):
            is_user = True
            print("is user", is_user, user)
    except KeyError:
        user = {"name": "patate", "times_pwned": 0}
        print(user)

    if not is_user:
        new_user = {"name": str(ctx.author), "times_pwned": 0}
        col.insert_one(new_user)
    times = user["times_pwned"]
    
    embed = discord.Embed(title=f"Tu as été feur {times} fois",
                          description="Gros nul",
                          color=discord.Color.blue()
                          )
    embed.set_author(name=user["name"].split("#")[0])
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
    embed = discord.Embed(title="Liste des commandes de Robert le Teubé",
                          color=discord.Color.blue()
                          )
    bot_pfp = bot.user.avatar.url
    embed.set_thumbnail(url=bot_pfp)
    embed.add_field(name="`/feur`", value="Pour savoir combien de fois tu as été 'feur'",
                    inline=False)
    embed.add_field(name="`/blague`", value="Pour afficher une blague random",
                    inline=False)
    embed.add_field(name="`/wiki`", value="Pour rechercher des informations sur Wikipedia.\n"
                                          "Si le mot recherché est 'random', un article au hasard sera résumé.\n"
                    )
    embed.set_footer(text="Et plus à venir!")
    await ctx.respond(embed=embed)


@bot.slash_command(name="wiki", description="Recherche sur Wikipedia")
async def wiki(ctx, query):
    try:
        if query == "random":
            embed = discord.Embed(title="Vous avez recherché un article au hasard sur Wikipedia :",
                                  color=discord.Color.light_gray()
                                  )
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png")
            wikipedia.set_lang("fr")
            article = wikipedia.random(pages=1)
            embed.add_field(name=article, value=wikipedia.summary(article))
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="Vous avez recherché sur Wikipedia :",
                                  color=discord.Color.light_gray()
                                  )
            embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png")
            wikipedia.set_lang("fr")
            article = wikipedia.summary(query, sentences=2)
            embed.add_field(name=query.capitalize(), value=article)
            await ctx.respond(embed=embed)
    except wikipedia.exceptions.PageError:
        embed = discord.Embed(title="Vous avez recherché sur Wikipedia :",
                              color=discord.Color.light_gray()
                              )
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png")
        embed.add_field(name=query, value="la recherche n'a rien donné")
        embed.set_footer(text="Essayez autre chose")
        await ctx.respond(embed=embed)


bot.run(dotenv_values()["TOKEN"])
