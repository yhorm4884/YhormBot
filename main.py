#Para tener un código más limpio vamos a meter todas las importaciones en otro archivo.
from __init__ import json, discord, commands, Editor, load_image_async, Font, File, get
#Solamente importaremos webserver porque no se utilizará en el resto del código
from config.webserver import keep_alive
from prettyconf import config

class YhormBot:
    def __init__(self):
        self.links = json.load(open("./src/json/gifs.json"))
        self.intents = discord.Intents.all()
        self.intents.members = True
        self.intents.messages = True
        self.intents.reactions = True
        self.command = commands.Bot(command_prefix='y!',
                                    description='YhormBot',
                                    intents=self.intents,
                                    allowed_mentions=discord.AllowedMentions(everyone=True),
                                    kick_members=True)
        
    def run(self, token):
            self.command.start(token)
    
    async def main():
        bot = YhormBot()
        await bot.command.load_extension('cogs.help_commands')
        await bot.command.load_extension('cogs.examples_commands')
        await bot.command.load_extension('cogs.moderation_commands')
        await bot.command.load_extension('cogs.fun_commands')

    async def on_ready(self):
        
        await self.command.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='lloros de yhorm'))
        print('Yhorm está despierto')
        try:
            # Sincronizando comandos de barra "/"
            await self.command.tree.sync()
            print(f"Synced slash commands.")
        except Exception as e:
            print(e)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRole):
            await ctx.send("You forget u dont have permission role idiot.¯\_(ツ)_/¯")
    
    async def on_member_join(self, member):
        channel = self.command.get_channel(776171604551008277)
        role = get(member.guild.roles, name=config("ROL"))
        await member.add_roles(role)

        background = Editor("./src/img/windows.jpg")
        profile_image = await load_image_async(str(member.avatar_url))

        profile = Editor(profile_image).resize((300, 300)).circle_image()
        poppins = Font.poppins(size=60, variant="bold")

        background.paste(profile, (800, 250))
        background.ellipse((800, 250), 300, 300, outline="gold", stroke_width=4)

        background.text((600, 600),
                        f"Bienvenido a {member.guild.name}",
                        color="white",
                        font=poppins,
                        align="center")
        background.text((600, 650),f"{member.name}#{member.discriminator}",
                    color="white",
                    font=poppins,
                    align="center")

        file = File(fp=background.image_bytes, filename="./src/img/22206.jpg")

        await channel.send(
            f"Ey {member.mention}! Eres bienvenido/a a **{member.guild.name} para más información dirígete a  <#693092008608137256>**"
        )

        await channel.send(file=file)

    async def on_member_remove(self, member):
        channel = self.command.get_channel(776171604551008277)
        await channel.send(f"{member.name} Se ha ido te echaremos de menos :( ")
if __name__ == "__main__":
    
    bot = YhormBot()
    bot.command.event(bot.on_ready)
    keep_alive()
    bot.run(config('TOKEN'))