#!/bin/bash

# Usage
#
# In order to send authenticated mail to the tmp_user you need to
# export these environment variables before running this script:
#   - FROM_EXTERNAL_OPTS for sending mails from external mailservers to the tmp_user account
#
# as an example:
#   export FROM_EXTERNAL_OPTS='-f user@example.org --tlsc --au user@example.or -ap MYPASSWORD -s smtp.example.org'


set -x
set -e

PROVIDER='cdev.bitmask.net'
BCTL='bitmaskctl'
LEAP_HOME="$HOME/.config/leap"
MAIL_UUID=$(uuidgen)

username="tmp_user_$(date +%Y%m%d%H%M%S)"
user="${username}@${PROVIDER}"
pw="$(head -c 10 < /dev/urandom | base64)"
SWAKS="swaks -t $user --h-Subject $MAIL_UUID"

# Stop any previously started bitmaskd
# and start a new instance
"$BCTL" stop

rm -rf "$LEAP_HOME"

"$BCTL" start


# Register a new user
"$BCTL" user create "$user" --pass "$pw"

# Authenticate
"$BCTL" user auth "$user" --pass "$pw"

# Note that imap_pw is the same for smtp

imap_pw="None"

# FIXME -- this would be prettier if we had the auth command block on
# the first-time run, so that we just return when the key has been generated
# and explicitely raise any error found

while [[ $imap_pw == *"None"* ]]; do
  response=$("$BCTL" mail get_token)
  sleep 2
  imap_pw=$(echo "$response" | head -n 1 | sed 's/  */ /g' | cut -d' ' -f 2)
done

$SWAKS $FROM_EXTERNAL_OPTS


echo "IMAP/SMTP PASSWD: $imap_pw"

# Send testmail
$SWAKS $FROM_EXTERNAL_OPTS

# XXX wait until we the get mail we just sent.

while [[ ! $(./getmail --mailbox INBOX --subject "$MAIL_UUID" $user $imap_pw) ]]
do
  sleep 10
done
