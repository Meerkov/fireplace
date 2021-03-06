from ..utils import *


##
# Hero Powers

# Wild Magic
class TBA01_5:
	activate = Buff(Give(CONTROLLER, RandomSpell()), "TBA01_5e")

class TBA01_5e:
	cost = SET(0)


# Molten Rage
class TBA01_6:
	activate = Summon(CONTROLLER, "CS2_118")


##
# Minions

# Dragonkin Hatcher
class BRMC_84:
	play = Summon(CONTROLLER, "BRMA09_2Ht") * 2


# Lucifron
class BRMC_85:
	play = Buff(ALL_MINIONS - SELF, "CS2_063e")


# Atramedes
class BRMC_86:
	events = Play(OPPONENT).on(Buff(SELF, "BRMC_86e"))


# Moira Bronzebeard
class BRMC_87:
	deathrattle = Summon(CONTROLLER, "BRM_028")


# Drakonid Slayer
class BRMC_88:
	events = Attack(SELF).on(CLEAVE)


# Son of the Flame
class BRMC_91:
	play = Hit(TARGET, 6)


# Coren Direbrew
class BRMC_92:
	play = Give(CONTROLLER, "EX1_407")
	tags = {
		enums.ALWAYS_WINS_BRAWLS: True,
	}


# Golemagg
class BRMC_95:
	cost_mod = -Attr(FRIENDLY_HERO, GameTag.DAMAGE)


# High Justice Grimstone
class BRMC_96:
	events = OWN_TURN_BEGIN.on(Summon(CONTROLLER, RandomMinion(rarity=Rarity.LEGENDARY)))


# Razorgore
class BRMC_98:
	events = OWN_TURN_BEGIN.on(Buff(FRIENDLY_MINIONS, "BRMC_98e"))


# Garr
class BRMC_99:
	events = SELF_DAMAGE.on(Summon(CONTROLLER, "BRMC_99e"))


##
# Spells

# Open the Gates
class BRMC_83:
	play = Summon(CONTROLLER, "BRMA09_2Ht") * 7


# Core Hound Puppies
class BRMC_95h:
	play = Summon(CONTROLLER, "BRMC_95he") * 2

class BRMC_95he:
	events = TURN_END.on(Summon(CONTROLLER, Copy(ID("BRMC_95he") + KILLED_THIS_TURN)))


##
# Weapons

# Sulfuras
class BRMC_94:
	deathrattle = Summon(CONTROLLER, "BRM_027p")
