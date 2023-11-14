from spade.agent import Agent

import spade

from AdvancedAgent import AdvancedAgent

topology = {1: [2, 4], 2: [3], 3: [4, 5], 4: [1, 3], 5: [3]}
# topology = {1: [2], 2: [1]}


async def main():
    num_agents = int(input("input number of agents: "))

    agents = []
    for i in range(1, num_agents + 1):
        agents.append(
            AdvancedAgent(
                f"agent{i}@localhost", f"pass{i}", id=i, neighbours_ids=topology[i]
            )
        )

    for i in range(len(agents)):
        await agents[-(i + 1)].start(auto_register=True)

    for i in range(len(agents)):
        await spade.wait_until_finished(agents[i])

    for i in range(len(agents)):
        await agents[i].stop()

    print("Agents finished")


if __name__ == "__main__":
    spade.run(main())
