import copy

from nbt import nbt

from utils import *
from .baseCommand import BaseCommand
from .commandCache import CommandCache


class SynchronizeCommand(BaseCommand):
    command_text = "!!synchronize"

    def __init__(self, client, command_cache, data_folder, stat_folder):
        super().__init__(client, command_cache)

        self.data_folder = data_folder
        self.stat_folder = stat_folder

    def help(self):
        return '`' + self.command_text + '`  **-**  Synchronizes stats and scoreboards`[A]`\n'

    async def process(self, message, args):
        async with CommandCache.semaphore:
            if str(message.author.id) in self.cache.admin_list:
                # removes entries that store namehistory usernames
                nbtfile = nbt.NBTFile(os.path.join(self.data_folder, 'scoreboard.dat'))

                for uuid in self.cache.uuids:
                    history = get_name_history(uuid)
                    for i, tag in zip(range(len(nbtfile['data']['PlayerScores']) - 1, -1, -1),
                                      reversed(nbtfile['data']['PlayerScores'])):
                        if any(d['name'] == str(tag['Name']) for d in history):
                            if any(char.isdigit() for char in tag['Objective'].value):
                                temp_tag = copy.deepcopy(tag)
                                temp_tag['Name'].value = self.cache.names[self.cache.uuids.index(uuid)]
                                for j, tag2 in zip(range(len(nbtfile['data']['PlayerScores']) - 1, -1, -1),
                                                   reversed(nbtfile['data']['PlayerScores'])):
                                    if tag2['Objective'].value == temp_tag['Objective'].value and tag2['Name'].value == \
                                            temp_tag['Name'].value:
                                        nbtfile['data']['PlayerScores'][j]['Score'].value += tag['Score'].value
                            else:
                                del nbtfile['data']['PlayerScores'][i]

                nbtfile.write_file(os.path.join(self.data_folder, 'scoreboard.dat'))

                # updates all playerscores to stat value if objective does not contain a number
                nbtfile = nbt.NBTFile(os.path.join(self.data_folder, 'scoreboard.dat'))

                for i, tag in zip(range(len(nbtfile['data']['PlayerScores']) - 1, -1, -1),
                                  reversed(nbtfile['data']['PlayerScores'])):
                    for objective in nbtfile['data']['Objectives']:
                        if tag['Objective'].value == objective['DisplayName'].value and not any(
                                char.isdigit() for char in objective['DisplayName'].value):
                            try:
                                uuid = self.cache.uuids[self.cache.names.index(tag['Name'].value)]
                                with open(os.path.join(self.stat_folder, convert_uuid(uuid) + '.json')) as json_data:
                                    stats = json.load(json_data)
                                nbtfile['data']['PlayerScores'][i]['Score'].value = stats[
                                    objective['CriteriaName'].value]
                            except:
                                pass

                nbtfile.write_file(os.path.join(self.data_folder, 'scoreboard.dat'))

                await message.channel.send('Scoreboard and Statistics are now synchronized')
            else:
                await message.channel.send('You dont have permissions to do that!')
