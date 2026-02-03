from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.message_service import MessageService
from ..repositories.chat_repository import ChatRepository
from ..auth import utils
import json

router = APIRouter(prefix="/api/ws", tags=["websockets"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_id: int):
        if chat_id in self.active_connections:
            self.active_connections[chat_id].remove(websocket)
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def broadcast(self, message: dict, chat_id: int):
        for connection in self.active_connections.get(chat_id, []):
            await connection.send_text(json.dumps(message))


manager = ConnectionManager()


@router.websocket("/chat/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: int,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    try:
        payload = utils.decode_jwt(token)
        user_id = payload.get("id")
        if not user_id:
            raise ValueError("No user id in token")
        repository = ChatRepository(db)
        repository.is_user_in_chat(user_id=user_id, chat_id=chat_id)

    except Exception as e:
        print("WS AUTH ERROR:", e)
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, chat_id)
    try:
        while True:
            data = await websocket.receive_text()
            if not data.strip():
                continue
            message = {
                "text": data,
                "chat_id": chat_id,
                "sender_id": user_id,
            }
            service = MessageService(db)
            service.create_message(chat_id=chat_id, text=data, user_id=user_id)
            await manager.broadcast(message, chat_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)


@router.websocket("/test")
async def ws_test(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"echo: {data}")
