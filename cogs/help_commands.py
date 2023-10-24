from __init__ import discord, datetime, commands, app_commands

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help commands cog is ready.")

    @app_commands.command(name="ayuda", description="'Muestra una pequeña ayuda del bot'")
    async def ayuda(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Comandos de YhormBot",
            description="Aquí están los comandos disponibles del bot",
            color=0xcd1aff,
        )
        embed.set_author(
            name="Yhorm #4884",
            url="https://www.instagram.com/yhorm/",
            icon_url="https://media.tenor.com/Vlr5ep-dRXMAAAAd/ryan-gosling-blade-runner2049.gif",
        )
        embed.set_thumbnail(
            url="https://media.tenor.com/Vlr5ep-dRXMAAAAd/ryan-gosling-blade-runner2049.gif",
        )
        embed.add_field(
            name="/info",
            value="Muestra información básica del servidor (en desarollo)",
            inline=True,
        )
        embed.add_field(
            name="/ban",
            value="Banea a una persona del servidor",
            inline=True,
        )
        embed.add_field(
            name="/kick",
            value="Expulsa a una persona del servidor",
            inline=True,
        )
        embed.add_field(
            name="/clear",
            value="Limpia el chat de mensajes",
            inline=True,
        )
        embed.add_field(
            name="/chiste",
            value="Cuenta un chiste aleatorio",
            inline=True,
        )
        embed.add_field(
            name="/DM",
            value="Envía un mensaje directo a una persona",
            inline=True,
        )
        embed.add_field(
            name="/avatar",
            value="Muestra tu avatar de Discord",
            inline=True,
        )
        embed.set_footer(
            text="Este bot aún está en desarrollo, disculpen las molestias.",
        )
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="info", description="muestra info del server")
    async def info(self, interaction: discord.Interaction):
        icon_url = interaction.guild.icon
        embed = discord.Embed(title=f'{interaction.guild.name}',
                            description='Datos Básicos',
                            timestamp=datetime.datetime.utcnow(),
                            color=discord.Color.red())
        embed.add_field(name='Creación del server ',value=f'{interaction.guild.created_at}')
        embed.add_field(name='Server ID', value=f'{interaction.guild.id}')
        embed.add_field(name='Propietario del command', value='Yhorm #4884')
        embed.set_thumbnail(url=icon_url)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(HelpCommands(bot))
