
import re

def draw(group, x = 0, y = 0):
	mute()
	if len(me.Answers) == 0:
		if len(shared.Answers) == 0: return
		shared.Answers[0].moveTo(me.hand)
		notify("{} drew 1 Answer. (shared)".format(me))
	else:
		me.Answers[0].moveTo(me.hand)
		notify("{} drew 1 Answer.".format(me))

def drawfill(group, x = 0, y = 0):
	mute()
	count = 10 - len(me.hand)
	if len(me.Answers) < count:
		if len(shared.Answers) < count: return
		for card in shared.Answers.top(count): card.moveTo(me.hand)
		notify("{} drew to 10 (+{}) Answers. (shared)".format(me, count))
	else:
		for card in me.Answers.top(count): card.moveTo(me.hand)
		notify("{} drew to 10 (+{}) Answers. (shared)".format(me, count))

def discard(card, x = 0, y = 0):
	mute()
	owner = card.owner
	card.isFaceUp = True
	rnd(10,100)
	card.moveTo(owner.Discard)
	if owner == shared:
		notify("{} confesses ignorance for not understanding {} (shared)".format(me, card))
	else:
		notify("{} confesses ignorance for not understanding {}".format(me, card))

def shuffle(group, x = 0, y = 0):
	mute()
	group.shuffle()
	notify("{} shuffled {}'s {}.".format(me, group.player.name, group.name))
	
def lookup(card, x = 0, y = 0):
	mute()
	openUrl("https://www.google.com/search?btnG=1&pws=0&q={}".format(card.name))
	notify("{} doesn't understand {}".format(me, card))
	
def random(group, x = 0, y = 0):
	mute()
	playercount = len(players) - 1
	n = rnd(0, playercount)
	notify("{} randomly selected {}.".format(me, players[n].name))

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
	for card in qgroup.top(1):
		card.moveToTable(0,0)
		rnd(1,10)
		notify("{}'s new question: {}".format(me, card))
		currentQuestion = card

def select(card, x = 0, y = 0):
	mute()
	if me.isActivePlayer:
		whisper("Is it fair for the Card Czar to answer his own question?")
		return
	if card.highlight != None:
		card.highlight = None
		notify("{} can't make up his mind.".format(me))
	else:
		card.highlight = selectColor
		notify("{} selected a card.".format(me))
		
def finalize(card, x = 0, y = 0):
	mute()
	global currentQuestion
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
		xcount = 0
		for answerList in loadedCards:
			ycount = 0
			xcount += 75
			for c in answerList:
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
		currentQuestion.moveTo(card.owner.piles['Score Pile'])
		notify("{} gets the Awesome Point.".format(card.owner))
		for c in table:
			c.moveTo(c.owner.Discard)
		currentQuestion = None
		