import discord
from game import Game
from embed_creator import create_embed
import config
import data_handler
data_handler = data_handler.DataHandler()
class RequestManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RequestManager, cls).__new__(cls)
            cls._instance.requests = dict()
        return cls._instance

    async def create_request(self, interaction, game, game_id, custom_info):

        # 1. If the user has already created a request, deny the new request
        if interaction.user.id in self.requests.copy():
            existing_request = self.requests[interaction.user.id]
            return f"每个人同时只能发布一条LFG信息。请先删除[这条信息]({existing_request.message.jump_url})再重新发布。"


        # 2. If the user isn't in a voice channel, deny the request
        if interaction.user.voice is None:
            return "请先点击左侧语音列表，加入一个语音频道后，再尝试使用/lfg"
        else:
            vc = interaction.user.voice.channel

        # 3. Craft the request message
        embed = create_embed(interaction, game, game_id, custom_info, vc)

        # 4. Send the request message to specified channel
        channel = interaction.guild.get_channel(game.channel)
        file = discord.File(f"Resources/Logos/{game.logo}", filename=game.logo)
        view = discord.ui.View()
        vc_invite = await vc.create_invite(temporary=True, max_age=3600*24)
        vc_url = vc_invite.url
        view.add_item(JoinButton(vc.name, vc_url))
        view.add_item(DeleteButton(interaction.user.id))
        view.timeout = None
        message = await channel.send(file=file, embed=embed, view=view)

        # 5. Create a Request object, add it to self.requests
        request = Request(channel=vc, message=message)
        self.requests[interaction.user.id] = request

        # 6. Update the database with the gamer's id info
        if game_id != "":
            data_handler.try_edit_or_add_game_id(interaction.user.id, game.name_eng, game_id)

        print(f"[Request Posted] {interaction.user.name} posted a {game.name_eng} request: {request.message.jump_url}")
        return f"成功发布了队友招募信息，[点此查看]({message.jump_url})。"

    async def remove_request(self, discord_id):
        # Find the request in self.requests
        if discord_id not in self.requests:
            raise RuntimeError(f"Trying to delete user {discord_id}'s request but there isn't one")
        request = self.requests[discord_id]

        # Delete the associating message
        await request.message.delete()

        # Remove the request from self.requests
        del self.requests[discord_id]


class Request:
    def __init__(self, channel, message):
        self.channel = channel
        self.message = message

    def __str__(self):
        s = f"\tchannel: {self.channel.name}\t\tmessage: {self.message.jump_url}\n"
        return s

    def __eq__(self, other):
        return id(self) == id(other)

    def __hash__(self):
        return hash(id(self))


# The two buttons
class JoinButton(discord.ui.Button):
    def __init__(self, name, url):
        super().__init__(label=f"点击加入 {name}", url=url)

class DeleteButton(discord.ui.Button):
    def __init__(self, user_id):
        super().__init__(label="删除", style=discord.ButtonStyle.red)
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        can_delete = False
        is_self = self.user_id == interaction.user.id
        is_admin = any(role.id == config.moderator_role_id for role in interaction.user.roles)
        suffix = "(Admin)" if is_admin and not is_self else ""

        if is_self or is_admin:
            await interaction.response.defer()
            request_mgr = RequestManager()
            await request_mgr.remove_request(self.user_id)
            print(f"[Request Removal] {interaction.user.name} successfully deleted the request by {self.user_id} {suffix}")
        else:
            await interaction.response.send_message("不可以删除别人的组队请求喔", ephemeral=True)
