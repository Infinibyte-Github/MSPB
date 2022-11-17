def motd_cleaner(motd:str):
    mc_codes = ["§0", "§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8", "§9", "§a", "§b", "§c", "§d", "§e", "§f","§g", "§l", "§n", "§k", "§m"]
        
    for code in mc_codes:
        motd = motd.replace(code, "")

    return motd