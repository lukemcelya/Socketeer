import json
from channels.generic.websocket import AsyncWebsocketConsumer

connected_clients = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.username = f"Guest{len(connected_clients) + 1}"  # Assign default username
        connected_clients[self] = self.username  # Store client connection

        # Notify all users when someone joins
        await self.broadcast_message(f"{self.username} joined the chat!", system=True)

    async def disconnect(self, close_code):
        username = connected_clients.pop(self, "Unknown User")
        await self.broadcast_message(f"{username} left the chat.", system=True)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if "username" in data:
            # Update username
            old_username = self.username
            self.username = data["username"]
            connected_clients[self] = self.username
            await self.broadcast_message(f"{old_username} changed their name to {self.username}", system=True)
        else:
            # Broadcast user message
            message = data["message"]
            await self.broadcast_message(f"{self.username}: {message}")

    async def broadcast_message(self, message, system=False):
        for client in connected_clients:
            await client.send(text_data=json.dumps({
                "message": message,
                "system": system
            }))
