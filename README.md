# robert-le-teube  
This is my first Discord bot, made in Python with [Pycord](https://docs.pycord.dev/en/stable/)  

You can use the following commands :  

- `/feur` : 
    - bot responds to see how many times you got pwned  
        - if it's the first time you use this command, you are written in database with your discord ID and 0 times pwned
- `/blague` :
  - displays a random joke in <u>**French**</u>
  - using [blagues_api PyPi](https://www.blagues-api.fr/) package
- `/help` :
  - Displays a list of all commands of the bot
- `/wiki`:
  - resumes a Wikipedia article that you search for with `query` param
  - using [Wikipedia](https://pypi.org/project/wikipedia/) package

Things that are done automatically :

- The bot responds to `quoi` with `feur` :  
    - if it is the first time, you are written in database with your discord ID and 0 times, and each time you get pwned, this number increments  
