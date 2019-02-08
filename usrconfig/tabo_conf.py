# This is the configuration file for TABO. You need to edit this file
# to setup the bot. Do not edit this file using Windows Notepad as it ruins the
# formatting. use Notepad++ or a code editor like VSC, Atom, Python IDLE.
# This file wrote with VSC. (following Python 3 format)
# For help, see: https://

# To get IDs, enable Developer Mode in Discord (Options -> Settings -> Appearance)
# on Discord and then right-click the person/channel you want to get the
# channel of, then click 'Copy ID'. You can also use the 'listids' command.


# SETTINGS
# This is your Discord bot account token.
# Find your bot's token here: https://discordapp.com/developers/applications/me/
# Create a new application, with no redirect URI or boxes ticked.
# Then click 'Create Bot User' on the application page and copy the bot token here.
# This is not application Client ID. This is Application > BOT Token. 
Token = ''

# The bot need databese. We supports MySQL, Maria DB (and the other)
# You have to fill in these options with valid
# details, following these instructions: https://
SQL_Hostname = ''
SQL_Username = ''
SQL_Password = ''
SQL_DBName = ''

# The bot need databese. We supports MySQL, Maria DB (and the other)
# You have to fill in these options with valid
# details, following these instructions: https://
logusr = 'SYSTEM'

# Permissions
# This option determines which user has full permissions and control of the bot.
# You can only set one owner, but you can use permissions.ini to give other
# users access to more commands.
# Setting this option to 'auto' will set the owner of the bot to the person who
# created the bot application, which is usually what you want. Else, change it
# to another user's ID.
OwnerID = ''

# This option determines which users have access to developer-only commands.
# Developer only commands are very dangerous and may break your bot if used
# incorrectly, so it's highly recommended that you ignore this option unless you
# are familiar with Python code.
DevIDs = ''

# This option determines which users have access to Tabo Plus-only commands.
# If you don't have Tabo Plus, you can buy it here: 
# or just pass this option.
LicenseSecret = ''


# [Chat]
# Determines the prefix that must be used before commands in the Discord chat.
# e.g if you set this to !, the login command would be triggered using !login.
CommandPrefix = '/'
