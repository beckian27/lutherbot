async def make_shopping_list(msg):
    requests = []
    async for request in msg.channel.history(limit = 2000, before = msg):
        # scans messages until previous list request
        if request.content.startswith('!shopping'):
            break
        if request.content.startswith('!'):
            for line in request.content.splitlines():
                requests.append(line.strip('! '))
    
    fs_dm = client.get_channel(FS_DM_ID)    

    # generates alphabetized shopping list in private channel
    # adds a reaction to each item to act as a check off button
    for request in sorted(requests):
        mymsg = await fs_dm.send(request)
        await mymsg.add_reaction(CHECK_MARK_CODE)
        
    copypaste = '' # also sends a single copy-pasteable message for this who prefer not to use this
    for request in sorted(requests):
        if len(copypaste) > 1950: # if message approches discord char limit
            await fs_dm.send(copypaste)
            copypaste = ''

        copypaste = copypaste + request + '\n'
    
    await fs_dm.send(copypaste)

async def delete_item(payload):
    user = await client.fetch_user(payload.user_id)
    
    if not user.bot:
        fs_dm = client.get_channel(FS_DM_ID)
        message = await fs_dm.fetch_message(payload.message_id)
        
        if message.author.bot:
            await fs_dm.delete_messages([message])