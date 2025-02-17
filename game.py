from discord.partial_emoji import PartialEmoji
from discord.colour import Colour
import config

# This file is responsible for defining the available game options in the menu


# Base Game class with common attributes and methods
class Game:
    _subclasses = []
    name_chn = ""
    name_eng = ""
    max_player = 0
    ranks = {}
    modes = {}
    emoji = None

    def __init__(self, rank=-1, mode=-1):
        self.rank = rank
        self.mode = mode

    def __init_subclass__(cls, **kwargs):
        if cls.__base__ is Game:
            Game._subclasses.append(cls)

    @classmethod
    def get_games(cls):
        return Game._subclasses if cls is Game else None

    @classmethod
    def get_game_index(cls):
        return Game.get_games().index(cls)

# Define game subclasses with specific settings
class Overwatch(Game):
    channel = config.overwatch
    name_chn = "守望先锋"
    name_eng = "Overwatch"
    max_player = 5
    colour = Colour.from_rgb(249, 158, 26)
    emoji = PartialEmoji.from_str("<:Overwatch_2_logo:1163939459683844129>")
    logo = "overwatch.png"
    ranks = [('任意', 'Any'),
             ('青铜', 'Copper', '<:ow1_bronze:1174866262178943066>'),
             ('白银', 'Silver', '<:ow1_silver:1174866269460238406>'),
             ('黄金', 'Gold', '<:ow1_gold:1174866265253351425>'),
             ('铂金', 'Platinum', '<:ow1_plat:1174866268038373538>'),
             ('钻石', 'Diamond', '<:ow1_diamond:1174866263114264627>'),
             ('大师', 'Master', '<:ow1_master:1174866266549407856>'),
             ('宗师', 'Grandmaster', '<:ow1_gm:1174866264603238521>'),
             ('500强', 'Top 500', '<:ow1_top_500:1174866270760484885>')]
    modes = [('快速', 'Quick Play'),
             ('开放排位', 'Open Queue'),
             ('预选排位', 'Role Queue'),
             ('其他', 'Others')]


class Apex(Game):
    channel = config.apex
    name_chn = "Apex英雄"
    name_eng = "Apex Legends"
    max_player = 3
    colour = Colour.from_rgb(205, 51, 51)
    emoji = PartialEmoji.from_str("<:apex_logo:1163672100012314635>")
    logo = "apex.png"
    ranks = [('任意', 'Any'),
             ('下三（青铜白银黄金）', 'Lower Three (Bronze, Silver, Gold)', '<:apex_Tier3_Gold:1174865395275018292>'),
             ('鉑金', 'Platinum', '<:apex_Tier4_Platinum:1174865396675915939>'),
             ('钻石', 'Diamond', '<:apex_Tier5_Diamond:1174865397648994404>'),
             ('大师', 'Master', '<:apex_Tier6_Master:1174865858095497256>'),
             ('猎杀', 'Predator', '<:apex_Tier7_Apex_Predator:1174865893524770846>')]
    modes = [('大逃杀', 'Battle Royale'),
             ('排位', 'Ranked'),
             ('团队死斗', 'Team Deathmatch'),
             ('控制', 'Control'),
             ('子弹时间', 'Bullet Time')]


class LeagueOfLegends(Game):
    channel = config.league
    name_chn = "英雄联盟"
    name_eng = "League of Legends"
    max_player = 5
    colour = Colour.from_rgb(180, 106, 55)
    emoji = PartialEmoji.from_str("<:league:1113566656090886195>")
    logo = "league.png"
    ranks = [('任意', 'Any', '<:League_Unranked:1174866185255391292>'),
             ('黑铁', 'Iron', '<:League_Iron:1174866175755305092>'),
             ('黄铜', 'Bronze', '<:League_Bronze:1174866167958093904>'),
             ('白银', 'Silver', '<:League_Silver:1174866183896432772>'),
             ('黄金', 'Gold', '<:League_Gold:1174866173079330866>'),
             ('铂金', 'Platinum', '<:League_Platinum:1174866183288262757>'),
             ('翡翠', 'Emerald', '<:League_Emerald:1174866171925897286>'),
             ('钻石', 'Diamond', '<:League_Diamond:1174866170667618425>'),
             ('大师', 'Master', '<:League_Master:1174866176921305108>'),
             ('宗师', 'Grandmaster', '<:League_Grandmaster:1174866174547333153>'),
             ('王者', 'Challenger', '<:League_Challenger:1174866169233150013>')]
    modes = [('匹配', 'Normal'),
             ('排位', 'Ranked'),
             ('云顶', 'TFT'),
             ('大乱斗', 'ARAM')]


class TheFinals(Game):
    channel = config.the_finals
    name_chn = "最终决战"
    name_eng = "The Finals"
    max_player = 3
    colour = Colour.from_rgb(211, 31, 60)
    emoji = PartialEmoji.from_str("<9UK6QGTY5BO3D7LD:1135832152794222613>")
    logo = "the_finals.png"
    ranks = [('任意', 'Any'),
             ('青铜', 'Bronze'),
             ('白银', 'Silver'),
             ('黄金', 'Gold'),
             ('鉑金', 'Platinum'),
             ('钻石', 'Diamond')]
    modes = [('快速', 'Quick Play'),
             ('排位', 'Ranked')]


