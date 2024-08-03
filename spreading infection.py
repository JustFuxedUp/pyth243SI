import random
import copy
import re

# Constants
REELHEIGHT = 3
REELS = 5
RUNCOUNT = 10
RARENUM = 4
EPICNUM = 1
UNIQUENUM = 1 
LEGENDNUM = 1
MYSTICNUM = 1
RARETHRES = 50
EPICTHRES = 65
UNIQUETHRES = 80
LEGENDTHRES = 85
MYSTICTHRES = 90
SCATTERTHRES = 95
VERBOSE = True
STREAMLINE = False

# Payouts for each symbol type
payouts = {
    "R": [0.05, 0.10, 0.50],    # Rare
    "E": [0.20, 0.40, 1.00],    # Epic
    "U": [0.20, 0.40, 1.00],    # Unique
    "L": [0.40, 0.80, 2.50],    # Legend
    "M": [1.00, 2.00, 5.00],    # Mystic
    "W": [0.00, 0.00, 10.00]     # Wild
}

# Create reels
reel1 = []
reel2 = []
reel3 = []
reel4 = []
reel5 = []


##reel1 = ['WW', 'WW', 'WW']
##reel2 = ['WW', 'WW', 'WW']
##reel3 = ['WW', 'WW', 'R1']
##reel4 = ['R3', 'WW', 'WW']
##reel5 = ['WW', 'WW', 'WW']

slots = [reel1, reel2, reel3, reel4, reel5]

# Generate symbols
rares = [f"R{x}" for x in range(RARENUM)]
epics = [f"E{x}" for x in range(EPICNUM)]
uniques = [f"U{x}" for x in range(UNIQUENUM)]
legends = [f"L{x}" for x in range(LEGENDNUM)]
mystics = [f"M{x}" for x in range(MYSTICNUM)]

# Initialize game variables
random.seed()
total_winnings = 0



def reelcheck(symbol, reel):
    connect = False
    for cursymbol in range(REELHEIGHT):
        if string_compare(symbol, slots[reel][cursymbol]):
            connect = True
    return connect

def strset_has(_str, _set):
    connect = False
    for x in _set:
        if string_has(_str, x):
            connect = True
    return connect

def string_has(str1, str2):
    if str1 in str2:
        return True
    else:
        return False


def strset_compare(_str, _set, strict = False):
    connect = False
    for x in _set:
        if string_compare(_str, x, strict):
            connect = True
    return connect

def string_compare(str1, str2, strict = False):
    if re.fullmatch(str.lower(str1), str.lower(str2)):
        return True
    elif 'W' in str1 or 'W' in str2:
        if strict:
            return False
        else:
            return True
    else:
        return False

def spreadcheck(reel, symbol):
    if string_has('S', slots[reel][symbol]):
                if reel != 0:
                    spreadingwild(reel-1,symbol)
                if reel != REELS-1:
                    spreadingwild(reel+1,symbol)
                if symbol != 0:
                    spreadingwild(reel,symbol-1)
                if symbol != REELHEIGHT-1:
                    spreadingwild(reel,symbol+1)

def spreadingwild(reel, symbol):
    if not string_has('W',slots[reel][symbol]):
        if not string_has('S',slots[reel][symbol]):
            if not string_has('R',slots[reel][symbol]):
                if not slots[reel][symbol].islower():
                    tempsymbol = list(copy.copy(slots[reel][symbol]))
                    tempsymbol[1] = 'S'
                    slots[reel][symbol] = str(f"{tempsymbol[0]}{tempsymbol[1]}")
                    spreadcheck(reel, symbol)
    

def spin(total, bonus = False, amount = 0):
        # Reset reels
        for reel in slots:
            reel.clear()
        
        # Populate reels
        for reel in slots:
            for _ in range(REELHEIGHT):
                pull = random.randint(1, 100)
                chance = random.randint(1,10)
                if pull <= RARETHRES:
                    rare = copy.copy(random.choice(rares))
                    reel.append(rare)
                elif pull <= EPICTHRES:
                    epic = copy.copy(random.choice(epics))
                    if chance <= 5:
                        epic = str.lower(epic)
                    reel.append(epic)
                elif pull <= LEGENDTHRES:
                    legend = copy.copy(random.choice(legends))
                    if chance <= 5:
                        legend = str.lower(legend)
                    reel.append(legend)
                elif pull <= MYSTICTHRES:
                    mystic = copy.copy(random.choice(mystics))
                    if chance <= 5:
                        mystic = str.lower(mystic)
                    reel.append(mystic)
