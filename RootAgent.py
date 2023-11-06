from spade.agent import Agent

import getpass
import ast
import asyncio

import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template


class RootAgent(Agent):
    def __init__(self, name, password, numSmallAgents):
        super().__init__(name, password)
        self.my_name = name
        self.all_info = {}
        self.num_small_agents = numSmallAgents

    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("RecvBehav running")

            msg = await self.receive(timeout=2)  # wait for a message for 10 seconds
            if msg:
                print("here")
                self.agent.all_info.update(ast.literal_eval(msg.body))
            if len(self.agent.all_info) == self.agent.num_small_agents:
                print(
                    f"mean: {sum(self.agent.all_info.values()) / self.agent.num_small_agents}"
                )
                self.kill()

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)
