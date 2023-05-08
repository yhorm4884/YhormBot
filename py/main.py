#Para tener un código más limpio vamos a meter todas las importaciones en otro archivo.
from __init__ import  *

# Para que la gente pueda realizar reacciones de gif dentro del chat
links = json.load(open("./src/json/gifs.json"))
#Libro de Chistes
ficheros = fichero.fichero("./chistes.txt", ";")
ficheros.generarListaChistes()
#Variables de control para el funcionamiento del bot
intents = discord.Intents.all()
intents.members = True
command = commands.Bot(command_prefix='y!',
                    description='YhormBot',
                    intents=intents,
                    #Activo esto para que el propio bot pueda hacer los everyone en caso de anuncios
                    allowed_mentions=discord.AllowedMentions(everyone=True),
                    kick_members=True)
client = discord.Client(intents=intents)




###EVENTOS
@command.event


#Evento al iniciar el bot
async def on_ready():
	await command.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='lloros de yhorm'))
	print('Yhorm está despierto')
	discord.Intents.members = True
	try:
		synted = await command.tree.sync()
		print(f"Synced {len(synted)} command(s)")
	except Exception as e:
		print(e)

#Evento al unirse un miembro:

async def on_member_join(member):
	#add the channel id in which you want to send the card
	channel = command.get_channel(776171604551008277)

	#if you want to give any specific roles to any user then you can add like this
	role = get(member.guild.roles, name="Miembro")
	await member.add_roles(role)

	pos = sum(m.joined_at < member.joined_at for m in member.guild.members
			if m.joined_at is not None)

	if pos == 1:
		te = "st"
	elif pos == 2:
		te = "nd"
	elif pos == 3:
		te = "rd"
	else:
		te = "th"

	background = Editor("windows.jpg")
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

	file = File(fp=background.image_bytes, filename="22206.jpg")

	await channel.send(
	    f"Ey {member.mention}! Eres bienvenido/a a **{member.guild.name} para más información dirígete a  <#693092008608137256>**"
	)

	await channel.send(file=file)

async def on_member_remove(member):
	channel = command.get_channel(776171604551008277)

	await channel.send(f"{member.name} Se ha ido te echaremos de menos :( ")

# help pages
page1 = discord.Embed(
    title="Bot Help 1",
    description="Use the buttons below to navigate between help pages.",
    colour=discord.Colour.red())
page2 = discord.Embed(title="Bot Help 2",
                    description="Page 2",
                    colour=discord.Colour.blue())
page3 = discord.Embed(title="Bot Help 3",
                    description="Page 3",
                    colour=discord.Colour.dark_gold())

command.help_pages = [page1, page2, page3]

@command.tree.command(name="example")
async def example(interaction: discord.Integration):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)
    

@command.tree.command(name="pages", description="Prueba de sistema de paginado")
async def paginas(ctx,):
	buttons = [u"\u23EA", u"\u2B05", u"\u27A1",u"\u23E9"]  # skip to start, left, right, skip to end
	current = 0
	msg = ctx.send(embed=command.help_pages[current],ephemeral=True)

	for button in buttons:
		await msg.add_reaction(button)

	while True:
		try:
			reaction, user = await command.wait_for(
			"reaction_add",
			check=lambda reaction, user: user == ctx.author and reaction.
			emoji in buttons,
			timeout=60.0)

		except asyncio.TimeoutError:
			return print("test")

		else:
			previous_page = current
			if reaction.emoji == u"\u23EA":
				current = 0

			elif reaction.emoji == u"\u2B05":
				if current > 0:
					current -= 1

			elif reaction.emoji == u"\u27A1":
				if current < len(command.help_pages) - 1:
					current += 1

			elif reaction.emoji == u"\u23E9":
				current = len(command.help_pages) - 1

			for button in buttons:
				await msg.remove_reaction(button, ctx.author)

			if current != previous_page:
				await msg.edit(embed=command.help_pages[current])


