import discord
import config
import tasks
from lfg_request import RequestManager

rq_mgr = RequestManager()


# The function that registers the client to all defined events
def setup(client, command_tree, guild, silent):
    # On ready is run when the bot finishes logging in
    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")
        if not silent:
            await client.get_channel(config.announcement_channel).send(content=f"@everyone"
                                       f"组队Bot 刚刚进行了重新启动并升级到了版本`v{config.bot_version}`, "
                                       f"更新日志如下：```{config.update_log}```"
                                       f"\n请在任意频道的消息框中使用/lfg指令来发起组队邀请。（图文教学请参照[此条消息]({config.tutorial_link})）"
                                       f"\n遇到Bug请联系<@356237738183360515>", suppress_embeds=True)
        # tasks.update_lfg_messages.start(client)
        tasks.report_state.start(client)
        await command_tree.sync(guild=guild)

    @client.event
    async def on_voice_state_update(member, before, after):
        # Making a dict copy so that looping over it won't be interrupted by item addition
        requests_dict = dict(rq_mgr.requests)
        matching_requests = set()

        # Iterate over the requests and check for channel match with before or after state
        for userid, request in requests_dict.items():
            # Check that before.channel and after.channel are not None before comparing IDs
            if (before.channel is not None and before.channel.id == request.channel.id) or \
                    (after.channel is not None and after.channel.id == request.channel.id):
                matching_requests.add(request)
                if before.channel is None:
                    print(f"[Voice State Update]\t{member.name} joined {after.channel.name}")
                elif after.channel is None:
                    print(f"[Voice State Update]\t{member.name} joined {before.channel.name}")
                else:
                    print(f"[Voice State Update]\t{member.name} moved from {before.channel.name} to {after.channel.name}")


        # Do something with matching_requests, like printing them
        for rq in matching_requests:
            current_embed = rq.message.embeds[0]
            current_name = current_embed.fields[3].name
            current_value = current_embed.fields[3].value
            current_inline = current_embed.fields[3].inline
            current_value_split = current_value.split('/')
            current_member_count = int(current_value_split[0])
            max_member_count = int(current_value_split[1])
            member_count = len(rq.channel.members)
            if member_count != current_member_count:
                await rq.message.edit(
                    embed=current_embed.set_field_at(index=3, name=current_name, inline=current_inline,
                                                     value=f"{member_count}/{max_member_count}"), attachments=[])
                print(
                    f"[Message update]\tAffected message: {rq.message.jump_url}, target channel: {current_member_count} -> {member_count}")

