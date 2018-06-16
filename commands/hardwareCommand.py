from .baseCommand import BaseCommand

import psutil

class HardwareCommand(BaseCommand):
    command_text = "!!hardware"

    def __init__(self, discord, client, message, command_cache):
        super().__init__(discord, client, message, command_cache)

    def help(self):
        return '`' + self.command_text + '`  **-**  Displays currently used hardware recources\n'

    async def process(self, args):
        if self.client == None:
            print('The current CPU usage is: **' + str(psutil.cpu_percent(interval=0.5)) + '%**\nThe current RAM usage is: **' + str(round(psutil.virtual_memory()[3] / 1073741824, 2)) + 'GB** ')
        else:
            await self.client.send_message(self.message.channel, 'The current CPU usage is: **' + str(psutil.cpu_percent(interval=0.5)) + '%**\nThe current RAM usage is: **' + str(round(psutil.virtual_memory()[3] / 1073741824, 2)) + 'GB** ')
