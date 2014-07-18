trollBot
========

A twisted IRC bot written in python. Hopefully this will end up being very easy to use and will support TLS. This is GPL v3 licenced.

# Usage:
You will need python 2.7, PyYAML and the twisted networking stuff (including components for TLS). See https://twistedmatrix.com/trac/.

Copy trollBot.yaml.example to trollBot.yaml and edit it to include the login details of the IRC server and channel which you would like to use. Also specify the regular expressions used for matching messages and the response texts. Two examples have been included already.

Finally run trollBot.py.
