import discord
from game import Game
import data_handler
import lfg_request
from discord.partial_emoji import PartialEmoji

data_handler = data_handler.DataHandler()


class CustomSelect(discord.ui.Select):
    def __init__(self, placeholder, options, custom_id, max_values=1, min_values=1):
        super().__init__(placeholder=placeholder, max_values=max_values, min_values=min_values, options=options,
                         custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()


class FinalInfoModal(discord.ui.Modal):
    def __init__(self, title, game, game_id):
        super().__init__(title=title)
        self.game = game
        self.request_sent = False
        self.game_id_str = ""
        if game_id is not None:
            self.game_id_str = game_id[0]
        id_input_field = discord.ui.TextInput(label='游戏ID',
                                              placeholder=f"你的 {game.name_chn}({game.name_eng}) 游戏ID",
                                              default=self.game_id_str, custom_id="game_id")
        self.add_item(id_input_field)
        self.add_item(
            discord.ui.TextInput(label='有什么想对队友说的吗?', style=discord.TextStyle.paragraph, required=False,
                                 custom_id="additional_info"))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        game_id_submission = ""
        additional_info_submission = ""
        for child in self.children:
            if child.custom_id == "additional_info":
                additional_info_submission = child.value
            if child.custom_id == "game_id":
                game_id_submission = child.value

        request_manager = lfg_request.RequestManager()
        request_result = await request_manager.create_request(interaction, self.game, game_id_submission,
                                                              additional_info_submission)
        await interaction.followup.send(request_result, ephemeral=True, suppress_embeds=True)


class SubmitButton(discord.ui.Button):
    def __init__(self, game_index):
        super().__init__(label="立即招募队友", style=discord.ButtonStyle.green, custom_id="submit_button")
        self.game = Game.get_games()[game_index]()

    async def callback(self, interaction: discord.Interaction):
        # Retrieve the user's current id for the given name
        game_id = data_handler.get_game_id(interaction.user.id, self.game.name_eng)

        # Create modal with these info: game index, rank index, mode index, game id
        modal = FinalInfoModal(f"向队友提供你的个人信息", self.game, game_id)
        await interaction.response.send_modal(modal)


class RankSelect(CustomSelect):
    def __init__(self, ranks):
        options = [discord.SelectOption(emoji=None if len(rank) < 3 else PartialEmoji.from_str(rank[2]), label=rank[0],
                                        description=rank[1], value=str(index)) for index, rank in enumerate(ranks)]
        super().__init__(placeholder="选择游戏段位", options=options, custom_id="rank_select")
        self.button = None

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.button is None:
            for child in self.view.children:
                if isinstance(child, SubmitButton):
                    self.button = child

        for option in self.options:
            if option.value == self.values[0]:
                option.default = True
            else:
                option.default = False

        self.button.game.rank = self.button.game.ranks[int(self.values[0])]
        print(f"[Rank Select]\t{interaction.user.name} selected {self.button.game.ranks[int(self.values[0])][1]}")

        view = self.view
        if all(len(getattr(child, 'values', [None])) == 1 for child in view.children):
            self.button.disabled = False
            await interaction.edit_original_response(view=view)


class ModeSelect(CustomSelect):
    def __init__(self, modes):
        options = [discord.SelectOption(label=mode[0], description=mode[1], value=str(index)) for index, mode in
                   enumerate(modes)]
        super().__init__(placeholder="选择游戏模式", options=options, custom_id="mode_select")
        self.button = None

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.button is None:
            for child in self.view.children:
                if isinstance(child, SubmitButton):
                    self.button = child

        for option in self.options:
            if option.value == self.values[0]:
                option.default = True
            else:
                option.default = False

        self.button.game.mode = self.button.game.modes[int(self.values[0])]

        view = self.view
        if all(len(getattr(child, 'values', [None])) == 1 for child in view.children):
            self.button.disabled = False
            await interaction.edit_original_response(view=view)


class GameSelect(CustomSelect):
    def __init__(self):
        self.gamelist = Game.get_games()
        options = [
            discord.SelectOption(emoji=game.emoji, label=game.name_chn, description=game.name_eng, value=str(index)) for
            index, game in enumerate(self.gamelist)]
        super().__init__(placeholder="Select a game", options=options, custom_id="game_select")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        index = interaction.data['values'][0]
        game = self.gamelist[int(index)]
        rankMenu = RankSelect(game.ranks)  # use game.ranks to initialize a RankSelect
        modeMenu = ModeSelect(game.modes)  # use game.modes to initialize a ModeSelect
        submitButton = SubmitButton(int(index))
        submitButton.disabled = True

        # Create the message to replace original:
        message = f"{str(game.emoji)} 已选择：{game.name_chn} ({game.name_eng})\n 请选择段位和游戏模式："

        # Create a new view that includes both RankSelect and ModeSelect
        view = discord.ui.View()
        view.add_item(rankMenu)
        view.add_item(modeMenu)
        view.add_item(submitButton)

        # Edit the original message to include the new dropdown menus
        await interaction.edit_original_response(content=message, view=view)
        print(f"[Game Select]\t{interaction.user.name} selected {game.name_eng}")


class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(GameSelect())
