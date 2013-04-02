
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
  
def playq(group, x = 0, y = 0):
  mute()
  for card in group.top(1):
    card.moveToTable(0,0)
    notify("{} played {}".format(me, card))

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

def select(card, x = 0, y = 0):
  mute()
  card.highlight = selectColor
  loadedCards = []
  activePlayer = None
  notify("{} selected a card.".format(me))
  for p in players:
    if p.isActivePlayer:
      activePlayer = p
    highlighted = [c for c in p.hand
        if c.highlight == selectColor]
    if len(highlighted) == 0:
      return
    if len(highlighted) == 1:
      for hc in highlighted:
        n = rnd(0, len(loadedCards))
        loadedCards.insert(n, hc)
  position = 1
  for lc in loadedCards:
    lc.moveToTable(75*position, 0)
    lc.setController(activePlayer)
    position += 1
  notify("All Answers have been selected.")
  notify("Card Czar, please choose your favorite!")

def declare(card, x = 0, y = 0):
  mute()
  notify("The Card Czar has chosen {}".format(card))
  card.moveTo(card.owner.piles['Score Pile'])
  notify("{} gets the point.".format(card.owner)) 