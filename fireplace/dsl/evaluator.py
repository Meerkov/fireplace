import copy
from ..utils import fireplace_logger as logger


class Evaluator:
	"""
	Lazily evaluate a condition at runtime.

	Evaluators must implement the check() method, which determines whether they
	evaluate to True in the current state.
	"""
	def __init__(self):
		self._if = None
		self._else = None

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.selector)

	def __and__(self, action):
		ret = copy.copy(self)
		ret._if = action
		return ret

	def __or__(self, action):
		ret = copy.copy(self)
		ret._else = action
		return ret

	def evaluate(self, source):
		"""
		Evaluates the board state from `source` and returns an iterable of
		Actions as a result.
		"""
		ret = self.check(source)
		if ret:
			if self._if:
				return self._if
		elif self._else:
			return self._else

	def trigger(self, source):
		"""
		Triggers all actions meant to trigger on the board state from `source`.
		"""
		actions = self.evaluate(source)
		if actions:
			source.game.trigger_actions(source, actions)


class CurrentPlayer(Evaluator):
	"""
	Evaluates to True if the selector is the current player.
	Selector must evaluate to only one player.
	"""
	def __init__(self, selector):
		super().__init__()
		self.selector = selector

	def check(self, source):
		for target in self.selector.eval(source.game, source):
			if not target.controller.current_player:
				return False
		return True


class Dead(Evaluator):
	"""
	Evaluates to True if every target in \a selector is dead
	"""
	def __init__(self, selector):
		super().__init__()
		self.selector = selector

	def check(self, source):
		for target in self.selector.eval(source.game, source):
			if not target.dead:
				return False
		return True


class Find(Evaluator):
	"""
	Evaluates to True if \a selector has a match.
	"""
	def __init__(self, selector, count=1):
		super().__init__()
		self.selector = selector

	def check(self, source):
		return bool(len(self.selector.eval(source.game, source)))


class Joust(Evaluator):
	"""
	Compare the sum of the costs of \a selector1 versus \a selector2.
	Evaluates to True if the mana cost of \a selector1 is higher.
	"""
	def __init__(self, selector1, selector2):
		super().__init__()
		self.selector1 = selector1
		self.selector2 = selector2

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.selector1, self.selector2)

	def check(self, source):
		t1 = self.selector1.eval(source.game, source)
		t2 = self.selector2.eval(source.game, source)
		if not t1:
			return False
		elif not t2:
			return True
		diff = sum(t.cost for t in t1) - sum(t.cost for t in t2)
		logger.info("Jousting %r vs %r -> %i difference", t1, t2, diff)
		return diff > 0
