
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
  phase = int(getGlobalVariable("phase"))
  if phase != 0:
    whisper("Cannot start a new Question at this point!")
    return
  q = getGlobalVariable("q")
  if q != "":
    whisper("There's already an active Question!")
    return
  for card in group.top(1):
    card.moveToTable(0,0)
    rnd(1,10)
    notify("{} played {}".format(me, card))
    setGlobalVariable("q", str(card._id))
    setGlobalVariable("phase", "1")

def select(card, x = 0, y = 0):
  mute()
  if me.isActivePlayer:
    whisper("Is it fair for the Card Czar to answer his own question?")
    return
  phase = int(getGlobalVariable("phase"))
  if phase != 1:
    whisper("This is a really inappropriate time to play an answer.")
    return
  if card.highlight != None:
    card.highlight = None
    notify("{} can't make up his mind.".format(me))
  else:
    card.highlight = selectColor
    notify("{} selected a card.".format(me))
  loadedCards = []
  activePlayer = None
  q = Card(int(getGlobalVariable("q")))
  if not q in table:
    notify("ERROR Question not found: {}".format(q))
    return
  for p in players:
    if p.isActivePlayer:
      activePlayer = p
    highlighted = [c for c in p.hand
        if c.highlight == selectColor]
    if len(highlighted) == q.Answers:
      for hc in highlighted:
        n = rnd(0, len(loadedCards))
        loadedCards.insert(n, hc)
    else:
      return
  position = 1
  for lc in loadedCards:
    lc.moveToTable(75*position, 0)
    lc.setController(activePlayer)
    position += 1
  notify("All Answers have been selected.")
  notify("Card Czar, lay upon thee with divine judgement!")

def finalize(card, x = 0, y = 0):
  mute()
  global currentQuestion, phase
  if not me.isActivePlayer:
    whisper("Only the Card Czar may use this!")
    return
  if card.Type == "Q":
    if phase != 1:
      whisper("Cannot finalize choices at this time!")
      return
    if currentQuestion == None or currentQuestion != card:
      whisper("You have to run this on the active Question card ({}).".format(currentQuestion))
      return
    count = card.Answers
    tardyness = ""
    cardpairs = []
    for p in players:
      if not p.isActivePlayer:
        cards = [c._id for c in table if card.owner == p]
        if len(cards) != count:
          tardyness += ", {}".format(p)
        else:
          cardpairs.append(cards)
    if len(tardyness) != "":
      notify("The Card Czar is growing impatient{}.".format(tardyness))
      return
    shuffled = []
    while len(cardpairs) > 0:
      n = rnd(0, len(cardpairs) - 1)
      shuffled.append(cardpairs.pop(n))
    xcount = 0
    for pair in shuffled:
      ycount = 0
      xcount += 75
      for c in pair:
       c.setController(me)
       c.moveToTable(xcount, ycount, False)
       ycount += 100
    notify("The Card Czar is ready to make a decision.")
    phase = 2
  elif card.Type == "A":
    if phase != 2:
      whisper("Cannot choose a favorite Answer at this time!")
      return
    if currentQuestion == None or currentQuestion.group != table:
      whisper("Cannot find the active Question card...?")
      return
    notify("The Card Czar has chosen {}".format(card))
    currentQuestion.moveTo(card.owner.piles['Score Pile'])
    notify("{} gets the Awesome Point.".format(card.owner))
    for c in table:
      c.moveTo(c.owner.Discard)
    currentQuestion = None
    phase = 0
