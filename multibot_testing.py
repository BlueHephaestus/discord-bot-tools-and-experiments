import tool_testing
from threading import Thread

"""
Each value in the bots dict is like so:
    token: Discord token.
    is_bot: If the token is for a bot account or user account.
    client: Function to call to initialize our bot's client and execute its code
"""
bots = {
            "DarkElement":("token", False, tool_testing.main),
       }

for bot in bots.keys():
    """
    Spawn a new thread for this bot. 
    """
    token, is_bot, client = bots[bot]
    Thread(target=client, args=(token, is_bot)).start()
