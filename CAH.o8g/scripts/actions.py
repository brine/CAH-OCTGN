
import re

#---------------
# Events
#---------------

def shuffleDeck(player, groups):
    mute()
    if player == me:
        for group in groups:
            pile = Pile(group._id, group.name, group.player)
            pile.shuffle()
            if pile.player == me:
                notify("{} shuffles their {}.".format(me, pile.name))
            else:
                notify("{} shuffles the shared {}.".format(me, pile.name))

##The CAH game def allows players to create their own personal decks, as well as global/shared decks.
##All draw-based functions will draw from the personal deck before it draws from the global deck.

def genericDraw(type):
    mute()
    if len(me.piles[type]) == 0:
        if len(shared.piles[type]) == 0:
            return
        shared.piles[type][0].moveTo(me.hand)
        return True
    me.piles[type][0].moveTo(me.hand)
    return False

def draw(group, x = 0, y = 0):
    mute()
    shared = genericDraw('Answers')
    if shared != None:
        notify("{} drew 1 Answer.{}".format(me, ' (shared)' if shared == True else ''))

def drawfill(group, x = 0, y = 0):
    mute()
    loopCount = 10 - len(me.hand)
    drawCount = 0
    for x in range(0, loopCount):
        shared = genericDraw('Answers')
        if shared != None:
            drawCount += 1
    notify("{} drew to {} (+{}) Answers.{}".format(me, len(me.hand), drawCount, ' (shared)' if shared == True else ''))

def discard(card, x = 0, y = 0):
    mute()
    owner = card.owner
    card.isFaceUp = True
    rnd(10,100)
    card.moveTo(owner.Discard)
    notify("{} confesses ignorance for not understanding {}.{}".format(me, card, ' (shared)' if owner == shared else ''))

def lookup(card, x = 0, y = 0):
    mute()
    openUrl("https://www.google.com/search?btnG=1&pws=0&q={}".format(card.name))
    notify("{} doesn't understand {}".format(me, card))

def random(group, x = 0, y = 0):
    mute()
    playercount = len(players) - 1
    n = rnd(0, playercount)
    notify("{} randomly selected {}.".format(me, players[n].name))

def rando(group, x = 0, y = 0):
    mute()
    randoStatus = getGlobalVariable("rando")
    if randoStatus == "False":
        notify("{} invites Rando Cardrissian to the party.".format(me))
        setGlobalVariable("rando", "True")
    else:
        notify("{} does not want Rando Cardrissian to play.".format(me))
        setGlobalVariable("rando", "False")

selectColor = '#f8359a'

currentQuestion = None

def playq(group, x = 0, y = 0):
    mute()
    if not me.isActivePlayer:
        whisper("Only the Card Czar can play a new question.")
        return
    global currentQuestion
    qs = (c for c in table if c.Type == "Q")
    for q in qs:
        whisper("Cannot play a new question: There's already one in play.")
        return
    if len(me.Questions) == 0:
        if len(shared.Questions) == 0:
            whisper("There are no more Questions in the deck!")
            return
        qgroup = shared.Questions
    else:
        qgroup = me.Questions
    card = qgroup[0]
    card.moveToTable(0,0)
    if card.controller != me:
        card.setController(me) ## apparently global decks retain the original person who loaded the deck as controller
    rnd(1,10)
    notify("{}'s new question: {}".format(me, card))
    currentQuestion = card
    for c in me.hand:
        c.highlight = None

def select(card, x = 0, y = 0):
    mute()
    if me.isActivePlayer:
        whisper("Is it fair for the Card Czar to answer their own question?")
        return
    if card.highlight != None:
        card.highlight = None
        notify("{} can't make up their mind.".format(me))
    else:
        card.highlight = selectColor
        notify("{} selected a card.".format(me))

owners = {}
annoyingReminder = True

def finalize(card, x = 0, y = 0):
    mute()
    global currentQuestion, owners, annoyingReminder
    if not me.isActivePlayer:
        whisper("Only the Card Czar may use this!")
        return
    if card.Type == "Q":
        if currentQuestion == None:
            loludumb = confirm("You're not supposed to drag these onto the table, but I'm a nice guy so I'll let it slide this time.")
            currentQuestion = card
        if currentQuestion != card:
            whisper("That's not the current question, what manner of witchcraft is this?")
            return
        loadedCards = []
        tardyness = ''
        for p in players:
            if p != me:
                chosencards = [c for c in p.hand if c.highlight == selectColor]
                if len(chosencards) > int(card.Answers):
                    notify("{} has selected too many cards.".format(p))
                    return
                elif len(chosencards) == int(card.Answers):
                    hclist = []
                    for hc in chosencards:
                        hclist.append(hc)
                    n = rnd(0, len(loadedCards))
                    loadedCards.insert(n, hclist)
                else:
                    tardyness += ", {}".format(p)
        if tardyness != "":
            notify("The Card Czar is growing impatient{}.".format(tardyness))
            return
        if table.isTwoSided() and annoyingReminder:
            notify("This game works better when 'Use Two-Sided Table' is turned off.  Next time, don't forget to uncheck it!")
            annoyingReminder = False
## If all players are ready, start processing
        ## Load Rando's cards
        randoCheck = getGlobalVariable("rando")
        if randoCheck == "True":
            hclist = []
            for loop in range(0, int(card.Answers)):
                hclist.append("rando")
            n = rnd(0, len(loadedCards))
            loadedCards.insert(n, hclist)
        ## Start dumping all the loaded cards onto the table
        xcount = 0
        for answerList in loadedCards:
            ycount = 0
            xcount += 75
            for c in answerList:
                if str(c) == "rando":
                    if len(shared.Answers) == 0: break
                    c = shared.Answers[0]
                    owners[c] = "rando"
                else:
                    owners[c] = c.controller
                c.moveToTable(xcount, ycount, False)
                c.setController(me)
                ycount += 100
        notify("Card Czar, lay upon us your divine judgement!")
        currentQuestion = card
    elif card.Type == "A":
        if currentQuestion == None or currentQuestion.group != table:
            whisper("Cannot find the active Question card...?")
            return
        notify("The Card Czar has chosen {}".format(card))
        if str(owners[card]) == "rando":
            currentQuestion.moveTo(shared.piles['Score Pile'])
            notify("Rando gets the Awesome Point ({} points).".format(len(shared.piles['Score Pile'])))
        else:
            currentQuestion.moveTo(owners[card].piles['Score Pile'])
            notify("{} gets the Awesome Point.".format(owners[card]))
        for c in table:
            c.moveTo(c.owner.Discard)
        currentQuestion = None
        owners = {}