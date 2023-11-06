from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
import random


class SmallAgent(Agent):
    def __init__(self, name, password, id):
        super().__init__(name, password)
        self.myId = id
        self.myNum = random.randint(0, 100)
        self.all_my_info = {id: self.myNum}

    def packageData(self, data=[]):
        data.append((self.myId, self.myNum))
        return data

    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            print(str(self.agent.myId) + ": " + str(self.agent.myNum))
            msg = Message(to="agent1@localhost")  # Instantiate the message
            msg.set_metadata(
                "performative", "inform"
            )  # Set the "inform" FIPA performative
            msg.body = str(self.agent.all_my_info)  # Set the message content

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        b = self.InformBehav()
        self.add_behaviour(b)
