from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
import random


class SmallAgent(Agent):
    def __init__(self, name, password, id):
        super.__init__(name, password)
        myId = id
        myNum = self.generateNumber()

    def generateNumber():
        return random.randint(0, 100)

    def packageData(self, data=[]):
        data.append((self.myId, self.myNum))
        return data

    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="agent1@10.16.252.242")  # Instantiate the message
            msg.set_metadata(
                "performative", "inform"
            )  # Set the "inform" FIPA performative
            msg.body = "Hello World"  # Set the message content

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("SenderAgent started")
        b = self.InformBehav()
        self.add_behaviour(b)
