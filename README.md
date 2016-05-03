# niki_project

Run setup.sh

Add users:
    
echo 'Now please go to localhost:5280/admin and add 2 users'
echo 'foo@localhost with password: foo'
echo 'bar@localhost with password: bar'

Run simple_chat.py to check the duplicate filter.

python simple_chat.py bar@localhost

Now login using bar@localhost with some IM client (Pidgin, empathy?) to check the messages it recieves.