##                elif pull <= SCATTERTHRES:
##                    reel.append("PP")
                else:
                    chance = random.randint(1,10)
                    if chance == 1:
                        reel.append("WS")
                    else:
                        reel.append("WW")
    ##    if VERBOSE:
    ##        for reel in slots:
    ##            print(f"reel{reel}")

        #Spreading wild check

        spreadhappening = False
        
        for curreel in range(REELS):
            for cursymbol in range(REELHEIGHT):
                if string_compare(slots[curreel][cursymbol], "WS", True):
                    spreadcheck(curreel,cursymbol)
                    spreadhappening = True

        for curreel in range(REELS):
            for cursymbol in range(REELHEIGHT):
                if string_has('S', slots[curreel][cursymbol]) and not string_compare(slots[curreel][cursymbol], "WS", True):
                    tempsymbol = list(copy.copy(slots[curreel][cursymbol]))
                    tempsymbol[1] = 'W'
                    slots[curreel][cursymbol] = str(f"{tempsymbol[0]}{tempsymbol[1]}")
                   
        if VERBOSE:
            for reel in slots:
                print(f"reel{reel}")

                    
            

    
    






            
        # Determine winning combinations and calculate payout
        round_winnings = 0
        freespins = 0

        #First, we read the first reel for the symbols we want connecting
        consecutive_symbols = set()
        minreel = 0
        #If you had no wilds you'd only check the first 3 reels, but since we have wilds, we could have wilds up to the 4th
        #reel, and then random symbols. These must be accounted for
        for curreel in range(REELS):
            cur_symbols = []
            wildextend = False
            #Hence, here
            if curreel == minreel:
                for cursymbol in range(REELHEIGHT):
                    symbol = slots[curreel][cursymbol]
                    if 'W' in symbol: #If there's a wild, it will allow all connections to the next reel, so add to the set.
                        if VERBOSE and not wildextend:
                            print("Wild extend!")
                        wildextend = True
                    consecutive_symbols.add(symbol)

            #If it's reel 2 or 3, we then compare and modify the list we made to hold what we've found continuing,
            #then make the consecutive symbols hold the new current symbols
            if curreel == 1 or curreel == 2:
                for connecting in consecutive_symbols:
                    purewild = False
                    if 'W' in connecting:
                        purewild = True
                    if strset_compare(connecting, slots[curreel], purewild):
                        cur_symbols.append(connecting)
                consecutive_symbols = set(cur_symbols)
            if VERBOSE:
                print(f"{consecutive_symbols}")
            if len(consecutive_symbols) == 0:
                break
            if wildextend: minreel += 1

        #Good debug to see what the computer sees
        if VERBOSE:
            print("winning symbols:" , ''.join(consecutive_symbols))

    ##Now we need to pay out.
    ##It is important that it was a set, and not a list, since with a list we can have multiple of the same symbol.
    ##Therefore, we want a highlander rule. Every unique symbol only needs evaluation once. It's also important
    ##to go by symbol like this, since multiple symbols can pay at different lines, in different way count. Even
    ##more so with wilds

        wildpay = 0
        
        if strset_has('W', consecutive_symbols):
            symbol = 'W'
            paylength = 0
            payways = 1
            mult = 0
            connecting = True
            purewild = False
            while connecting:
                for curreel in range(REELS):
                    if strset_has(symbol, slots[curreel]) and connecting == True:
                        paylength += 1
                        for cursymbol in range(REELHEIGHT):
                            if string_has(symbol, slots[curreel][cursymbol]):
                                mult += 1
                        payways = payways * mult
                        mult = 0
                    else:
                        connecting = False
                    if curreel == REELS - 1:
                        connecting = False
            if paylength == 5:
                if VERBOSE:
                    print(f"ways: {payways}")
                    print(f"length: {paylength}")
                payout = payouts[symbol[0]][paylength - 3] * payways
                if not STREAMLINE:
                    print(symbol + f" has paid out ${payout:.2f}")
                round_winnings += payout
                wildpay += payways
        nonwildlines = copy.copy(consecutive_symbols)
        for symbol in consecutive_symbols:
            if 'W' in symbol:
                nonwildlines.remove(symbol)
        consecutive_symbols = nonwildlines
            
            
        for symbol in consecutive_symbols:
            paylength = 0 #How far did the connection go?
            payways = 1 #How many ways are there?
            mult = 0
            connecting = True
            #While statement to kill the loop. No need to check further if we stopped connecting
            while connecting:
                for curreel in range(REELS):
                    if strset_compare(symbol, slots[curreel]) and connecting == True:
                        paylength += 1
                        for cursymbol in range(REELHEIGHT):
                            if string_compare(symbol, slots[curreel][cursymbol]):
                                mult += 1
                        payways = payways * mult
                        mult = 0
                    else:
                        connecting = False
                    if curreel == REELS - 1: #Should failsafe and always close off if full connection
                        connecting = False
            if VERBOSE:
                print(f"ways: {payways - wildpay}")
                print(f"length: {paylength}")
            payout = payouts[str.upper(symbol[0])][paylength - 3] * (payways - wildpay)
            if not STREAMLINE:
                print(symbol + f" has paid out ${payout:.2f}")
            round_winnings += payout

        if not bonus:    
            total += round_winnings
            total_winnings = total
            if not STREAMLINE:
                print(f"Spin {run + 1}: Winnings: ${round_winnings:.2f}")
        elif freespins != 0:
            spin(total, True, freespins)
        else:
            if amount > 0:
                spin(total, True, amount - 1)


# Run the simulation
print("Luck is arriving!")
print(f"If {RUNCOUNT} spins happened...")
for run in range(RUNCOUNT):
    # can't win if you don't play
    total_winnings -= 1
    spin(total_winnings)
        

print(f"Total Winnings: ${total_winnings:.2f}")



                
##    #print("Total dupes: " + str(dupe))
##    #print("Total money spent: " + str(money))
##    total += money
##    dupetotal += dupe
##    if mindupe == 69 or  mindupe > dupe:
##        mindupe = dupe
##    if maxdupe == 69 or  maxdupe < dupe:
##        maxdupe = dupe
##    if mintotal == 69 or  mintotal > money:
##        mintotal = money
##    if maxtotal == 69 or  maxtotal < money:
##        maxtotal = money
##        
##        
##    money = 0
##    dupe = 0
##    collection.clear()
##    run += 1
##print("avg money spent: " + str(total/run))
##print("min money spent: " + str(maxtotal))
##print("max money spent: " + str(mintotal))
##print("avg dupes : " + str(dupetotal/run))
##print("min dupes : " + str(mindupe))
##print("max dupes : " + str(maxdupe))



