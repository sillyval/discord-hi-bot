import sqlite3
import json

with open("config.json", "r") as file:
    config = json.loads(file.read())

database_file = config.get("database-file", "db/main.db")

def get_db():
    return sqlite3.connect(database_file)

def add_guild_entry(guildID = -1, interactions = 0):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO guilds (guildID, interactions)
        VALUES (?, ?)
    """, (
        guildID,
        interactions,
    ))
    conn.commit()
    conn.close()

def get_guild_interactions(guildID = -1):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT interactions FROM guilds 
        WHERE guildID=?;
    """, (
        guildID,
    ))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else 0

def get_guild_greeting_channel(guildID = -1):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT greetingChannel FROM guilds 
        WHERE guildID=?;
    """, (
        guildID,
    ))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def set_guild_greeting_channel(guildID = -1, greetingChannel = None):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE guilds
        SET greetingChannel = ?
        WHERE guildID=?;
    """, (
        greetingChannel,
        guildID,
    ))
    conn.commit()
    conn.close()

def get_guild_admin_role(guildID = -1):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT adminRole FROM guilds 
        WHERE guildID=?;
    """, (
        guildID,
    ))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def set_guild_admin_role(guildID = -1, adminRole = None):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE guilds
        SET adminRole = ?
        WHERE guildID=?;
    """, (
        adminRole,
        guildID,
    ))
    conn.commit()
    conn.close()
    
 
def is_blacklisted(channelID):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT channelID FROM blacklist WHERE channelID = ?", (channelID,))
    result = cur.fetchone()
    
    conn.close()

    if result:
        return True
    else:
        return False

def add_channel_to_blacklist(channelID):
    if not is_blacklisted(channelID):
        conn = get_db()
        cur = conn.cursor()

        cur.execute("INSERT INTO blacklist (channelID) VALUES (?)", (channelID,))
        
        conn.commit()
        conn.close()

def remove_channel_from_blacklist(channelID):
    if is_blacklisted(channelID):
        conn = get_db()
        cur = conn.cursor()

        cur.execute("DELETE FROM blacklist WHERE channelID = ?", (channelID,))
        
        conn.commit()
        conn.close()

def increment_guild(guildID = -1, increment = 1):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT interactions FROM guilds WHERE guildID = ?", (guildID,))
    result = cur.fetchone()
    
    if result:
        cur.execute("UPDATE guilds SET interactions = interactions + ? WHERE guildID = ?", (increment, guildID))
    else:
        cur.execute("INSERT INTO guilds (guildID, interactions) VALUES (?, ?)", (guildID, increment))
    
    conn.commit()
    conn.close()
