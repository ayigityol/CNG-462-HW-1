from collections import namedtuple
import Queue
#imports

shortestPath = {}
found = 0 # A* STOPPER
result = 0 # BFS STOPPER
ucsResult = [] #STATS
bfsResult = [] #STATS
#global varibales

# node structs strat
class nodeAstar(object):
    def __init__(self):
        self.inner = None
        self.nextprio = {"L": {}, "R": {}, "U": {}, "D": {}}
        self.prio = None
        return

class nodeUniform(object):
    def __init__(self, inner, children, path, cost):
        self.inner = inner
        self.children = children
        self.path = path
        self.cost = cost
    def __cmp__(self, other):
        return cmp(self.cost, other.cost)

class functionObject(object):
    def __init__(self, priorty,  position, cost):
        self.priorty = priorty
        #self.args = args
        self.position = position
        self.cost = cost
        return

    def __cmp__(self, other):
        return cmp(self.priorty, other.priorty)
# node structs end

#queue element struct
def searchDic(dic, val):
    try:
        return dic[val]
    except:
        return -1
#handy function 1, search with controller in a hash table


def tupleaddition(tuple1, tuple2):
    return (tuple1[0] + tuple2[0], tuple1[1] + tuple2[1])
#handy function 2, add two tuple -> used in graph movements

#bussines logic functions start
def heuristic(coor1, coor2):
    return abs(coor1[0] - coor2[0]) + abs(coor1[1] - coor2[1])

def Astar(statepos, tsmmap, pos, cost, queue, searchfor):
    global found
    if found != 0:
        return
    if searchDic(tsmmap, pos) != -1:
        node = nodeAstar()
        node.inner = tsmmap[pos]
        if searchfor == node.inner:
            found = cost
            return
        else:
            node.prio = heuristic(pos, statepos[searchfor]) + cost
            node.nextprio["L"] = heuristic(tupleaddition(pos, (-1, 0)), statepos[searchfor]) + cost
            node.nextprio["R"] = heuristic(tupleaddition(pos, (1, 0)), statepos[searchfor]) + cost
            node.nextprio["U"] = heuristic(tupleaddition(pos, (0, -1)), statepos[searchfor]) + cost
            node.nextprio["D"] = heuristic(tupleaddition(pos, (0, 1)), statepos[searchfor]) + cost
            queue.put(functionObject(node.nextprio["L"], tupleaddition(pos, (-1, 0)),  cost + 1))
            queue.put(functionObject(node.nextprio["R"], tupleaddition(pos, (1, 0)),  cost + 1))
            queue.put(functionObject(node.nextprio["U"], tupleaddition(pos, (0, -1)),  cost + 1))
            queue.put(functionObject(node.nextprio["D"], tupleaddition(pos, (0, 1)),  cost + 1))
            nextState = queue.get()
            while found == 0:
                Astar(statepos, tsmmap, nextState.position, nextState.cost, queue, searchfor)
                nextState = queue.get()

def makeTree(states, current,  parent, path, cost): # make search tree for BFS
    node = nodeUniform(current,[],path,cost)
    temppath = path
    for child in states.replace(current,""):
        temppath = temppath + node.inner + "-"
        node.children.insert(len(node.children), makeTree(states.replace(current,""), child, node.inner, temppath, cost + shortestPath[current+"-"+child]))
        temppath = path

    return node

def bfs(tree):
    global bfsResult
    node = tree
    for child in node.children:
        if len(child.children) == 0:
            bfsResult = [child.path + child.inner + "-" + "A",child.cost + shortestPath[child.inner+"-"+"A"] ]
            print "Algorithm Used BFS"
            print child.path + child.inner + "-" + "A"
            print "Total Tour Cost = " + str(child.cost + shortestPath[child.inner+"-"+"A"])
            return -1
    for child in node.children:
        result = bfs(child)
        if result == -1:
            return -1

def ucs(tree):
    global result
    global ucsResult
    node = tree

    if len(node.children)==0:
        result = 1
        ucsResult = [node.path + node.inner + "-" + "A", node.cost + shortestPath[node.inner+"-"+"A"]]
        print "Algorithm used UCS"
        print node.path + node.inner + "-" + "A"
        print "Total Tour Cost = " + str(node.cost + shortestPath[node.inner+"-"+"A"])
        return
    for child in node.children:
        queue.put(child)
    while result== 0:
        ucs(queue.get())

def statistics():
    print "        NODES         COST"
    print "BFS " + bfsResult[0] + "         " + str(bfsResult[1])
    print "UCS " + ucsResult[0] + "         " + str(ucsResult[1])
#bussines logic functions end


## MAIN
stringmap = open("input.txt","r")
string =  stringmap.read()

x = 0
y = 0
tsmmap = {} # MAP OF THE TSM PROBLEM ON COORDINATES
statepos = {} # STATE POSITIONS ON COORDINATES

states = string.replace("*", "").replace(" ", "").replace("\n", "")
states = "".join(sorted(states))

line = string.find("\n")
string.replace("\n", "")

for ch in string: # FILLING DICTIONARIES
    if x > line:
        y += 1
        x = 0
    if ch in states:
        statepos[ch] = (x, y)
    if ch != "*" and ch != "\n":
        tsmmap[(x, y)] = ch
    x += 1
rest = states
for start in rest: ## FILLING DICTIONARY OF SHORTEST PATHS USING A*
    rest = rest.replace(start,"")
    for goal in rest:
        queue = Queue.PriorityQueue()
        Astar(statepos, tsmmap, statepos[start], 0, queue, goal)
        print start + "-" + goal + ":" +  str(found)
        shortestPath[start+"-"+goal] = found
        shortestPath[goal+"-"+start] = found
        found = 0

##uninform search
rest = states
root = makeTree(rest,"A","","",0)
bfs(root)
queue = Queue.PriorityQueue()
ucs(root)
statistics()