import datetime
import discord

def create_embed(interaction, game, game_id, custom_info, vc):
    game_name = f"{game.name_chn} ({game.name_eng})"
    rank = game.rank
    mode = game.mode
    embed = discord.Embed(
        title=f"发起了 {game_name} 组队邀请！",
        description=f"{interaction.user.mention}： “{custom_info}”"
    )
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
    embed.set_thumbnail(url=f"attachment://{game.logo}")

    embed.add_field(name="游戏ID （点击复制）", value=f"```{game_id}```", inline=False)
    embed.add_field(name="游戏模式", value=mode[0], inline=True)

    rank_emoji = "" if len(rank) < 3 else rank[2]
    embed.add_field(name="所在段位", value=f"{rank_emoji}{rank[0]}", inline=True)
    embed.add_field(name="目前人数", value=f"{len(vc.members)}/{game.max_player}")

    embed.colour = game.colour

    embed.set_footer(text="发布于")
    embed.timestamp = datetime.datetime.now()

    return embed
