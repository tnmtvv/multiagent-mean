import spade
from spade.agent import Agent
from spade.template import Template
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
import random
import ast

STATE_ONE = "STATE_ONE"
STATE_TWO = "STATE_TWO"
STATE_THREE = "STATE_THREE"
STATE_FOUR = "STATE_FOUR"
STATE_FIN = "STATE_FIN"


class MyFSMBehaviour(FSMBehaviour):
    async def on_start(self):
        print(f"FSM starting at initial state {self.current_state}")

    async def on_end(self):
        print(f"FSM finished at state {self.current_state}")
        await self.agent.stop()

    #     # await self.agent.stop()


class StateOne(State):
    async def run(self):
        # print("STATE1")
        already_used = []
        for (
            key,
            neighbour,
        ) in self.agent.neighbours.items():
            if key not in already_used:
                new_msg = None
                msg = Message(to=neighbour)
                msg.set_metadata("performative", "inform")
                msg.body = str(self.agent.all_info)
                for _ in range(5):
                    try:
                        await self.send(msg)
                    except:
                        pass
                    print("Message sent!")
                    try:
                        new_msg = await self.receive(timeout=5)
                    except:
                        pass
                    if new_msg:
                        if new_msg.body == "Delivered":
                            # print(f"Message from {self.agent.myId} to {key} delivered")
                            already_used.append(key)
                            break
                        else:
                            for item in ast.literal_eval(new_msg.body).items():
                                if (
                                    item[0] not in self.agent.all_info.keys()
                                ):  # если информация новая, обновляем таблицу
                                    print(
                                        f"Обновили таблицу {self.agent.myId} элементом {item[0]}"
                                    )
                                    self.agent.all_info.update(
                                        ast.literal_eval(new_msg.body)
                                    )
                            break
        if self.agent.leaf:
            self.set_next_state(STATE_FIN)
        else:
            self.set_next_state(STATE_THREE)


class StateTwo(State):
    async def run(self):
        # print("jkjhlkj;l")
        print("-------------------------------")
        print(f"agent {self.agent.myId}")
        print(self.agent.all_info)
        print(f"mean: {sum(self.agent.all_info.values()) / len(self.agent.all_info)}")
        print("-------------------------------")
        self.set_next_state(STATE_FIN)


class StateFour(State):
    async def run(self):
        if_new_info = False

        msg = None
        try:
            msg = await self.receive(timeout=40)  # wait for a message for 10 seconds
        except:
            pass
        if msg:
            new_msg = Message(to=str(msg.sender))
            new_msg.set_metadata("performative", "inform")
            new_msg.body = str(self.agent.all_info)
            await self.send(new_msg)
            for item in ast.literal_eval(msg.body).items():
                if (
                    item[0] not in self.agent.all_info.keys()
                ):  # если информация новая, обновляем таблицу
                    print(f"Обновили таблицу {self.agent.myId} элементом {item[0]}")
                    if item[0] > self.agent.myId:
                        self.agent.is_root = False
                    print("item in final node: ")
                    print(item)
                    self.agent.all_info.update(ast.literal_eval(msg.body))
                    if_new_info = True
            if if_new_info:
                self.set_next_state(STATE_FOUR)
            else:
                self.set_next_state(STATE_FOUR)
        else:
            if self.agent.is_root:
                self.set_next_state(STATE_TWO)
            else:
                self.set_next_state(STATE_FIN)


class StateThree(State):
    async def run(self):
        print(f"RecvBehav running {self.agent.myId}")
        if_new_info = False
        msg = None
        try:
            # print("succsess1")
            msg = await self.receive(timeout=15)
            # print(f"succsess2 agent {self.agent.myId}")
        except:
            pass

        if msg and self.agent.countNotActual < 5:
            print("Message recieved!")
            new_msg = Message(to=str(msg.sender))
            new_msg.set_metadata("performative", "inform")
            new_msg.body = "Delivered"
            await self.send(new_msg)
            for item in ast.literal_eval(msg.body).items():
                print("item: ")
                print(item)
                if (
                    item[0] not in self.agent.all_info.keys()
                ):  # если информация новая, обновляем таблицу
                    print(f"Обновили таблицу {self.agent.myId} элементом {item[0]}")
                    self.agent.all_info.update(ast.literal_eval(msg.body))
                    if_new_info = True
            if if_new_info:
                self.set_next_state(STATE_ONE)
            else:
                self.set_next_state(
                    STATE_THREE
                )  # если информация получена, но она не актуальна, слушаем дальше
                self.agent.countNotActual += 1
                print(f"not actual {self.agent.myId}: {self.agent.countNotActual}")
        else:
            self.set_next_state(STATE_FIN)


class Final(State):
    async def run(self):
        # print(f"final state {self.agent.myId}")
        pass


class AdvancedAgent(Agent):
    def __init__(self, name, password, id, neighbours_ids=[]):
        super().__init__(name, password)
        self.myId = id
        self.myNum = random.randint(0, 100)
        self.all_info = {id: self.myNum}
        print(self.all_info)
        self.neighbours, self.leaf = self.make_neighbours_dict(neighbours_ids, id)
        self.modifications_check = 0
        self.countNotActual = 0
        self.is_root = False

    def make_neighbours_dict(self, indx, self_id):
        neighbours = {}
        leaf = True
        for i in indx:
            if i > self_id:
                neighbours.update(
                    {i: f"agent{i}@localhost"}
                )  # храним только соседей с бОльшим индексом
                leaf = False
        return neighbours, leaf

    async def setup(self):
        template = Template()
        template.set_metadata("performative", "inform")
        fsm = MyFSMBehaviour()
        if len(self.neighbours) > 0:
            fsm.add_state(name=STATE_ONE, state=StateOne(), initial=True)
            fsm.add_state(name=STATE_THREE, state=StateThree())
            fsm.add_state(name=STATE_FIN, state=Final())

            fsm.add_transition(source=STATE_ONE, dest=STATE_THREE)
            fsm.add_transition(source=STATE_THREE, dest=STATE_ONE)
            fsm.add_transition(source=STATE_THREE, dest=STATE_THREE)
            fsm.add_transition(source=STATE_THREE, dest=STATE_FIN)
            fsm.add_transition(source=STATE_ONE, dest=STATE_FIN)

        else:
            self.is_root = True
            fsm.add_state(name=STATE_TWO, state=StateTwo())
            fsm.add_state(name=STATE_FOUR, state=StateFour(), initial=True)
            fsm.add_state(name=STATE_FIN, state=Final())

            fsm.add_transition(source=STATE_FOUR, dest=STATE_TWO)
            fsm.add_transition(source=STATE_FOUR, dest=STATE_FOUR)
            fsm.add_transition(source=STATE_TWO, dest=STATE_FIN)
            fsm.add_transition(source=STATE_FOUR, dest=STATE_FIN)
        self.add_behaviour(fsm, template)
