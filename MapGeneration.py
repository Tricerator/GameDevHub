def generateMap(MapWidth, MapHeight):

    # 0 = grass, 1 = rock
    import random

    intMap = []
    tileMap = []


    for row in range(MapHeight):
        intMap.append([])
        tileMap.append([])
        for column in range(MapWidth):
            intMap[row].append([0])
            tileMap[row].append(["G", "G", "G", "G"])


    for i in range(MapWidth * 3):
        x = random.randint(0, MapWidth - 1)
        y = random.randint(0, MapHeight - 1)

        intMap[x][y] = 1

        for xEdit in range(random.randint(-2, 0), random.randint(1, 2)):
            for yEdit in range(random.randint(-2, 0), random.randint(1, 2)):
                if random.randint(0, 100) > 25:
                    if x + xEdit > MapWidth - 1:
                        intMap[random.randint(10, MapWidth - 10)][random.randint(10, MapHeight - 10)] = 1
                    elif y + yEdit > MapHeight - 1:
                        intMap[random.randint(10, MapWidth - 10)][random.randint(10, MapHeight - 10)] = 1

                    else:
                        intMap[x + xEdit][y + yEdit] = 1



    for row in range(MapHeight):
        for column in range(MapWidth):
            if intMap[row][column] == 1:
                #tileCode = ["R", "R", "R", "R"]
                resultCode = "RRRR"

            else:
                tileCode = ["G", "G", "G", "G"]

                if intMap[row][column-1] == 1:  # Left
                    tileCode[0] = "R"
                    tileCode[2] = "R"

                if column + 1 < MapWidth and intMap[row][column + 1] == 1:  # Right
                    tileCode[1] = "R"
                    tileCode[3] = "R"

                if intMap[row - 1][column] == 1:  # Up
                    tileCode[2] = "R"
                    tileCode[3] = "R"

                if row + 1 < MapHeight and intMap[row + 1][column] == 1:  # Down
                    tileCode[0] = "R"
                    tileCode[1] = "R"

                resultCode = ""
                for i in tileCode:
                    resultCode += i

            tileMap[row][column] = resultCode

    for rowIndex in range(MapHeight):
        for columnIndex in range(MapWidth):
            if tileMap[rowIndex][columnIndex] == "GGGG":
                try:
                    if tileMap[rowIndex + 1][columnIndex][2] == "R":
                        tileMap[rowIndex][columnIndex] = "RGGG"

                    if tileMap[rowIndex - 1][columnIndex][1] == "R":
                        tileMap[rowIndex][columnIndex] = "GGGR"

                    if tileMap[rowIndex + 1][columnIndex][3] == "R":
                        tileMap[rowIndex][columnIndex] = "GRGG"

                    if tileMap[rowIndex - 1][columnIndex][0] == "R":
                        tileMap[rowIndex][columnIndex] = "GGRG"
                except:
                        pass

    return tileMap

#generateMap()