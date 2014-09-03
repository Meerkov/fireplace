import random
from fireplace.targeting import *
from ..card import Card


# helpers
drawCard = lambda self: self.owner.draw()


def discard(count):
	def _discard(self):
		# discard at most x card
		discard = random.sample(self.owner.hand, min(count, len(self.owner.hand)))
		for card in discard:
			card.discard()
	return _discard


def healTarget(amount):
	def _healTarget(self, target):
		target.heal(amount)
	return _healTarget


# Healing Totem
class NEW1_009(Card):
	def endTurn(self):
		targets = self.getTargets(TARGET_FRIENDLY_MINIONS)
		for target in targets:
			if self.game.currentPlayer is self.owner:
				target.heal(1)

# Bloodsail Corsair
class NEW1_025(Card):
	def activate(self):
		weapon = self.owner.opponent.hero.weapon
		if self.owner.opponent.hero.weapon:
			weapon.loseDurability(1)


# Voodoo Doctor
class EX1_011(Card):
	targeting = TARGET_ANY_CHARACTER
	activate = healTarget(2)

# Novice Engineer
class EX1_015(Card):
	activate = drawCard

# Acidic Swamp Ooze
class EX1_066(Card):
	def activate(self):
		if self.owner.opponent.hero.weapon:
			self.owner.opponent.hero.weapon.destroy()

# Loot Hoarder
class EX1_096(Card):
	deathrattle = drawCard

# Succubus
class EX1_306(Card):
	activate = discard(1)

# Murloc Tidehunter
class EX1_506(Card):
	def activate(self):
		self.owner.summon("EX1_506a")

# Harrison Jones
class EX1_558(Card):
	def activate(self):
		weapon = self.owner.opponent.hero.weapon
		if weapon:
			weapon.destroy()
			self.owner.draw(weapon.durability)

# Priestess of Elune
class EX1_583(Card):
	targeting = TARGET_FRIENDLY_HERO
	activate = healTarget(4)

# Nightblade
class EX1_593(Card):
	targeting = TARGET_ENEMY_HERO
	def activate(self, target):
		target.damage(3)

# Dalaran Mage
class EX1_582(Card):
	spelldamage = 1

# Guardian of Kings
class CS2_088(Card):
	targeting = TARGET_FRIENDLY_HERO
	activate = healTarget(6)

# Earthen Ring Farseer
class CS2_117(Card):
	targeting = TARGET_ANY_CHARACTER
	activate = healTarget(3)

# Raid Leader
class CS2_122(Card):
	aura = "CS2_122e"

# Kobold Geomancer
class CS2_142(Card):
	spellpower = 1

# Gnomish Inventor
class CS2_147(Card):
	activate = drawCard

# Archmage
class CS2_155(Card):
	spelldamage = 1

# Elven Archer
class CS2_189(Card):
	targeting = TARGET_ANY_CHARACTER
	def activate(self, target):
		target.damage(1)

# Ogre Magi
class CS2_197(Card):
	spellpower = 1