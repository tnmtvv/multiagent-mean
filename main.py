from spade.agent import Agent

import getpass
import asyncio

import spade

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from RootAgent import RootAgent
from SmallAgent import SmallAgent

from spade.container import Container
from spade.agent import Agent


async def main():
    num_agents = int(input("input number of agents: "))

    receiveragent = RootAgent("agent1@localhost", "pass1", numSmallAgents=num_agents)
    await receiveragent.start(auto_register=True)
    print("Receiver started")

    for i in range(2, num_agents + 2):
        senderagent = SmallAgent(f"agent{i}@localhost", f"pass{i}", id=i)
        await senderagent.start(auto_register=True)
        print(f"Sender {i} started")

    await spade.wait_until_finished(receiveragent)
    print("Agents finished")


if __name__ == "__main__":
    spade.run(main())