class Valorant(Game):
    channel = config.valorant
    name_chn = "无畏契约"
    name_eng = "Valorant"
    max_player = 5
    colour = Colour.from_rgb(255, 70, 85)
    emoji = PartialEmoji.from_str("<:Valorant:1113566622330921131>")
    logo = "valorant.png"
    ranks = [('任意', 'Any'),
             ('黑铁', 'Iron', '<:Valorant_Iron_3_Rank:1174886736258682930>'),
             ('青铜', 'Bronze', '<:Valorant_Bronze_3_Rank:1174886728490823690>'),
             ('白银', 'Silver', '<:Valorant_Silver_3_Rank:1174886739853197404>'),
             ('黄金', 'Gold', '<:Valorant_Gold_3_Rank:1174886730814459955>'),
             ('鉑金', 'Platinum', '<:Valorant_Platinum_3_Rank:1174886737214976142>'),
             ('钻石', 'Diamond', '<:Valorant_Diamond_3_Rank:1174886729971404811>'),
             ('超凡入圣', 'Ascendant', '<:Valorant_Ascendant_3_Rank:1174886727467405422>'),
             ('神话', 'Immortal', '<:Valorant_Immortal_3_Rank:1174886732563484724>'),
             ('辐能战魂', 'Radiant', '<:Valorant_Radiant_Rank:1174886738494242898>')]
    modes = [('快速', 'Quick Play'),
             ('排位', 'Ranked'),
             ('娱乐', 'Spike Rush')]


class CounterStrike(Game):
    channel = config.cs
    name_chn = "反恐精英"
    name_eng = "Counter-Strike"
    max_player = 5
    colour = Colour.from_rgb(255, 255, 255)
    emoji = PartialEmoji.from_str("<:CSGOLogo:1163939309112541185>")
    logo = "cs.png"
    ranks = [('任意', 'Any', '<:cs_unranked:1174865953973088286>'),
             ('白银', 'Silver', '<:cs_silver:1174865952094031962>'),
             ('黄金', 'Gold Nova', '<:cs_gold_nova:1174865949023801396>'),
             ('AK', 'Master Guardian', '<:cs_master_guardian:1174865950865113088>'),
             ('菊花', 'Distinguished Master Guardian', '<:cs_dmg:1174865945970364507>'),
             ('老鹰', 'Legendary Eagle', '<:cs_legendary_eagle:1174865950034624642>'),
             ('小地球', 'Supreme Master First Class', '<:cs_smfc:1174865953176162386>'),
             ('大地球', 'Global Elite', '<:cs_global_elite:1174865947073445978>')]
    modes = [('排位', 'Competitive')]


class Dota(Game):
    channel = config.dota
    name_chn = "DOTA"
    name_eng = "DOTA"
    max_player = 5
    colour = Colour.from_rgb(234, 71, 59)
    emoji = PartialEmoji.from_str("<:Dota2:1113566589590175935>")
    logo = "dota.png"
    ranks = [('任意', 'Any', '<:Dota_Uncalibrated:1174866111469211769>'),
             ('先锋', 'Herald', '<:Dota_Herald:1174866015541276792>'),
             ('卫士', 'Guardian', '<:Dota_Guardian:1174866013746114581>'),
             ('圣骑士', 'Crusader', '<:Dota_Crusader:1174866012311666768>'),
             ('大师', 'Archon', '<:Dota_Archon:1174866010705252464>'),
             ('传奇', 'Legend', '<:Dota_Legend:1174866018334679120>'),
             ('古代', 'Ancient', '<:Dota_Ancient:1174866009765711882>'),
             ('神圣', 'Divine', '<:Dota_Divine:1174866013209243748>'),
             ('不朽', 'Immortal', '<:Dota_Immortal:1174866016589852682>')]
    modes = [('普通', 'Normal'),
             ('排位', 'Ranked'),
             ('快速', 'Turbo')]


class Rainbowsix(Game):
    channel = config.r6
    name_chn = "彩虹六号：围攻"
    name_eng = "Rainbow Six: Siege"
    max_player = 5
    colour = Colour.from_rgb(0, 0, 0)
    emoji = PartialEmoji.from_str("<:Rainbow_six_by_patriotLV:1113566688709967983>")
    logo = "r6.png"
    ranks = [('任意', 'Any'),
             ('紫铜', 'Copper', '<:r6_copper:1174866352251601026>'),
             ('青铜', 'Bronze', '<:r6_bronze:1174866351312080936>'),
             ('白银', 'Silver', '<:r6_silver:1174886623335424060>'),
             ('黄金', 'Gold', '<:r6_gold:1174886620693024789>'),
             ('白金', 'Platinum', '<:r6_plat:1174886621720629248>'),
             ('翡翠', 'Emerald', '<:r6_emerald:1174866355166642217>'),
             ('钻石', 'Diamond', '<:r6_diamond:1174866354021597244>'),
             ('冠军', 'Champion', '<:r6_champion:1174894691255320646>')]
    modes = [('排位', 'Ranked'),
             ('标准', 'Standard'),
             ('快速', 'Quick Match')]
