import random
from Utils import *
import Player
import Inventory
import Monster

def create_map2():
    gamemap = [[1 for _ in range(W)] for _ in range(H)]
    gamemap[0][0] = TILE_ROAD

    x, y = 0, 0
    nx, ny = 0, 0

    randdirs = [(1, 0), (0, 1)]
    spots = [(0, 0)]

    while x != W - 1 or y != H - 1:
        if x - y > MAP_RAND:
            nx = x
            ny = y + 1
        elif y - x > MAP_RAND:
            nx = x + 1
            ny = y
        else:
            bounddirs = list(filter(lambda direction: isbound(x + direction[0], y + direction[1]), randdirs))
            randx, randy = random.choice(bounddirs)
            nx = x + randx
            ny = y + randy
        gamemap[nx][ny] = 0
        spots.append((nx, ny))
        x = nx
        y = ny

    picked_spots = random.choices(spots, k = MAP_SIDE_CNT) # 숫자를 바꿔서 길 개수를 조정 할수 있다

    for x, y in picked_spots:
        length = 0
        movex = x
        movey = y
        dirx, diry = random.choice(list(filter(lambda direction: isbound(x + direction[0], y + direction[1]), [(0, 1), (1, 0), (0, -1), (-1, 0)])))
        while length <= MAP_SIDE_LEN and isbound(movex, movey):
            gamemap[movex][movey] = 0
            movex += dirx
            movey += diry
            length += 1

    gamemap[0][0] = TILE_PLAYER
    gamemap[W - 1][H - 1] = TILE_FINISH

    roads = [(i, i2) for i, line in enumerate(gamemap) for i2, component in enumerate(line) if component == TILE_ROAD]
    for _ in range(NUM_MONSTR):
        where = random.choice(roads)
        gamemap[where[0]][where[1]] = TILE_MONSTR
        roads.remove(where)
    
    for _ in range(NUM_POTION):
        where = random.choice(roads)
        gamemap[where[0]][where[1]] = TILE_POTION
        roads.remove(where)
    
    for _ in range(NUM_ARMOR):
        where = random.choice(roads)
        gamemap[where[0]][where[1]] = TILE_ARMOR
        roads.remove(where)
    
    for _ in range(NUM_WEAPON):
        where = random.choice(roads)
        gamemap[where[0]][where[1]] = TILE_WEAPON
        roads.remove(where)
    return gamemap, (0, 0), (W - 1, H - 1)
    # 1. (0, 0)에서 시작
    # 2. x-y가 정해진 값 (예: 3) 보다 더 클 경우, 무조건 y 좌표를 증가시키기
    # 3. y-x가 정해진 값 (예: 3) 보다 더 클 경우, 무조건 x 좌표를 증가시키기
    # 4. 2번 & 3번이 둘다 아닐경우, 랜덤으로 x증가 또는 y증가 고르기
    # 5. 고른곳을 파고, 그 지점을 기준점으로 설정
    # 6. 2번 ~ 5번을 (9, 9)에 도달할때까지 반복
    # 7. 1번 ~ 6번을 한 후, 판 곳에서 몇 군데를 고른다
    # 8. 7번에서 일정 길이 (예: 5) 를 도달 하거나, 맵 밖으로 나갈 경우 그만 파기

def create_map():
    gamemap = [[0 for _ in range(W)] for _ in range(H)]
    start = (0, 0)
    finish = (W - 1, H - 1)
    places = [(x, y) for x in range(W) for y in range(H)]
    random.shuffle(places)
    walls = 0
    for x, y in places:
        if walls > WALL_COUNT:
            break
        gamemap[x][y] = TILE_WALL
        if bfs(gamemap, start, finish):
            walls += 1
        else:
            gamemap[x][y] = TILE_ROAD
    # for _ in range(WALL_COUNT):
    #     x, y = random.choice(list(range(W))), random.choice(list(range(H)))
    #     while True:
    #         saved = gamemap[x][y]
    #         gamemap[x][y] = TILE_WALL
    #         if saved == TILE_ROAD and bfs(gamemap, start, finish):
    #             break
    #         gamemap[x][y] = saved
    #         x, y = random.choice(list(range(W))), random.choice(list(range(H))) # 다시 만들기
    gamemap[start[0]][start[1]] = TILE_PLAYER
    gamemap[finish[0]][finish[1]] = TILE_FINISH
    blanks = [(i, i2) for i, line in enumerate(gamemap) for i2, component in enumerate(line) if component == TILE_ROAD]
    for _ in range(NUM_MONSTR):
        x, y = random.choice(blanks)
        gamemap[x][y] = TILE_MONSTR
        blanks.remove((x, y))
    for _ in range(NUM_POTION):
        x, y = random.choice(blanks)
        gamemap[x][y] = TILE_POTION
        blanks.remove((x, y))
    for _ in range(NUM_ARMOR):
        x, y = random.choice(blanks)
        gamemap[x][y] = TILE_ARMOR
        blanks.remove((x, y))
    for _ in range(NUM_WEAPON):
        x, y = random.choice(blanks)
        gamemap[x][y] = TILE_WEAPON
        blanks.remove((x, y))
    return gamemap, start, finish

