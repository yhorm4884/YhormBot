from __init__ import commands, discord, app_commands
    
class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="dm", description="Envia dm a la persona etiquetada con un mensaje")
    @commands.has_role("Administradores")
    async def dm(self, ctx, user: discord.Member, *mensaje):
        try:
            if ctx.author.guild_permissions.administrator:
                texto = ""
                for i in mensaje:
                    if str(i) != "&":
                        texto += str(i) + " "
                    else:
                        texto += "\n"
                await user.send(texto)
                await ctx.message.delete()
            else:
                await ctx.send(f'No puedes porque no eres administrador <3')
        except discord.ext.commands.errors.MissingRole as error:
            await ctx.send(error)

    

    @app_commands.command(name="eliminar", description="Elimina a un usuario del servidor")
    @commands.has_role("Administradores")
    async def kick(self, ctx, user: discord.Member, *, reason:str):
        if user.guild_permissions.administrator:
            await ctx.send(f"No puedes expulsar a {user.mention} porque es un administrador")
        else:
            await user.kick(reason=reason)
            await ctx.send(f"{user.mention} ha sido expulsado del servidor")

    @app_commands.command(name='ban', description='Banea a un usuario del servidor')
    @commands.has_role('Administradores')
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = 'No especificado'):
        try:
            await member.ban(reason=reason)
            await ctx.send(f'{member.display_name} ha sido baneado del servidor por {reason}.')
        except discord.Forbidden:
            await ctx.send(f'No tengo permisos para banear a {member.display_name}.')
        except discord.HTTPException:
            await ctx.send(f'Ha ocurrido un error al intentar banear a {member.display_name}.')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            await ctx.send('No tienes el rol necesario para utilizar este comando.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Por favor, menciona al miembro que deseas banear.')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send('El miembro mencionado no se encuentra en el servidor.')
        else:
            await ctx.send('Ha ocurrido un error al ejecutar este comando.')

    @app_commands.command(name="clear", description="Limpiar chat")
    @commands.has_role("Administradores")
    async def clear(self, ctx, num: int = 10):
        try:
            async for message in ctx.channel.history(limit=num + 1):
                await message.delete()
        except:
            await ctx.send(f'No se ha podido realizar la acción')

    @app_commands.command(name="warn", description="Aviso al personal")
    @commands.has_role("Administradores")
    async def warn_user(self, ctx, member: discord.Member, *, reason: str = None):
        try:
            mbed = discord.Embed(title='Has sido avisado ',
                                color=discord.Color.red())
            mbed.add_field(name="Razón", value=reason, inline=True)
            await member.send(embed=mbed)
            await ctx.channel.send(member.mention + ' tienes un aviso!')
        except:
            await ctx.send(f'No se hapodido realizar la acción')

    @app_commands.command(name="slowmode", aliases=["sm"])
    async def slowmode(self, ctx, sm: int, channel=None):
        try:
            if channel is None:
                channel = ctx.channel
            if sm < 0:
                await ctx.send("El modo lento debe ser 0 o positivo")
                return
            else:
                await channel.edit(slowmode_delay=sm)
        except:
            await ctx.send(f'No se ha podido realizar la acción')

    @app_commands.command(name="setnick", description="Establecer nick de persona")
    @commands.has_permissions(manage_nicknames=True)
    async def setnick(self, ctx, member: discord.Member, *, nick: str=None):
        old_nick = member.display_name
        await member.edit(nick=nick)
        new_nick = member.display_name

        await ctx.send(f'Changed nick from *{old_nick}* to *{new_nick}*')

    @app_commands.command(name="lock", description="Bloquear Canal temporalmente")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction, *, reason:str='None'):
        channel = interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(title=f'🔒 Canal bloqueado',
                            description=f'Canal: {channel.mention}\nRazón: {reason}\n\nPor favor, no envíes mensajes en este canal mientras esté bloqueado.',
                            color=0xff0000)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unlock", description="Desbloquear canal")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        channel = interaction.channel
        overwrite = channel.overwrites_for(interaction.guild.default_role)
        overwrite.send_messages = None
        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)

        embed = discord.Embed(title=f'🔓 Canal desbloqueado',
                            description=f'Canal: {channel.mention}\n\nEl canal ha sido desbloqueado y ahora puedes enviar mensajes de nuevo.',
                            color=0x00ff00)
        await interaction.response.send_message(embed=embed)
def setup(bot):
    bot.add_cog(ModerationCommands(bot))