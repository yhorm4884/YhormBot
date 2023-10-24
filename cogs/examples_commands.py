from __init__ import discord, aiohttp, commands, app_commands
from prettyconf import config

class ExampleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Examples commands cog is ready.")
    
    @app_commands.command(name="example")
    async def example(self, interaction: discord.Integration):
        await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)
    
    @commands.command()
    async def gpt(self, ctx: commands.Context, *, prompt: str):
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "prueba",
                "prompt": prompt,
                "temperature": 0.5,
                "max_tokens": 50,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "best_of": 1
            }
            print(config('API_KEY'))
            headers = {"Authorization": config('API_KEY')}
            async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
                response = await resp.json()
                output_text = response['choices'][0]['text']
                embed = discord.Embed(title="Chat GPT's Respuesta:", description=output_text)
                await ctx.reply(embed=embed)

    @app_commands.command(name="pages", description="Prueba de sistema de paginado")
    async def paginas(self, interaction: discord.Interaction):
        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
        current = 0
        pages = [
            discord.Embed(title="Page 1", description="This is the first page."),
            discord.Embed(title="Page 2", description="This is the second page."),
            discord.Embed(title="Page 3", description="This is the third page.")
        ]
        await interaction.response.defer()
        msg = await interaction.followup.send(embed=pages[current])
        for button in buttons:
            await msg.add_reaction(button)
        while True:
            try:
                reaction, user = await self.command.wait_for(
                    "reaction_add",
                    check=lambda reaction, user: user == interaction.user and str(reaction.emoji) in buttons,
                    timeout=60.0
                )
            except TimeoutError:
                return print("Timeout")
            else:
                previous_page = current
                if str(reaction.emoji) == u"\u23EA":
                    current = 0
                elif str(reaction.emoji) == u"\u2B05":
                    if current > 0:
                        current -= 1
                elif str(reaction.emoji) == u"\u27A1":
                    if current < len(pages) - 1:
                        current += 1
                elif str(reaction.emoji) == u"\u23E9":
                    current = len(pages) - 1
                for button in buttons:
                    await msg.remove_reaction(button, interaction.user)
                if current != previous_page:
                    await msg.edit(embed=pages[current])
def setup(bot):
    bot.add_cog(ExampleCommands(bot))