try:
	from . import models
	from . import forms
	from . import middleware
	from . import widgets
	from . import context_processors
except ImportError:
	import models
	import forms
	import middleware
	import widgets
	import context_processors