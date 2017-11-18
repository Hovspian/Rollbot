from Managers.data_manager import SessionDataManager


class SlotMachineBot:
    def __init__(self, bot, data_manager: SessionDataManager):
        self.bot = bot
        self.data_manager = data_manager

    async def play_slots(self, slot_machine):
        slot_machine.play_slot()
        self.save_payout(slot_machine)
        await self.announce_report(slot_machine)

    async def announce_report(self, slot_machine):
        host_name = slot_machine.get_host_name()
        report = '\n'.join([f"{host_name}'s slot results",
                            slot_machine.get_outcome_report()])
        await self.bot.say(slot_machine.draw_slot_interface())
        await self.bot.say(report)

    def save_payout(self, slot_machine):
        user = slot_machine.get_host()
        gold_amount = slot_machine.get_payout_amount()
        self.data_manager.update_gold(user, gold_amount)