

# Pip requirements
sudo pip install cachetools


# Install ejabberd
sudo apt-get -y install ejabberd
# Add a admin user
ejabberdctl register admin localhost password

service ejabberd restart

echo 'Now please go to localhost:5280/admin and add 2 users'
echo 'foo@localhost with password: foo'
echo 'bar@localhost with password: bar'
