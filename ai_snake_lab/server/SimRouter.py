"""
ai_snake_lab/server/SimRouter.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

import asyncio
import zmq
import zmq.asyncio

from ai_snake_lab.constants.DSim import DSim
from ai_snake_lab.constants.DMQ import DMQ, DMQ_Label


class SimRouter:
    """Pure MQ router between TUIs and the Simulation Server."""

    def __init__(self):

        # Initialize ZMQ context
        self.ctx = zmq.asyncio.Context()

        # Create a ROUTER socket to manage multiple clients
        self.socket = self.ctx.socket(zmq.ROUTER)
        # TODO replace localhost with actual host
        host = DSim.HOST
        mq_port = DSim.MQ_PORT
        protocol = DSim.PROTOCOL
        sim_service = f"{protocol}://{host}:{mq_port}"
        try:
            self.socket.bind(sim_service)
        except zmq.error.ZMQError as e:
            print(f"Failed to bind router to {sim_service}: {e}")
            raise
        print(DMQ_Label.STARTUP_MSG % sim_service)

        self.clients = {}  # i.e. {identity: "SimClient" or "SimServer"}

    async def handle_requests(self):
        """Continuously route messages between SimClients and the SimServer."""
        count = 0
        while True:
            try:
                # ROUTER sockets prepend an identity frame
                frames = await self.socket.recv_multipart()
                identity = frames[0]
                msg_bytes = frames[1]

                if len(frames) != 2:
                    print(f"{DMQ_Label.MALFORMED_MESSAGE}: {frames}")
                    continue

                msg = zmq.utils.jsonapi.loads(msg_bytes)

            except asyncio.CancelledError:
                print("SimRouter shutting down...")
                break

            except KeyboardInterrupt:
                print(DMQ_Label.SHUTDOWN_MSG)
                break

            except zmq.ZMQError as e:
                print(f"ZMQ error in router: {e}")
                await asyncio.sleep(0.1)
                continue

            except Exception as e:
                print(DMQ_Label.ROUTER_ERROR % e)
                continue

            # Parse message
            sender_type = msg.get(DMQ.SENDER)  # SimClient or SimServer
            elem = msg.get(DMQ.ELEM)
            data = msg.get(DMQ.DATA, {})

            print(f"{count} MQ Message: {msg}")
            count += 1

            # Validate message
            if not sender_type or elem is None:
                print(f"{DMQ_Label.MALFORMED_MESSAGE}: {msg}")
                continue

            # Register/refresh sender identity
            if elem == DMQ.REGISTER:
                self.register_client(identity, sender_type)
                continue

            # Route logic
            if sender_type == DMQ.SIM_CLIENT:
                # Forward TUI commands to the SimServer
                await self.forward_to_simserver(elem=elem, data=data, sender=identity)

            elif sender_type == DMQ.SIM_SERVER:
                # DON'T broadcast STATUS or ERROR messages
                if elem not in (DMQ.STATUS, DMQ.ERROR):
                    # Broadcast simulation state to all TUIs
                    await self.broadcast_to_simclients(
                        elem=elem, data=data, sender=identity
                    )

            else:
                print(f"{DMQ_Label.UNKNOWN_SENDER}: {sender_type}")

    async def forward_to_simserver(self, elem, data, sender):
        """Forward TUI command to the simulation server."""

        # Find all connected SimServers
        sim_identities = [
            id for id, typ in self.clients.items() if typ == DMQ.SIM_SERVER
        ]

        # No SimServer connected - inform the client
        if not sim_identities:
            await self.socket.send_multipart(
                [
                    sender,
                    zmq.utils.jsonapi.dumps(
                        {DMQ.ERROR: DMQ_Label.NO_SIMSERVER_CONNECTED}
                    ),
                ]
            )
            return

        # Construct atomic message
        msg = {DMQ.SENDER: DMQ.SIM_CLIENT, DMQ.ELEM: elem, DMQ.DATA: data}
        msg_bytes = zmq.utils.jsonapi.dumps(msg)

        # Send message to all connected SimServers
        for sim_id in sim_identities:
            await self.socket.send_multipart([sim_id, msg_bytes])

        # Acknowledge sender (SimClient)
        await self.socket.send_multipart(
            [
                sender,
                zmq.utils.jsonapi.dumps({DMQ.STATUS: DMQ.OK}),
            ]
        )

    async def broadcast_to_simclients(self, elem, data, sender):
        """Broadcast simulation updates (from SimServer) to all connected TUIs."""

        client_ids = [id for id, typ in self.clients.items() if typ == DMQ.SIM_CLIENT]

        # Nothing to do, just return
        if not client_ids:
            return

        msg = {DMQ.SENDER: DMQ.SIM_SERVER, DMQ.ELEM: elem, DMQ.DATA: data}
        msg_bytes = zmq.utils.jsonapi.dumps(msg)

        for client_id in client_ids:
            if client_id != sender:
                await self.socket.send_multipart([client_id, msg_bytes])

    def register_client(self, identity, role):
        identity_str = identity.decode()
        print(f"New client registered: {role} ({identity_str})")
        self.clients[identity] = role


async def main():
    router = SimRouter()
    await router.handle_requests()


if __name__ == "__main__":
    asyncio.run(main())
