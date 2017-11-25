
# SimpleBot

Simplebot is a way to make an irc bot really easily.

Just make a program that reads and write to stdin and stdout (the default input and output) and use simplebot to pipe it to and from irc

# To run:
Copy simplebot.py, subapi.py and ircsender.py to one of your own folders
Create a config.json in the same folder (or copy and edit the example one), or add a path to a config file as command line argument.

The config file should have the following properties:

- "server": the irc server
- "port": the irc server
- "nickname": the name of the bot in irc
- "channels": a list of channels that the bot should join
- "program": the command to start your program. This can be eiter a string or a list of strings. If an executable if run from a relative path, the path is relative to the location of the config file
- "format": the format in which the input is passed to the program.
  If this field is ommitted or null it will just pass the message text.
  Otherwise it will pass the string with the following string conversions:
  * "{text}" will be replaced with the message text
  * "{nick}" will be replaced with the nick of the sender
  * "{chan}" will be replaced with the channel it was sent in



echobot.py is an example of a program that can be run with simplebot

Simplebot pipes the program's stdout line by line, so any output won't be send to irc until a newline character is encountered (most programming languages append a newline on their default print function)

Some languages do io buffering, which means they won't actually perform io actions when they are called, but later.
In python, this can be turned of with the -u option.
Alternatively you can flush stdout after every print

Warning: never run arbitrary code form irc or other users.
Someone could rm -rf ~ (remove all files in your home directory) or add more keys to your allowed_keys (granting them all acces to your account).
Most people here can be trusted, but anyone can join.
