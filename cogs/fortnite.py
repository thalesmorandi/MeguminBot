from datetime import datetime, timedelta
from urllib.parse import quote
import aiohttp
import discord
from discord.ext import commands
class Fortnite():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def solo(self, *, player: str = ''):
        """Return solo stats for a player or yourself using Partybus.gg"""
        if len(player) > 0:
            embed = await self.player_stats(player, 1)
            if embed is not None:
                await self.bot.say(embed=embed)

    @commands.command()
    async def duo(self, *, player: str = ''):
        """Return duo stats for a player or yourself using Partybus.gg"""
        print(player)
        if len(player) > 0:
            print(player)
            embed = await self.player_stats(player, 2)
            print(embed)
            if embed is not None:
                await self.bot.say(embed=embed)

    @commands.command()
    async def squad(self, *, player: str = ''):
        """Return squad stats for a player or yourself using Partybus.gg"""
        if len(player) > 0:
            embed = await self.player_stats(player, 3)
            if embed is not None:
                await self.bot.say(embed=embed)

    async def player_stats(self, name, mode):
        """Get the general stats for a Fortnite player."""
        url = 'https://api.partybus.gg/v1/players/' + quote(name)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    js = await r.json()

                    embed = discord.Embed()

                    embed.title = js['details']['displayName']
                    embed.url = 'https://partybus.gg/player/' + quote(js['details']['displayName'])

                    platform = js['stats'][0]['platform']
                    if platform == 'pc':
                        embed.set_footer(text='PC',
                                         icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Windows_logo_-_2012.svg/768px-Windows_logo_-_2012.svg.png')
                        embed.colour = 44527
                    elif platform == 'ps4':
                        embed.set_footer(text='PS4',
                                         icon_url='https://psmedia.playstation.com/is/image/psmedia/404-three-column-playstationlogo-01-en-19feb15?$ThreeColFeature_Image$')
                        embed.colour = discord.Colour.dark_blue()
                    elif platform == 'xb1':
                        embed.set_footer(text='XB1',
                                         icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Xbox_one_logo.svg/2000px-Xbox_one_logo.svg.png')
                        embed.colour = 1080335

                    if mode == 1:
                        embed.description = 'Estatisticas Solo'
                        for stat in js['stats']:
                            if stat['p'] == 2:
                                minutes = timedelta(minutes=int(stat['minutes']))
                                time = datetime(1, 1, 1) + minutes
                                time = '{}D {}H {}M'.format(time.day - 1, time.hour, time.minute)
                                embed.description += f' ({time})'
                                embed.add_field(name='Partidas Totais', value=str(stat['games']))
                                embed.add_field(name='Vitorias', value=str(stat['placeA']))
                                embed.add_field(name='Win Rate',
                                                value=str(round(stat['placeA'] / stat['games'] * 100, 2)) + '%')
                                embed.add_field(name='KD Ratio',
                                                value=str(round(stat['kills'] / (stat['games'] - stat['placeA']), 1)))
                                embed.add_field(name='Top 10s', value=str(stat['placeB']))
                                embed.add_field(name='Top 25s', value=str(stat['placeC']))
                                return embed
                        return None
                    elif mode == 2:
                        embed.description = 'Estatisticas Dupla'
                        for stat in js['stats']:
                            if stat['p'] == 10:
                                minutes = timedelta(minutes=int(stat['minutes']))
                                time = datetime(1, 1, 1) + minutes
                                time = '{}D {}H {}M'.format(time.day - 1, time.hour, time.minute)
                                embed.description += f' ({time})'
                                embed.add_field(name='Partidas Totais', value=str(stat['games']))
                                embed.add_field(name='Vitorias', value=str(stat['placeA']))
                                embed.add_field(name='Win Rate',
                                                value=str(round(stat['placeA'] / stat['games'] * 100, 2)) + '%')
                                embed.add_field(name='Kill Rate', value=str(round(stat['kills'] / stat['games'], 1)))
                                embed.add_field(name='Top 5s', value=str(stat['placeB']))
                                embed.add_field(name='Top 12s', value=str(stat['placeC']))
                                return embed
                        return None
                    elif mode == 3:
                        embed.description = 'Estatisticas Esquadrão'
                        for stat in js['stats']:
                            if stat['p'] == 9:
                                minutes = timedelta(minutes=int(stat['minutes']))
                                time = datetime(1, 1, 1) + minutes
                                time = '{}D {}H {}M'.format(time.day - 1, time.hour, time.minute)
                                embed.description += f' ({time})'
                                embed.add_field(name='Partidas Totais', value=str(stat['games']))
                                embed.add_field(name='Vitorias', value=str(stat['placeA']))
                                embed.add_field(name='Win Rate',
                                                value=str(round(stat['placeA'] / stat['games'] * 100, 2)) + '%')
                                embed.add_field(name='Kill Rate', value=str(round(stat['kills'] / stat['games'], 1)))
                                embed.add_field(name='Top 3s', value=str(stat['placeB']))
                                embed.add_field(name='Top 6s', value=str(stat['placeC']))
                                return embed
                        return None
                    elif mode == 4:
                        embed.description = 'Overall Statistics'
                        kills = time = Vitorias = top25 = top10 = games = 0
                        for stat in js['stats']:
                            games += stat['games']
                            kills += stat['kills']
                            time += stat['minutes']
                            Vitorias += stat['placeA']
                            top10 += stat['placeB']
                            top25 += stat['placeC']
                        minutes = timedelta(minutes=int(time))
                        time = datetime(1, 1, 1) + minutes
                        time = '{}D {}H {}M'.format(time.day - 1, time.hour, time.minute)
                        embed.description += f' ({time})'
                        embed.add_field(name='Partidas Totais', value=str(games))
                        embed.add_field(name='Vitorias', value=str(Vitorias))
                        embed.add_field(name='Win Rate', value=str(round(Vitorias / games * 100, 2)) + '%')
                        embed.add_field(name='Kill Rate', value=str(round(kills / games, 1)))
                        embed.add_field(name='Top 25%', value=str(round(top25 / games * 100, 2)) + '%')
                        embed.add_field(name='Top 10%', value=str(round(top10 / games * 100, 2)) + '%')
                        return embed

def setup(bot):
    bot.add_cog(Fortnite(bot))