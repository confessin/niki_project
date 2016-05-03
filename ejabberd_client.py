from pyejabberd import EjabberdAPIClient

# Create a client and authenticate with elevated user 'bob@example.com'
client = EjabberdAPIClient(host='localhost', port=5222, username='foo', password='foo', user_domain='localhost',
                                   protocol='http')

client = EjabberdAPIClient(host='localhost', port=5222, username='foo', password='foo', user_domain='example.com',
                           protocol='http')


# Test the connection by sending an echo request to the server
sentence = 'some random data'
result = client.echo(sentence)
assert result == sentence

# Get a list of users that are on the server
registered_users = client.registered_users('localhost')
# result is in the format [{'username': 'bob', ...}]

# Register a new user
client.register(user='alice', host='example.com', password='@l1cepwd')

# Change a password
client.change_password(user='alice', host='example.com', newpass='newpwd')

# Verify password
assert client.check_password_hash(user='bob', host='example.com', password='newpwd') is True

# Set nickname
client.set_nickname(user='bob', host='example.com', nickname='Bob the builder')

# Get Bob's contacts
client.get_roster(user='bob', host='example.com')

# Add Alice to Bob's contact group Friends
client.add_rosteritem(localuser='bob', localserver='example.com', user='alice', server='example.com', nick='Alice from Wonderland', group='Friends', subs='both')

# Delete Alice from Bob's contacts
client.delete_rosteritem(localuser='bob', localserver='example.com', user='alice', server='example.com')

# Get list of *all* connected users
client.connected_users()

# Get list of *all* connected users and information about their sessions
client.connected_users_info()

# Get number of connected users
client.connected_users_number()

# Get information for all sessions for a user
client.user_sessions_info(user="jim", host="example.com")

# Get muc rooms
muc_online_rooms = client.muc_online_rooms()
# result is in the format ['room1@conference', ...] where 'conference' is the muc service name

# Create a muc room
client.create_room(name='room1', service='conference', host='example.com')

# Get room options
room_options = client.get_room_options(name='room1', service='conference')

# Set room option
from pyejabberd.muc.enums import MUCRoomOption
client.change_room_option(name='room1', service='conference', option=MUCRoomOption.public, value=False)
client.change_room_option(name='room1', service='conference', option=MUCRoomOption.members_only, value=True)

# Set room affiliation
from pyejabberd.muc.enums import Affiliation
client.set_room_affiliation(name='room1', service='conference', jid='alice@example.com', affiliation=Affiliation.member)

# Get room affiliations
affiliations = client.get_room_affiliations(name='room1', service='conference')

# Destroy a muc room
client.destroy_room(name='room1', service='conference', host='example.com')

# Unregister a user
client.unregister(user='alice', host='example.com')

