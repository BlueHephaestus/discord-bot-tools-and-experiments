"""
Template for one of our ghost bots.

Makes use of our tools and other such code along with the rest of our files
    to give the caller account behavior unique to this template.

Currently only used by Akari, but may expand to more if needed.
"""
import discord
import discord_bot_tools as dt
import asyncio
import pickle


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

    @client.event
    async def on_message(msg):
        await handle_message(msg)
        

    async def handle_message(msg):
        """
        How we handle each individual message we encounter.
        """
        """
        If we get summoned, print the summoning message
        We check if any of these returned matches by checking if they are not all False.
            If any are not false(i.e. are messages or list of results), it means one of our queries was successful and found matches

        So we loop through our results for each search, and if we find something != False,
            we notify darkelement and set our flag so as never to notify twice. 

        Note: I didn't include DarkElement's id ("151561724338765824"), because I didn't want double notifications whenever I was pinged.
        """
        #Our flag for if we already notified 
        notified = False
        search_results = dt.multiquery_message(msg.content, ["darkelement", "akari", "88089662303784960"], ignore_case=True)
        for search_result in search_results:
            #Main check
            if search_result != False:
                #Check if it's a PM, so we avoid recursion
                if msg.server != None:
                    await notify_darkelement(msg)
                    notified = True
                    break

        """
        If we get pm'd, it's not from ourselves, and we haven't notified darkelement yet, notify.
        """
        if msg.server == None and not (msg.author.name == client.user.name) and not notified:
            await notify_darkelement(msg)
            notified = True

    async def notify_darkelement(msg):
        """
        In this case, we simply print it to notify him.
        """
        print("{}".format(dt.get_global_msg_str(msg)))

    """
    Finally, run our bot. This should be the last thing in main(), since it blocks execution.
    """
    client.run(token, bot=is_bot, loop=loop)
