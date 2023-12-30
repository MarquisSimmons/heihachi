import json, datetime, logging, os, discord, sched, time, sys
from typing import List

from src.wavu import wavu_importer
from src.module import configurator
from src.module import json_movelist_reader
from src.module import embed
from src.module import util
from src.module import character
from src.resources import const
from src.module import button

from threading import Thread

sys.path.insert(0, (os.path.dirname(os.path.dirname(__file__))))

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

base_path = os.path.dirname(__file__)
CONFIG_PATH = configurator.Configurator(os.path.abspath(os.path.join(base_path, "resources", "config.json")))
CHARACTER_LIST_PATH = os.path.abspath(os.path.join(base_path, "resources", "character_list.json"))

discord_token = CONFIG_PATH.read_config()['DISCORD_TOKEN']
feedback_channel_id = CONFIG_PATH.read_config()['FEEDBACK_CHANNEL_ID']

character_list = []


class heihachi(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=645011181739835397))
            self.synced = True
        print('Logged on as', self.user)


try:
    hei = heihachi(intents=discord.Intents.default())
    tree = discord.app_commands.CommandTree(hei)

except Exception as e:
    time_now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    logger.error(f'{time_now} \n Error: {e}')


def get_frame_data_embed(name: str, move: str) -> discord.Embed:

    character_name = util.correct_character_name(name.lower())
    if character_name:

        character = util.get_character_by_name(character_name, character_list)
        move_list = json_movelist_reader.get_movelist(character_name)
        move_type = util.get_move_type(move)
        if move_type:
            moves = json_movelist_reader.get_by_move_type(move_type, move_list)
            moves_embed = embed.move_list_embed(character, moves, move_type)
            return moves_embed
        else:
            character_move = json_movelist_reader.get_move(move, move_list)
            if character_move:
                move_embed = embed.move_embed(character, character_move)
                return move_embed

            else:
                similar_moves = json_movelist_reader.get_similar_moves(move, move_list)
                similar_moves_embed = embed.similar_moves_embed(similar_moves, character_name)
                return similar_moves_embed
    else:
        error_embed = embed.error_embed(f'Character {name} does not exist.')
        return error_embed
@hei.event
async def on_message(message):

    if not is_author_blacklisted(message.author.id) and message.content and message.author.id != hei.user.id:
        user_command = message.content.split(' ', 1)[1]
        parameters = user_command.strip().split(' ',1)
        character_name = parameters[0].lower()
        character_move = parameters[1]

        embed = get_frame_data_embed(character_name, character_move)
        await message.channel.send(embed=embed)


@tree.command(name="fd", description="Frame data from a character move", guild=discord.Object("645011181739835397"))
async def self(interaction: discord.Interaction, character_name: str, move: str):
    if not (is_author_blacklisted(interaction.user.id) or is_author_newly_created(interaction)):
        embed = get_frame_data_embed(character_name, move)
        await interaction.response.send_message(embed=embed, ephemeral=False)


def is_author_blacklisted(user_id):
    if user_id in const.ID_BLACKLIST:
        return True
    else:
        return False


def is_author_newly_created(interaction):
    today = datetime.datetime.strptime(datetime.datetime.now().isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
    age = today - interaction.user.created_at.replace(tzinfo=None)
    if age.days < 120:
        return True
    return False


@tree.command(name="feedback", description="Send feedback incase of wrong data",
              guild=discord.Object("645011181739835397"))
async def self(interaction: discord.Interaction, message: str):

    if not (is_author_blacklisted(interaction.user.id) or is_author_newly_created(interaction)):
        try:
            feedback_message = "Feedback from **{}** with ID **{}** in **{}** \n- {}\n".format(str(interaction.user.name), interaction.user.id,
                                                         interaction.guild, message)
            channel = hei.get_channel(feedback_channel_id)
            await channel.send(content=feedback_message,view=button.DoneButton())
            result = embed.success_embed("Feedback sent")
        except Exception as e:
            result = embed.error_embed("Feedback couldn't be sent caused by: " + e)

        await interaction.response.send_message(embed=result, ephemeral=True)



def create_json_movelists(character_list_path: str) -> List[character.Character]:
    with open(character_list_path) as file:
        all_characters = json.load(file)
        cha_list = []

        for character_meta in all_characters:
            cha = wavu_importer.import_character(character_meta)
            cha.export_movelist_as_json()
            cha_list.append(cha)

    return cha_list


def schedule_create_json_movelists(character_list_path: str, scheduler):
    try:
        create_json_movelists(character_list_path)
        scheduler.enter(3600, 1, create_json_movelists, (character_list_path, scheduler,))

    except Exception as e:
        raise Exception("Error when importing character from wavu" + str(e))


try:
    character_list = create_json_movelists(CHARACTER_LIST_PATH)
    print("Character jsons are successfully created")
    scheduler = sched.scheduler(time.time, time.sleep)

    # Repeat importing move list of all character from wavu.wiki once an hour
    scheduler.enter(3600, 1, schedule_create_json_movelists, (CHARACTER_LIST_PATH, scheduler,))
    Thread(target=scheduler.run).start()

    hei.run(discord_token)

except Exception as e:
    time_now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    logger.error(f'{time_now} \n Error: {e}')
