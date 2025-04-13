from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, chat_id: int, user_id: int, websocket: WebSocket):
        """Подключение пользователя к чату"""
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)
        await websocket.accept()

    def disconnect(self, chat_id: int, user_id: int):
        """Отключение пользователя от чата"""
        if chat_id in self.active_connections:
            self.active_connections[chat_id] = [
                ws for ws in self.active_connections[chat_id] if ws.client != user_id
            ]

    async def broadcast(self, chat_id: int, message: str):
        """Отправка сообщения всем подключённым пользователям в чате"""
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                await connection.send_text(message)

    async def send_personal_message(self, websocket: WebSocket, message: str):
        """Отправка личного сообщения"""
        await websocket.send_text(message)


manager = ConnectionManager()
