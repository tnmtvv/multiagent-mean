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
    receiveragent = RootAgent("agent1@10.16.252.242", "pass1")
    await receiveragent.start(auto_register=True)
    print("Receiver started")

    senderagent = SmallAgent("agent2@10.16.252.242", "pass2")
    await senderagent.start(auto_register=True)
    print("Sender started")

    await spade.wait_until_finished(receiveragent)
    print("Agents finished")


if __name__ == "__main__":
    spade.run(main())
