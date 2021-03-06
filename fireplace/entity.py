import uuid
from .utils import fireplace_logger


class BaseEntity(object):
	base_events = []
	logger = fireplace_logger
	ignore_scripts = False

	def __init__(self):
		self.manager = self.Manager(self)
		self.play_counter = 0
		self.tags = self.manager
		self.uuid = uuid.uuid4()

		scripts = getattr(self.data, "scripts", None)
		events = getattr(scripts, "events", [])
		if not isinstance(events, list):
			self._events = [events]
		else:
			self._events = events[:]

	def __int__(self):
		return self.entity_id

	@property
	def events(self):
		return self.base_events + self._events

	@property
	def update_scripts(self):
		ret = []
		if self.data and not self.ignore_scripts:
			scripts = getattr(self.data.scripts, "update", ())
			if not hasattr(scripts, "__iter__"):
				ret.append(scripts)
			else:
				for s in scripts:
					ret.append(s)
		return ret

	def log(self, message, *args):
		self.logger.info(message, *args)

	def get_actions(self, name):
		actions = getattr(self.data.scripts, name, None)
		if callable(actions):
			actions = actions(self)
		if actions and not hasattr(actions, "__iter__"):
			actions = (actions, )
		return actions

	def trigger_event(self, source, event, args):
		"""
		Trigger an event on the Entity
		* \a source: The source of the event
		* \a event: The event being triggered
		* \a args: A list of arguments to pass to the callback
		"""
		actions = []
		for action in event.actions:
			if callable(action):
				ac = action(self, *args)
				if not ac:
					# Handle falsy returns
					continue
				if not hasattr(ac, "__iter__"):
					actions.append(ac)
				else:
					actions += action(self, *args)
			else:
				actions.append(action)
		# XXX This is racey. Replace with something more solid.
		self.event_args = args
		source.game.queue_actions(self, actions)
		self.event_args = None
		if event.once:
			self._events.remove(event)


class BuffableEntity(BaseEntity):
	def __init__(self):
		super().__init__()
		self.buffs = []
		self.slots = []

	def _getattr(self, attr, i):
		i += getattr(self, "_" + attr, 0)
		for buff in self.buffs:
			i = buff._getattr(attr, i)
		for slot in self.slots:
			i = slot._getattr(attr, i)
		if self.ignore_scripts:
			return i
		return getattr(self.data.scripts, attr, lambda s, x: x)(self, i)

	def clear_buffs(self):
		if self.buffs:
			self.log("Clearing buffs from %r", self)
			for buff in self.buffs:
				buff.destroy()


class Entity(BuffableEntity):
	pass


def slot_property(attr, f=any):
	@property
	def func(self):
		return f(getattr(slot, attr, False) for slot in self.slots)
	return func


def boolean_property(attr):
	@property
	def func(self):
		return (
			getattr(self, "_" + attr, False) or
			any(getattr(buff, attr, False) for buff in self.buffs) or
			any(getattr(slot, attr, False) for slot in self.slots) or
			getattr(self.data.scripts, attr, lambda s, x: x)(self, False)
		)

	@func.setter
	def func(self, value):
		setattr(self, "_" + attr, value)

	return func


def int_property(attr):
	@property
	def func(self):
		ret = self._getattr(attr, 0)
		return max(0, ret)

	@func.setter
	def func(self, value):
		setattr(self, "_" + attr, value)

	return func
