import discord
from ui_main_menu import MenuView
from discord import app_commands
from lfg_request import RequestManager


def setup(client, guild):
    tree = app_commands.CommandTree(client)

    @tree.command(name="lfg", description="寻找游戏队友！", guild=guild)
    async def lfg(interaction):
        print(f"[Command Execution]/lfg called by:\t{interaction.user.name} ")

        # Check if the user already has a reqeust
        request_mgr = RequestManager()
        if interaction.user.id in request_mgr.requests:
            existing_request = request_mgr.requests[interaction.user.id]
            await interaction.response.send_message(
                f"每个人同时只能发布一条LFG信息。请先删除[这条信息]({existing_request.message.jump_url})再重新发布。",
                ephemeral=True, suppress_embeds=True)
            print(f"[Command Execution]\t{interaction.user.name} failed to create a request. (Already having one)")
            return

        # Check if the user is in a VC
        if interaction.user.voice is None:
            await interaction.response.send_message(
                "请先点击左侧语音列表，加入一个语音频道后，再尝试使用/lfg",
                ephemeral=True, suppress_embeds=True)
            print(f"[Command Execution]\t{interaction.user.name} failed to create a request. (Not in a VC)")
            return

        # Show the menu
        await interaction.response.send_message(f"{interaction.user.mention} 欢迎使用LFG Bot!\n今天要玩什么游戏呢？",
                                                view=MenuView(), ephemeral=True)

    return tree
