import discord
import json


with open("general_settings.json") as f:
    settings = json.load(f)


lvl1 = settings["secrets"]["Hokage"]
lvl2 = settings["secrets"]["Moderador"]
lvl3 = settings["secrets"]["Lodo Humano"]


def get(memb):
    lvl = [0]
    for r in memb.roles:
        if r.name in lvl3:
            lvl.append(3)
        elif r.name in lvl2:
            lvl.append(2)
        elif r.name in lvl1:
            lvl.append(1)
    return max(lvl)


def checklvl(memb, lvl):
    return get(memb) >= lvl


def check(member):
    if discord.utils.get(member.roles, name="Lodo Humano") is None:
        return False
    return True


def check_if_megumi(member):
    return member.id == "417982567699185665"
