import discord
from db import get_guild_admin_role, set_guild_admin_role

async def sendGreetMessage(channel: discord.channel, member: discord.member):
    await channel.send(f'hi {member.mention}')

def isAdmin(member: discord.member, guild: discord.guild, allowAdminRole=True):
    roleID = get_guild_admin_role(guild.id)

    if member == guild.owner:
        return True
    
    if member.guild_permissions.administrator:
        return True
    
    if roleID is None:
        return False
    
    if allowAdminRole:
        roles = member.roles
        for role in roles:
            if role.id == roleID:
                return True
        
    return False