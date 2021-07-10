import random

scenario = [[0 for i in range(20)] for j in range(20)]*20

# helper functions

def room_fits(roomx,roomy,roomw,rooml,sizerange,gamemap):

    #Check for size
    if roomw * rooml < sizerange[0] or roomw * rooml > sizerange[1]:
        return False
    
    # corners of bounding box for room (room must leave 1 space between itself and nearest)
    p1 = (roomx - 1,roomy - 1)
    p2 = (roomx + roomw + 2, roomy + rooml + 2)

    # Check if room is inside map
    
    mapwidth = len(gamemap[0])
    maplen = len(gamemap) // mapwidth


    if p1[0] < 0 or p1[1] < 0 or p2[0] >= mapwidth or p2[1] >= maplen:
        return False


    # iterate in game map passed, if a tile overlaps return false
    for y in range(p1[1],p2[1]+1):
        for x in range(p1[0],p2[0]+1):
            if gamemap[y][x] == 255:
                return False
    # Return true if no tiles overlap
    return True

def fill_room(roomx,roomy,roomw,rooml,gamemap):
    # Get corners
    p1 = (roomx,roomy)
    p2 = (roomx + roomw, roomy + rooml)

    # Write room
    for y in range(p1[1],p2[1]+1):
        for x in range(p1[0],p2[0]+1):
            gamemap[y][x] = 255




def graph_map(gamemap):
    SIZEOF_MAP = 1
    screen = ""
    for i in range((len(gamemap)//len(gamemap[0]))*SIZEOF_MAP):
        for j in range(len(gamemap[0])*SIZEOF_MAP):
            whereIminMap = i//SIZEOF_MAP,j//SIZEOF_MAP
            whereIminSquare = i%SIZEOF_MAP,j%SIZEOF_MAP
            if gamemap[whereIminMap[0]][whereIminMap[1]] == 255:
                screen += "██"
            elif gamemap[whereIminMap[0]][whereIminMap[1]] == 0:
                screen += ".."
            else:
                screen+= f"{gamemap[whereIminMap[0]][whereIminMap[1]]:02d}"
        screen += "\n"
    print(screen)

def generate_map(gamemap,areas,sizeof_areas=(15,25)):
    
    # usefull variables:
    mapw = len(gamemap[0])
    mapl = len(gamemap)//mapw
    

    
    rooms = []
    tempmap = gamemap.copy()
    
    # Part 1: Generate the rooms:
    
    mapGeneratedSuccesfully = False
    while not mapGeneratedSuccesfully:
        # Make 100 attempts to generate more rooms
        tempmap = [i.copy() for i in gamemap]
        roompos = []
        roomsgenerated = 0
        for i in range(100):
            # Generate candidate room
            x = random.randint(1,mapw)
            y = random.randint(1,mapl)
            w = random.randint(3,sizeof_areas[1]//2)
            l = random.randint(3,sizeof_areas[1]//2)
            
            # Check if viable:
            if room_fits(x,y,w,l,sizeof_areas,tempmap):
                roomsgenerated += 1
                roompos.append((x,y,w,l))
                fill_room(x,y,w,l,tempmap)

            # Check if finished
            if roomsgenerated == areas:
                mapGeneratedSuccesfully = True
                break

    gamemap = [i.copy() for i in tempmap]
    graph_map(gamemap)

    
    # Part 2: Generate the walls:
    for y in range(1,mapl - 1):
        for x in range(1,mapw - 1):
            # if all adjacent blocks are member of room:
            if tempmap[y-1][x] and tempmap[y+1][x] and tempmap[y][x+1] and tempmap[y][x-1]:
                gamemap[y][x] = 0
    graph_map(gamemap)
    # Part 3: Generate doors
    print(rooms)
    for room in rooms:
        # 1 is top, 2 is left, 3 is bottom, 4 is right
        doorside = random.randint(1,4)
        print(doorside)
        if doorside == 1:
            # Top
            shift = random.randin(1,room[2]-1)
            pos = (room[0] + shift, room[1])
            gamemap[pos[0]][pos[1]] = 0
            print(pos)
        elif doorside == 2:
            # Left
            shift = random.randin(1,room[3]-1)
            pos = (room[0], room[1] + shift)
            gamemap[pos[0]][pos[1]] = 0
            print(pos)
        elif doorside == 3:
            # Bottom
            shift = random.randin(1,room[2]-1)
            pos = (room[0]+room[2]-shift,room[1]+room[3])
            gamemap[pos[0]][pos[1]] = 0
            print(pos)
        elif doorside == 4:
            # Right
            shift = random.randin(1,room[3]-1)
            pos = (room[0]+room[2],room[1]+room[3]-shift)
            gamemap[pos[0]][pos[1]] = 0
            print(pos)
    graph_map(gamemap)
    
            
generate_map(scenario,5)
