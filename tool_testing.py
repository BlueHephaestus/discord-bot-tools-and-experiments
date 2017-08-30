import discord
import discord_bot_tools as dt
import asyncio

"""
Initialize an object for use later, we can have helpful attributes as a part of this class.

We shouldn't need to pass in the name, it should use the given name by default and only change that if a name arg is passed in.
"""

def main(token, is_bot=True):
    """
    This will probably be run inside a thread, so spawn a new event loop for our thread to use.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    """
    Initialize a new discord client for this bot
    """
    client = discord.Client()
    @client.event
    async def on_ready():

        print('Logged in as %s' % client.user.name)
        print('------')
        dt.ensure_dir(dt.get_valid_filename(client.user.name))

        """
        Make sure we have our necessary directories for logging
        """
        dt.ensure_necessary_log_dirs(client)

        #ALL THE MESSAGES from everywhere - tested
        #await dt.log_all_messages(client)

        #All Servers - tested
        #await dt.log_all_server_messages(client)

        #All Private Messages - tested
        #await dt.log_all_private_messages(client)
        
        #Example server and channel from that server, and private channel
        server = [channel for channel in client.get_all_channels()][0].server
        channel = [channel for channel in server.channels][0]
        private_channel = [private_channel for private_channel in client.private_channels][0]

        #Server object -> All Channels - tested
        #await dt.log_server_messages((client, [server]))

        #Server -> Channel object -> All messages - tested
        #await dt.log_channel_messages((client, [channel]))

        #Server strings -> All Channels  - tested
        #await dt.log_server_messages((client, ["bot testing"]))

        #Server(s) -> Channel strings -> All messages - tested
        #await dt.log_channel_messages((client, ["academy"]))

        #Private Channel object -> All messages - tested
        #await dt.log_private_messages((client, [private_channel]))

        #Private Channel string -> All messages - tested
        #await dt.log_private_messages((client, ["darkelement"]))

        #Regex all logfiles for a regex query and return all results found as list of messages - not asynchronous - tested
        #res = dt.regex_messages(client, r"<TAG\b[^>]*>(.*?)</TAG>", return_full_message=False)


        #Search for matches of a given string, and return all results found as list of messages. Actually is a one-liner to call regex_messages with a nice regex so it takes the same arguments. - not asynchronous - tested
        #res = dt.query_messages(client, "asdf", return_full_message=False)

        #Since our profile never exits, we have this here so we know when we can force shut it off.
        print("Completed Execution.")

    @client.event
    async def on_message(msg):
        print(dt.get_global_msg_str(msg))

    """
    Finally, run our bot. This should be the last thing in main(), since it blocks execution.
    """
    client.run(token, bot=is_bot, loop=loop)

