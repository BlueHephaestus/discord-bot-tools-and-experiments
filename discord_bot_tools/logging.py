import discord_bot_tools as dt
import datetime, os, asyncio

async def log_all_messages(client):
    """
    Arguments:
        client: A discord.py Client Object
    """
    print("Logging All Messages for %s..." % client.user.name)

    """
    Then loop through the connected channels from expected smallest amount to largest amount:
        1. Private Messages
        2. Servers -> Server Channels
    """
    await log_all_private_messages(client)
    await log_all_server_messages(client)
        
    print("Completed Logging All Messages for %s." % client.user.name)

async def log_all_server_messages(client):
    """
    Arguments:
        client: A discord.py Client Object
    """
    print("Logging All Server Messages for %s from %i Servers..." % (client.user.name, len([server for server in client.servers])))

    await log_channel_messages(client, client.get_all_channels())

    print("Completed Logging All Server Messages for %s." % client.user.name)

async def log_all_private_messages(client):
    """
    Arguments:
        client: A discord.py Client Object
    """
    print("Logging All Private Messages for %s from %i Private Channels..." % (client.user.name, len([private_channel for private_channel in client.private_channels])))

    await log_private_messages(client, client.private_channels)

    print("Completed Logging All Private Messages for %s." % client.user.name)

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
    """
    servers = [server for server in server_iterable]
    for server in servers:
        if isinstance(server, str):
            print("Logging Server Messages from %s for %s." % (server, client.user.name))
            await log_server_str_messages(client, server)
            print("Completed Logging Server Messages from %s for %s." % (server, client.user.name))
        else:
            print("Logging Server Messages from %s for %s." % (server.name, client.user.name))
            await log_server_obj_messages(client, server)
            print("Completed Logging Server Messages from %s for %s." % (server.name, client.user.name))


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
    """
    await log_channel_messages(client, server.channels)

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
    """

    """
    We already have our query, just need our strings to search through.
    This is easily obtained by getting the names of all the servers our client is connected to.
    """
    servers = [server for server in client.servers]
    server_names = [server.name for server in servers]

    #idxs is plural of i because otherwise we would be saying "is"
    search_result_idxs = dt.search_strings(server_str, server_names)

    #If we have results
    if len(search_result_idxs) > 0:
        #Get first result and reference our server object with it.
        first_search_result_i = search_result_idxs[0]
        server_obj = servers[first_search_result_i]

        #Then log messages from this object
        await log_server_obj_messages(client, server_obj)

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
    """
    channels = [channel for channel in channel_iterable]
    for channel in channels:
        if isinstance(channel, str):
            await log_channel_str_messages(client, channel)
        else:
            await log_channel_obj_messages(client, channel)

async def log_channel_obj_messages(client, channel):
    """
    Arguments:
        client: A discord.py Client Object
        channel: A channel OBJECT from discord.py .

    Returns:
        Logs messages from channel using the usual format.
        Will use server attribute to determine the server directory.
    """
    log_fname = channel.name + ".log"
    log_fpath = dt.get_valid_filename(client.user.name) + os.sep + "Servers" + os.sep + dt.get_valid_filename(channel.server.name) + os.sep + dt.get_valid_filename(log_fname)

    with open(log_fpath, "w") as f:
        log = []
        try:
            async for msg in client.logs_from(channel, limit=100100100100):
                log.append(msg)
        except:
            pass
        log = dt.sort_log(log)
        for msg in log:
            f.write(dt.get_msg_str(msg))

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
    """

    """
    We already have our query, just need our strings to search through.
    This is easily obtained by getting the names of all the channels our client is connected to.
    """
    channels = [channel for channel in client.get_all_channels()]
    channel_names = [channel.name for channel in channels]

    #idxs is plural of i because otherwise we would be saying "is"
    search_result_idxs = dt.search_strings(channel_str, channel_names)

    #If we have results
    if len(search_result_idxs) > 0:
        #Get first result and reference our channel object with it.
        first_search_result_i = search_result_idxs[0]
        channel_obj = channels[first_search_result_i]

        #Then log messages from this object
        await log_channel_obj_messages(client, channel_obj)

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
    """
    private_channels = [private_channel for private_channel in private_channel_iterable]
    for private_channel in private_channels:
        if isinstance(private_channel, str):
            await log_str_private_messages(client, private_channel)
        else:
            await log_obj_private_messages(client, private_channel)

async def log_obj_private_messages(client, private_channel):
    """
    Arguments:
        client: A discord.py Client Object
        private_channel: A PrivateChannel OBJECT from discord.py .

    Returns:
        Logs messages from PrivateChannel object using the usual format.
        Will use their recipient count to determine if it is a group private message or not.
    """
    if len(private_channel.recipients) == 1:
        #One user message
        log_fname = private_channel.user.name + ".log"
        log_fpath = dt.get_valid_filename(client.user.name) + os.sep + "Private_Messages" + os.sep + dt.get_valid_filename(log_fname)
    else:
        #Group Message
        log_fname = '-'.join([user.name for user in private_channel.recipients]) + "-" + dt.get_date_str(private_channel.created_at) + ".log"
        log_fpath = dt.get_valid_filename(client.user.name) + os.sep + "Private_Group_Messages" + os.sep + dt.get_valid_filename(log_fname)

    with open(log_fpath, "w") as f:
        log = []
        try:
            async for msg in client.logs_from(private_channel, limit=100100100100):
                log.append(msg)
        except:
            pass
        log = dt.sort_log(log)
        for msg in log:
            f.write(dt.get_msg_str(msg))

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
    """

    """
    We already have our query, just need our strings to search through.
    This is easily obtained by getting the names of all the private channels our client is connected to.
    We get these names in a similar way to how we get them for their log filenames in log_obj_private_messages(), 
        but without the filename, file extension, filepath, and date. We use recipients to tell if it is a group or private message.
    """
    private_channels = [private_channel for private_channel in client.private_channels]
    private_channel_names = []
    for private_channel in private_channels:
        if len(private_channel.recipients) == 1:
            #One user message
            private_channel_name = private_channel.user.name
        else:
            #Group Message
            private_channel_name = '-'.join([user.name for user in private_channel.recipients]) 

        #Add to list of names
        private_channel_names.append(private_channel_name)

    #idxs is plural of i because otherwise we would be saying "is"
    search_result_idxs = dt.search_strings(private_channel_str, private_channel_names)

    #If we have results
    if len(search_result_idxs) > 0:
        #Get first result and reference our private channel object with it.
        first_search_result_i = search_result_idxs[0]
        private_channel_obj = private_channels[first_search_result_i]

        #Then log messages from this object
        await log_obj_private_messages(client, private_channel_obj)
