from __init__ import discord, commands, app_commands, json, random
from ..fichero import fichero


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.links = json.load(open("./src/json/gifs.json"))
        self.ficheros = fichero("./py/chistes.txt", ";")
        self.ficheros.generarListaChistes()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun commands cog is ready.")
        
    @app_commands.command(name="avatar", description="Mira el avatar de una persona :D")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        member = interaction.author if not member else member
        embed = discord.Embed(
            description=f"Aquí está el avatar de {member.mention}",
            color=member.color,
        )
        embed.set_author(
            name=f"Avatar de {member.name}#{member.discriminator}",
            icon_url=member.avatar.url,
        )
        embed.set_image(url=member.avatar.url)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="gif", description="Muestra un gif de reacción")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Gif", value="gif"),
        app_commands.Choice(name="Hug", value="hug"),
        app_commands.Choice(name="Kill", value="kill")
    ])
    async def gif(self, interaction: discord.Interaction, choice: app_commands.Choice[str], user: discord.Member):
        if choice.value == "gif":
            await interaction.response.send_message(random.choice(self.links[choice.value]))
        elif choice.value == "hug":
            if user.mention == interaction.user.mention:
                await interaction.response.send_message(f"¡{user.mention} se ha abrazado así mismo!\n",random.choice(self.links[choice.value]))
            else:
                await interaction.response.send_message(f"{user.mention} ha recibido un abrazo de {interaction.user.mention}!<{random.choice(self.links[choice.value])}>")
        elif choice.value == "kill":
            if user.mention == interaction.user.mention:
                await interaction.response.send_message(f"¡{user.mention} se ha suicidado!\n{random.choice(self.links[choice.value])}")
            else:
                await interaction.response.send_message(f"{user.mention} ha sido asesinado por {interaction.user.mention} 💔\n<{random.choice(self.links[choice.value])}>")
    
    @app_commands.command(name="chiste", description="Cuenta un chiste random entre los que tenemos registrados")
    async def chiste(self, interaction: discord.Integration):
        embed = discord.Embed(title="Chistes Malos.",
                            description=random.choice(
                            self.ficheros.obtenerListaChistes()))
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(FunCommands(bot))