#ver avatar del usuario
@command.tree.command(name="avatar", description="Mira el avatar de una persona :D")
async def avatar(ctx, member: discord.Member = None):
	member = ctx.author if not member else member
	embed = discord.Embed(title=member.name + "#" + member.discriminator)
	embed.set_image(url=member.avatar_url)
	await ctx.send(embed=embed)


@command.tree.command(name="gif", description="Muestra un gif de reacción")
# aliases=["hug", "love", "kill"]
@app_commands.choices(choices=[app_commands.Choice(name="Hug", value="hug"), app_commands.Choice(name="Love", value="love"), app_commands.Choice(name="Kill", value="kill")])
async def Gif(ctx, choices: app_commands.Choice[str], user: discord.Member):
    interaction = ctx.interaction

    if choices.value == "hug":
        if interaction.user.mention == ctx.author.mention or interaction.user.mention is None:
            await interaction.response.send_message(f"{interaction.user.mention} se ha abrazado a sí mismo")
        else:
            await interaction.response.send_message(f"{interaction.user.mention} ha sido abrazado por {ctx.author.mention}")
        await ctx.send(random.choice(links[choices.value]))
    elif choices.value == "kill":
        if interaction.user.mention == ctx.author.mention or interaction.user.mention is None:
            await ctx.send(f"{interaction.user.mention} se ha suicidado")
        else:
            await ctx.send(f"{interaction.user.mention} ha sido asesinado por {ctx.author.mention}")
        await ctx.send(random.choice(links[choices.value]))



#Comando de Ayudas
@command.tree.command(name="ayuda", description="'Muestra una pequeña ayuda del bot'")
async def ayuda(ctx,):
	embed = discord.Embed(title='HELP',
						description='Muestra una pequeña ayuda del bot',
						color=0xcd1aff)
	embed.set_author(
	    name='Yhorm #4884',
	    url='https://www.instagram.com/yhorm/',
	    icon_url=
	    'https://cdn.discordapp.com/avatars/610099597213433858/062a5425519065b3b946469dae18dcbe.png?size=2048'
	)
	embed.set_thumbnail(
	    url=
	    'https://discord.com/channels/@me/765276775205961739/770647516513304646'
	)
	embed.add_field(
	    name='info',
	    value='Muestra información básica del servidor (en desarollo)',
	    inline=True)
	embed.add_field(name='ban', value='Baneo de Personas', inline=True)
	embed.add_field(name='kick', value='kickear Personas', inline=True)
	embed.add_field(name='clear', value='Limpiar chat', inline=True)
	embed.add_field(name='chiste',
	                value='Cuenta un chiste random',
	                inline=True)
	embed.add_field(name='DM',
	                value='Manda un dm a la persona etiquetada',
	                inline=True)
	embed.add_field(name='avatar', value='Te muestra tu avatar', inline=True)
	embed.set_footer(
	    text='Este bot aún está en mantenimiento, disculpen las molestias.')
	await ctx.send(embed=embed)


# Informacion del server
@command.tree.command(name="info", description="muestra info del server")
async def info(ctx):
	icon_url = ctx.guild.icon_url
	embed = discord.Embed(title=f'{ctx.guild.name}',
						description='Datos Básicos',
						timestamp=datetime.datetime.utcnow(),
						color=discord.Color.red())
	embed.add_field(name='Creación del server ',value=f'{ctx.guild.created_at}')
	embed.add_field(name='Server ID', value=f'{ctx.guild.id}')
	embed.add_field(name='Propietario del command', value='Yhorm #4884')
	embed.set_thumbnail(url=icon_url)
	await ctx.send(embed=embed)


# funcion DM:  permite mandar un mensaje por privado por medio del command.
@command.command(name="dm", description="Envia dm a la persona etiquetada con un mensaje")
@commands.has_role("Administradores")
async def dm(ctx, user: discord.Member, *mensaje):
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


