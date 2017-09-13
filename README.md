# Description 

# Installation

1. Download/Clone this repository

2. Open `multibot_testing.py` with your editor of choice, and change "DarkElement" to be your account's nickname, e.g. "EternalEnvy". 

3. Then change "token" to your account's token, which can be obtained by opening developer tools in discord's client, going to the "Application" tab, then getting the value of the "token" key.

4. Don't share this token, it will give anyone access to your entire discord account. I encourage looking through the code in this repository to assure yourself that this is a safe 
  use of your token, and that it will not be used for malevolent reasons. I use discord.py as the backend for many functions, which is a reliable source.

5. Change any of the arguments as you wish for this bot / account, using the below documentation.

6. Add whatever functions you want to the main section of template_tool_testing.py, for the functions of this bot.

7. Feel free to add other bots to run asynchronously alongside each other in the bots dictionary, 
  using different templates if you wish for them to have different functions. Again, I encourage reading the documentation.

8. Run with `python3.6 multibot_testing.py`

# Requirements

**Python 3.6**

**Python Libraries**:

* discord
* threading
* asyncio
* datetime
* os
* re

# Documentation

While `discord_bot_tools/` contains the functions which each bot can use, it is important that they are called correctly.

In order to create a new bot, you must add it to the bots dictionary in `multibot_testing.py`, as detailed in the above installation instructions. Then, you must add function calls for each function you wish your bot to execute, in the associated template file for each bot. By default, this template file is `template_tool_testing.py`. I recommend knowledge of Python 3.6 for this. 

Below is the detailed documentation for functions available in `discord_bot_tools/`, which can be used when creating these template files. `template_tool_testing.py` contains a good deal of commented example calls to these functions as well, however the below documentation will enable you to understand how to call each and every function, and what they do.

## logging.py - All functions included

### log_all_messages(client)

**Arguments:**

* **client**: A discord.py Client Object

**Returns:**

Logs messages from all private channels, servers, everything it can see.


### all_messages(client):

**Arguments:**

* **client**: A discord.py Client Object

**Returns:**

Exactly like our log_all_messages function, except this function is a generator.  It loops through all messages belonging to the client object, be them in private channels, private group messages, servers, or whatever.  

I could write a version of these for every single other log_ function, but I really don't want to yet.


async def log_all_server_messages(client):
    """
    Arguments:
        client: A discord.py Client Object

    Returns:
        Logs messages from all servers and channels in these servers.


async def log_all_private_messages(client):
    """
    Arguments:
        client: A discord.py Client Object

    Returns:
        Logs messages from all private messages and private group messages.


async def log_server_messages(client, server_iterable):
    """
    Arguments:
        client: A discord.py Client Object
        server_iterable: An iterable of servers, where all the servers are either strings or discord.py Server objects.
            Can be of any length > 0
    Returns:
        Will loop through every server in the server_iterable, and log messages from all channels in each server.
        Will call the appropriate function depending on if each server is a string or discord.py Server object.
        Will overwrite existing logs for this server, if it is found, using the usual message format. 


async def log_server_obj_messages(client, server):
    """
    Arguments:
        client: A discord.py Client Object
        server: A server OBJECT, from discord.py. 
            Do not confuse with log_server_str_messages, as this only works when the server is an object.

    Returns:
        All messages from the server object, including all channels of the server.
        Will overwrite existing logs for this server. 
        This is very useful when you want to ensure you get from a specific server,
            whereas log_server_str_messages can only search for the first server matching
            the name given, and use that. However, this function has the cost of it not being
            obvious what the server is when printing it, since it is a discord object


async def log_server_str_messages(client, server_str):
    """
    Arguments:
        client: A discord.py Client Object
        server_str: A server STRING.
            Do not confuse with log_server_obj_messages, as this only works when the server is a string.

    Returns:
        Searches for servers matching the string passed in, and uses the first result if found.
        If found, logs all messages from the server object, including all channels of the server.
        Will overwrite existing logs for this server. 
        This is very useful when you don't want to use an object, however you know the name
            and it's hopefully a unique name. While not as specific as the object, it is easier to use.


async def log_channel_messages(client, channel_iterable):
    """
    Arguments:
        client: A discord.py Client Object
        channel_iterable: An iterable of channels, where all the channels are either strings or discord.py Channel objects.
            Can be of any length > 0

    Returns:
            Will check the first element in the iterable and call the appropriate sub-function.
                If string -> log_channel_str_messages()
                If object -> log_channel_obj_messages()
            Will overwrite existing logs for all channels, if they are found, using the usual message format. 


