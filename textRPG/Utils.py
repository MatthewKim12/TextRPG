from colorama import Fore, Back, init

init(autoreset = True)

MAP_RAND = 3
MAP_SIDE_LEN = 5
MAP_SIDE_CNT = 5
W, H = 20, 20
WALL_COUNT = 100
TILE_ROAD = 0
TILE_WALL = 1
TILE_PLAYER = 2
TILE_MONSTR = 3
TILE_POTION = 4
TILE_ARMOR = 5
TILE_WEAPON = 6
TILE_FINISH = 9
MAX_HP = 25
DEFEND_RANGE = (2, 4)
ATTACK_RANGE = (3, 6)
ARMOR_RANGE = (1, 2)
WEAPON_RANGE = (2, 3)

NUM_MONSTR = 10
NUM_POTION = 3
NUM_ARMOR = 5
NUM_WEAPON = 7
COMPONENTS = {
    TILE_ROAD: "  ", 
    TILE_WALL: "██", 
    TILE_PLAYER: "😀", 
    TILE_MONSTR: "🧟", 
    TILE_POTION: "⚗️ ", 
    TILE_ARMOR: "🛡️", 
    TILE_WEAPON: "🗡️", 
    TILE_FINISH: "🚩"
}

MONSTER_HP_RANGE = (15, 35)
MONSTER_ATK_RANGE = (6, 10)
MONSTER_DEFEND_RANGE = (3, 6)

INTRO = """
                                Text RPG
=======================================================================
                               a: move left
                               w: move front
                               s: move back
                               d: move right
                               i: inventory
                               p: drink potion
                               q: quit game
=======================================================================
"""

INTRO_BATTLE = """
                              Battle Scene
=======================================================================
                                e: escape
                                a: attack
                                d: defend
=======================================================================
"""

def isbound(x, y):
    return x >= 0 and x < W and y >= 0 and y < H

def printlist(strlist):
    for ln in strlist:
        for item in ln:
            print(Fore.BLUE + COMPONENTS[item], end = "")
        print("")

def printinventory(player, inventory, score):
    print(Back.GREEN + f"score: {score}")
    print(Back.BLUE + "=" * player.get_status(), end = "", flush = True)
    print(Back.RED + "-" * (MAX_HP - player.get_status()), end = "", flush = True)
    print(Back.CYAN + f" {player.get_status()}/{MAX_HP}")
    print(Back.WHITE + f"{COMPONENTS[TILE_POTION] * inventory.potions} | {COMPONENTS[TILE_ARMOR] * len(inventory.armors)} | {COMPONENTS[TILE_WEAPON] * len(inventory.weapons)}")

def print_battlescene(player, monster, inventory):
    print(COMPONENTS[TILE_PLAYER] + " " + Back.BLUE + "=" * player.get_status() + Back.RED + "-" * (MAX_HP - player.get_status()) + Back.CYAN + f" {player.get_status()}/{MAX_HP} " + Back.CYAN + COMPONENTS[TILE_POTION] * inventory.potions + COMPONENTS[TILE_ARMOR] * len(inventory.armors) + COMPONENTS[TILE_WEAPON] * len(inventory.weapons))
    print(COMPONENTS[TILE_MONSTR] + " " + Back.BLUE + "=" * monster.hp + f" {monster.hp}")

dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
def getnodes(x, y):
    nodes = []
    for dx, dy in dirs:
        if isbound(x + dx, y + dy):
            nodes.append((x + dx, y + dy))
    return nodes

def bfs(maze, start, end):
    in_check = [start]
    visited = []
    while len(in_check) > 0:
        x, y = in_check.pop(0)
        if x == end[0] and y == end[1]:
            return True # 비어있을때
        nodes = getnodes(x, y)
        for nodex, nodey in nodes:
            if maze[nodex][nodey] == TILE_ROAD and (nodex, nodey) not in visited:
                in_check.append((nodex, nodey))
                visited.append((nodex, nodey))
    return False