def battle(player, inventory):
    choices = ["a", "d"]
    print(INTRO_BATTLE)
    monster = Monster.Monster(random.randrange(MONSTER_HP_RANGE[0], MONSTER_HP_RANGE[1]), MONSTER_ATK_RANGE, MONSTER_DEFEND_RANGE)
    while True:
        print_battlescene(player, monster, inventory)
        if player.is_defeated():
            print("you lost...")
            return "dead"
        if monster.is_defeated():
            print("YOU WON!")
            return "won"
        mode = input("mode: ").strip().lower()
        monster_choice = choices[random.randrange(0, 2)]
        print(f"monster picked {monster_choice}!")
        if mode == "e":
            really = input("really? Are you going to escape the battle? (y/n): ")
            if really == "y":
                print("you escaped")
                return "flee"
        elif mode in choices:
            if mode == "a" and monster_choice == "a":
                monster.damaged(player.attack() + sum(inventory.weapons))
                player.damaged(monster.attack() - round(sum(inventory.armors)))
            elif mode == "a" and monster_choice == "d":
                monster.damaged((player.attack() + sum(inventory.weapons)) // 2) # float는 디스플레이에서 에러남; int만 가능
            elif mode == "d" and monster_choice == "a":
                player.damaged(monster.attack() - round(sum(inventory.armors)) // 2) # float는 디스플레이에서 에러남; int만 가능
            elif mode == "d" and monster_choice == "d":
                pass

def main():
    score = 0
    gamemap, start, end = create_map()
    player = Player.Player(start, MAX_HP, MAX_HP, DEFEND_RANGE, ATTACK_RANGE)
    inventory = Inventory.Inventory(0, [], [])
    print(INTRO)
    while True:
        if player.place == end:
            print("yay! We finished!")
            break
        printlist(gamemap)
        mode = input("mode: ").strip().lower()
        if mode == "q":
            really = input("really? Are you going to quit the game? (y/n): ")
            if really == "y":
                print("Quitting the game...")
                break
        elif mode == "i":
            printinventory(player, inventory, score)
        elif mode == "p":
            if inventory.use_potion():
                player.recover(MAX_HP)
                print("succesfully used the potion")
            else:
                print("you don't have a potion yet!")
        elif mode in ["w", "a", "s", "d"]:
            if mode == "w":
                dx, dy = -1, 0
            elif mode == "a":
                dx, dy = 0, -1
            elif mode == "s":
                dx, dy = 1, 0
            elif mode == "d":
                dx, dy = 0, 1
            nx, ny = player.place[0] + dx, player.place[1] + dy
            if not isbound(nx, ny):
                print("out of the map!")
                continue
            if gamemap[nx][ny] == TILE_WALL:
                print("it's a wall!")
                continue
            status = ""
            if gamemap[nx][ny] == TILE_POTION:
                inventory.add_potion()
                print("you got a potion!")
            elif gamemap[nx][ny] == TILE_ARMOR:
                defend = random.randrange(ARMOR_RANGE[0], ARMOR_RANGE[1])
                inventory.add_armor(defend)
                print(f"you got a armor! [{defend}]")
            elif gamemap[nx][ny] == TILE_WEAPON:
                attack = random.randrange(WEAPON_RANGE[0], WEAPON_RANGE[1])
                inventory.add_weapon(attack)
                print(f"you got a weapon! [{attack}]")
            elif gamemap[nx][ny] == TILE_MONSTR:
                print("oh no! It's a monster!")
                status = battle(player, inventory)
                if status == "dead":
                    break
                elif status == "won":
                    score += 10
            if status != "flee":
                gamemap[nx][ny] = TILE_PLAYER
                gamemap[player.place[0]][player.place[1]] = TILE_ROAD
                player.move(dx, dy)

main()
# player = Player.Player((0, 0), MAX_HP, MAX_HP, DEFEND_RANGE, ATTACK_RANGE)
# inventory = Inventory.Inventory(0, [2], [3])
# battle(player, inventory)
