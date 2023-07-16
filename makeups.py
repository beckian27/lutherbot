async def create_makeup(msg, check):
    if msg.content.startswith('!makeup'):
        opportunity = msg.content.removeprefix('!makeup ')
        opportunity = opportunity + '\nClick the check mark to claim this chore!'
        await msg.channel.delete_messages([msg])
        msg = await msg.channel.send(opportunity)
        await msg.add_reaction(check)