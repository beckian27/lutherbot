async def create_makeup(msg, check):
    if msg.content.startswith('!makeup'):
        opportunity = msg.content.removeprefix('!makeup ')
        opportunity = opportunity + '\nClick the check mark to claim this chore!'
        await msg.channel.delete_messages([msg])
        msg = await msg.channel.send(opportunity)
        await msg.add_reaction(check)

async def claim_makeup(payload, client, serve, makeup, worm):
    server = await client.fetch_guild(serve)
    user = await server.fetch_member(payload.user_id)
    
    if not user.bot:
        channel = client.get_channel(makeup)
        message = await channel.fetch_message(payload.message_id)
        
        if message.author.bot:
            text = message.content
            await channel.delete_messages([message])

            if not user.get_role(worm):
                text = text.removesuffix('\nClick the check mark to claim this chore!')
                text = f'{text}\n{user.display_name} claimed this chore!'
                await channel.send(text)
