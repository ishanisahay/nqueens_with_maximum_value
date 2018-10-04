import time

maxReward = 0
rewards = []

def assignRowCol(row, col, grid, n):

    for i in xrange(n):
        if grid[row][i] == 0:
            grid[row][i] = -1

    for i in xrange(n):
        if grid[i][col] == 0:
            grid[i][col] = -1

    x = row
    y = col
    #upper left diag
    while (y >= 0 and x >=  0):
        if grid[x][y] == 0:
            grid[x][y] = -1
        y = y-1
        x = x-1


    x = row
    y = col
    #lower left diag
    while (y >= 0 and x < n):
        if grid[x][y] == 0:
            grid[x][y] = -1
        y = y-1
        x = x+1

    x = row
    y = col
    #upper right diag
    while (y < n and x >= 0):
        if grid[x][y] == 0:
            grid[x][y] = -1
        y = y+1
        x = x-1

    x = row
    y = col
    #lower right diag
    while (y < n and x < n):
        if grid[x][y] == 0:
            grid[x][y] = -1
        y = y+1
        x = x+1


def isPlaceable(n,p,grid, row, col):

    #same row
    for i in xrange(n):
        if grid[row][i] == 1:
            return False

    #same col
    for i in xrange(n):
        if grid[i][col] == 1:
            return False

    x = row
    y = col
    #upper left diag
    while (y >= 0 and x >=  0):
        if grid[x][y] == 1:
            return False
        else:
            y = y-1
            x = x-1


    x = row
    y = col
    #lower left diag
    while (y >= 0 and x < n):
        if grid[x][y] == 1:
            return False
        else:
            y = y-1
            x = x+1

    x = row
    y = col
    #upper right diag
    while (y < n and x >= 0):
        if grid[x][y] == 1:
            return False
        y = y+1
        x = x-1

    x = row
    y = col
    #lower right diag
    while (y < n and x < n):
        if grid[x][y] == 1:
            return False
        y = y+1
        x = x+1

    return True

def isGoalStateReached(count, police):
    #no of assigned is equal to police in a grid
    if count == police:
        return True
    else:
        return False

def checkIfCurrentIterShouldBeSkipped(curReward, police, cnt, val):
    #if the maximum possible reward is less than maxReward, we should break
    global maxReward
    if (curReward + ((police - cnt) * val)) < maxReward:
        return True

    if (curReward + ((police - cnt) * val)) == maxReward:
        return True

    return False

def placePolToMaxRewardUsingDFS(start, grid,row, col, n,police, cnt, sortedRewardsDict, curReward):

    global points
    global solutions
    global maxReward

    curTime = time.time()
    if curTime - start >= 172:
        return

    if police <= n:
        len_of_rewards = len(sortedRewardsDict)
        for m in xrange(len_of_rewards):

            count = cnt
            z = sortedRewardsDict[m]
            rewardCoords = z[0]
            val = int(z[1])
            x = rewardCoords.split(",")
            xc = int(x[0])
            yc = int(x[1])

            #check if now incoming coords have reward as 0, consider only if current reward is greater than max
            #we have
            if val == 0:
                if curReward < maxReward:
                    break
            #check max reward that is possible with this val and curReward of grid
            if checkIfCurrentIterShouldBeSkipped(curReward, police, cnt, val):
                break

            if grid[xc][yc] == 0 and isPlaceable(n, police, grid, xc, yc):
                grid_copy = [tmp[:] for tmp in grid]
                grid_copy[xc][yc] = 1
                assignRowCol(xc, yc, grid_copy, n)
                count += 1

                curReward = curReward + val
                if isGoalStateReached(count, police):
                    point = curReward
                    if point > maxReward:
                        maxReward = point
                    break

                placePolToMaxRewardUsingDFS(start, grid_copy, 0, 0, n, police, count, sortedRewardsDict[m+1:], curReward)
                curReward = curReward - val


def pointsCountGrid(grid, n, police):
    global rewards
    point = 0
    cnt = 0
    for i in xrange(n):
        for j in xrange(n):
            if grid[i][j] == 1:
                point += rewards[i][j]
                cnt += 1
                if cnt == police:
                    return point
    return point


def createRewards(scooterpoints, n):
    global rewards

    for i in xrange(n):
        l = []
        for j in xrange(n):
            l.append(0)
        rewards.append(l)

    len_of_scooterpoints = len(scooterpoints)
    for i in xrange(3,len_of_scooterpoints,1):
        coords = scooterpoints[i].split(",")
        x = int(coords[0])
        y = int(coords[1])
        rewards[x][y] += 1

    tmp = {}
    for i in xrange(0,n):
        for j in xrange(0,n):
            key = str(i) + "," + str(j)
            tmp[key] = rewards[i][j]

    sortedRewardsDict = (sorted(tmp.items(), key=lambda x: x[1], reverse=True))
    return sortedRewardsDict


def main():

    start = time.time()
    global maxReward
    fp = open("input.txt", 'r')

    lines = fp.read().splitlines()
    fp.close()

    n = int(lines[0])
    k = int(lines[1])

    grid = [0]*n
    for i in xrange(n):
        grid[i] = [0]*n

    sortedRewardsDict = createRewards(lines, n)
    placePolToMaxRewardUsingDFS(start, grid, 0, 0, n, k, 0, sortedRewardsDict, 0)
    #print maxReward
    fw = open("output.txt", 'w')
    buf = str(maxReward)
    fw.write(buf)
    fw.close()
    #print time.time() - start

if __name__== "__main__":
  main()