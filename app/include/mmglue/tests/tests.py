import mmglue
from google.appengine.ext import ndb
from protorpc import messages


class DummyModel(ndb.Model):
	name = ndb.StringProperty(indexed=False, required=True)
	alias = ndb.StringProperty(repeated=True)

class DummyMessage(messages.Message):
	name = messages.StringField(1)
	alias = messages.StringField(2, repeated=True)


def test_message_from_model():

	model = DummyModel(
		name="Adrian",
		alias=["Bob", "Mac"])

	msg = mmglue.message_from_model(model, DummyMessage)

	assert msg.name == 'Adrian'
	#assert msg.alias == ["Bob", "Mac"]