async def log_channel_obj_messages(client, channel):
    """
    Arguments:
        client: A discord.py Client Object
        channel: A channel OBJECT from discord.py .

    Returns:
        Logs messages from channel using the usual format.
        Will use server attribute to determine the server directory.


async def log_channel_str_messages(client, channel_str):
    """
    Arguments:
        client: A discord.py Client Object
        channel_str: A channel STRING.
            Do not confuse with log_channel_obj_messages, as this only works when the channel is a string.

    Returns:
        Searches for channels matching the string passed in, and uses the first result if found.
        If found, logs all messages from the channel object.
        Will overwrite existing logs for this channel. 
        This is very useful when you don't want to use an object, however you know the name
            and it's hopefully a unique name. While not as specific as the object, it is easier to use.


async def log_private_messages(client, private_channel_iterable):
    """
    Arguments:
        client: A discord.py Client Object
        private_channel_iterable: An iterable of private messages / channels, where all the channels are either strings or discord.py private channel objects.
            Can be of any length > 0

    Returns:
            Will check the first element in the list and call the appropriate sub-function.
                If string -> log_channel_str_messages()
                If object -> log_channel_obj_messages()
            Will overwrite existing logs for all channels, if they are found, using the usual message format. 


async def log_obj_private_messages(client, private_channel):
    """
    Arguments:
        client: A discord.py Client Object
        private_channel: A PrivateChannel OBJECT from discord.py .

    Returns:
        Logs messages from PrivateChannel object using the usual format.
        Will use their recipient count to determine if it is a group private message or not.


async def log_str_private_messages(client, private_channel_str):
    """
    Arguments:
        client: A discord.py Client Object
        private_channel_str: A private channel STRING.
        Do not confuse with log_obj_private_messages, as this only works when the private channel is a string.

    Returns:
        Searches for private channels matching the string passed in, and uses the first result if found.
        If found, logs all messages from the private channel object.
        Will overwrite existing logs for this private channel. 
        This is very useful when you don't want to use an object, however you know the name
            and it's hopefully a unique name. While not as specific as the object, it is easier to use.
        When searching, will use only the name of the users. If it is a group message, it will not use a given name - instead using the users in the group message.
            If you have multiple group messages with the same users, then I suggest using that object or simply logging all private messages instead.


## misc_utils.py - Not all functions included

All functions are not included because not all of them are used in a standalone manner, many are used by our logging functions.

###

def get_msg_str(msg):
    """
    Arguments:
        msg: Discord.py Message object
    Returns:
        Gets a string formatted like
            date-author-content
        This should only be used when looking at one channel,
            since it doesn't include any server, channel, or even private message specifiers
            as for the location or origin of each message


def get_global_msg_str(msg):
    """
    Arguments:
        msg: Discord.py Message object

    Returns:
        Gets a string formatted like
            server(will not be included if private message)-channel(or private message if not a channel)-date-author-content
        This can be used when looking at any channel,
            since it includes specifiers as for the location or origin of each message


def recursive_get_paths(directory):
    """
    Arguments:
        directory : directory to recursively traverse. Should be a string.

    Returns:
        A list of filepaths, e.g.:
            "/home/darkelement/test.txt"        


def ensure_necessary_log_dirs(client):
    """
    Given a discord.py Client object, ensures that all directories are created for logging from any private message, channel, server, and so on.
    Will format as:
    <user>/
        servers/
            <server1>/
                <channel logfile>
                ...
            ...
        private messages/
            <logfile>
            ...
        private group messages/
            <logfile>
            ...


def search_strings(query, strings):
    """
    Arguments:
        query: A string to search our list of strings with.
        strings: A list of strings to search with our query.

    Returns:
        Does the following process:
        1. Converts query and all strings in list to lowercase, 
        2. Substitutes all non-alphanumeric characters for spaces (only in the strings),
        2. Divides query and all strings into list of words by splitting on space
        4. For every string list in our strings list, 
            check how many words match the words in our query and store both the integer "score" of that string, 
            and the index of our original string in a new list, with the format [score, index].
        5. Sort our original list of strings with the primary key as the score, and the secondary key as the original index.
        6. Only add entries which have scores of <= 0, and add the original index when adding an entry.

        So it returns indices for easy refererence, sorted by how closely each indices' associated string matched the query.