# funcion  chiste: muestra un chiste de forma aleatoria desde la lista.
@command.tree.command(name="chiste", description="Cuenta un chiste random entre los que tenemos registrados")
async def chiste(interaction: discord.Integration):
	embed = discord.Embed(title="Chistes Malos.",
						description=random.choice(
						ficheros.obtenerListaChistes()))
	await interaction.response.send_message(embed=embed)


# kickear usuarios
@command.tree.command(name="eliminar", description="Elimina a un usuario del servidor")
@commands.has_role("Administradores")
async def kick(ctx, user: discord.Member, *, reason:str):
    if user.guild_permissions.administrator:
        await ctx.send(f"No puedes expulsar a {user.mention} porque es un administrador")
    else:
        await user.kick(reason=reason)
        await ctx.send(f"{user.mention} ha sido expulsado del servidor")


# Banear usuarios
@command.tree.command(name='ban', description='Banea a un usuario del servidor')
@commands.has_role('Administradores')
async def ban(ctx: commands.Context, member: discord.Member, *, reason: str = 'No especificado'):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'{member.display_name} ha sido baneado del servidor por {reason}.')
    except discord.Forbidden:
        await ctx.send(f'No tengo permisos para banear a {member.display_name}.')
    except discord.HTTPException:
        await ctx.send(f'Ha ocurrido un error al intentar banear a {member.display_name}.')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send('No tienes el rol necesario para utilizar este comando.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Por favor, menciona al miembro que deseas banear.')
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send('El miembro mencionado no se encuentra en el servidor.')
    else:
        await ctx.send('Ha ocurrido un error al ejecutar este comando.')


# limpiar chat
@command.tree.command(name="clear", description="Limpiar chat")
@commands.has_role("Administradores")
async def clear(ctx, num: int = 10):
	try:
		async for message in ctx.channel.history(limit=num + 1):
			await message.delete()
	except:
		await ctx.send(f'No se ha podido realizar la acción')

# Warnear usuarios
@command.tree.command(name="warn", description="Aviso al personal")
@commands.has_role("Administradores")
async def warn_user(ctx, member: discord.Member, *, reason: str = None):
	try:
		mbed = discord.Embed(title='Has sido avisado ',
		                     color=discord.Color.red())
		mbed.add_field(name="Razón", value=reason, inline=True)
		await member.send(embed=mbed)
		await ctx.channel.send(member.mention + ' tienes un aviso!')
	except:
		await ctx.send(f'No se ha podido realizar la acción')



@command.command(name="slowmode", aliases=["sm"])
async def slowmode(ctx, sm: int, channel=None):
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


@command.tree.command(name="setnick", description="Establecer nick de persona")
@commands.has_permissions(manage_nicknames=True)
async def setnick(ctx, member: discord.Member, *, nick: str=None):
	old_nick = member.display_name
	await member.edit(nick=nick)
	new_nick = member.display_name

	await ctx.send(f'Changed nick from *{old_nick}* to *{new_nick}*')


#esto bloqueará el canal para que ningún usuario pueda enviar ningún mensaje
@command.tree.command(name="lock", description="Bloquear Canal temporalmente")
@commands.has_permissions(manage_channels=True)
async def lock(ctx, *, reason:str='None'):
	channel = ctx.channel
	overwrite = channel.overwrites_for(ctx.guild.default_role)
	overwrite.send_messages = False
	await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

	embed = discord.Embed(title=f'🔒 Canal bloqueado',
						description=f'Razón: {reason}')
	await channel.send(embed=embed)


@command.tree.command(name="unlock", description="Desbloquear canal")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, *, reason:str='None'):
	channel = ctx.channel
	overwrite = channel.overwrites_for(ctx.guild.default_role)
	overwrite.send_messages = True
	await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
	embed = discord.Embed(title=f'🔓 Canal desbloqueado',
						description=f'Razon: {reason}')
	await channel.send(embed=embed)
keep_alive()
command.run(token)