def regex_messages(client, regex_query, return_full_message=True, ignore_case=False):
    """
    Arguments:
        client: A discord.py Client Object
        regex_query: A regex string to use with python's re library, so it should be a valid string with that library.
            Example: regex_query = r"[^A-Z]"
        return_full_message: 
            If True, this function will return the entire message containing a match for our regex, 
                and information about if the matching message was from a channel in a server, a private message, or private group message. 
                It will do this out of all logfiles searched.
            If False, this function will only return a list of the strings which our regex matched,
                out of all logfiles searched.
        ignore_case:
            If True, will ignore case.
            If False, will not ignore case.

    Returns:
        Will go through all already existing logfiles under the client's username, 
            and return all matches from all logfiles using our regex_query for each logfile.
        if return_full_message=True,
            Will add on information about if the matching message was from a channel in a server,
                a private message, or private group message.
        if return_full_message=False,
            It will only return the section matching our regex.
        Since we may be connected to a lot of different servers and channels, or overrall
            may just have a fuckton of messages, we don't want to try loading all messages from 
            all connected channels into memory at once. So instead, we loop through all existing logfiles
            to do it one logfile at a time.
        This function is currently not asynchronous, though that may change.


def regex_message(message, regex_query, return_full_message=True, ignore_case=False):
    """
    Arguments:
        message: Message to check with our regex.
        regex_query: A regex string to use with python's re library, so it should be a valid string with that library.
            Example: regex_query = r"[^A-Z]"
        return_full_message: 
            If True, this function will return the entire message if it contained a match for our regex.
            If False, this function will only return a list of the strings which our regex matched.
        ignore_case:
            If True, will ignore case.
            If False, will not ignore case.

    Returns:
        Not to be confused with regex_messages, which works with all of our messages.
        This looks at the given message to see if our regex finds a match in it.
        If True,
            If return_full_message=True, this function will return the entire message if it contained a match for our regex.
            If return_full_message=False, this function will only return a list of the strings which our regex matched.
        If False, returns False.


def query_messages(client, query_str, return_full_message=True, ignore_case=True):
    """
    Arguments:
        client: A discord.py Client Object
        query_str: A query string, we will use this to search through all logfiles for matches of this string.
        return_full_message: 
            If True, this function will return the entire message containing a match for our query, 
                and information about if the matching message was from a channel in a server, a private message, or private group message. 
                It will do this out of all logfiles searched.
            If False, this function will only return a list of the strings which our query matched,
                out of all logfiles searched.
        ignore_case:
            If True, will ignore case.
            If False, will not ignore case.

    Returns:
        This function is literally one line to call regex_messages using our query_str to create a regex_query.
        So check the documentation there if you want to know how it works.
        We use \S*query_str\S* as our regex string, as it checks for any instances of our query string in another string, excluding bordering spaces.


def query_message(message, query_str, return_full_message=True, ignore_case=True):
    """
    Arguments:
        message: Message to check with our query.
        query_str: A query string, we will use this to search through all logfiles for matches of this string.
        return_full_message: 
            If True, this function will return the entire message if it contained a match for our query.
            If False, this function will only return a list of the strings which our query matched.
        ignore_case:
            If True, will ignore case.
            If False, will not ignore case.

    Returns:
        Not to be confused with query_messages, which works with all of our messages.
        This looks at the given message to see if our query finds a match in it.
        If True,
            If return_full_message=True, this function will return the entire message if it contained a match for our regex.
            If return_full_message=False, this function will only return a list of the strings which our regex matched.
        If False, returns False.

        Literally calls regex_message.


def multiquery_message(message, query_strs, return_full_message=True, ignore_case=True):
    """
    Arguments:
        message: Message to check with our query.
        query_strs: A list of query strings, we will use this to search through all logfiles for matches of this string.
        return_full_message: 
            If True, this function will return the entire message if it contained a match for our query.
            If False, this function will only return a list of the strings which our query matched.
        ignore_case:
            If True, will ignore case.
            If False, will not ignore case.

    Returns:
        Loops through all our query_strs, calling our query_message function using the arguments passed in. 
        Will return a list of the return values from each call.


































# Final Note

You can, as always, email me any questions you have. Good luck, have fun!

-Blake Edwards / Dark Element
