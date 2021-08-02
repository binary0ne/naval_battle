from django.shortcuts import render
from django.views.generic.base import TemplateView
from datetime import datetime
import asyncio

CONNECTED_SOCKETS = {}


def create_or_skip_chat(chat_id):
    if chat_id in CONNECTED_SOCKETS.keys():
        return
    else:
        CONNECTED_SOCKETS[chat_id] = []


def index_view(request, chat_id='general'):
    create_or_skip_chat(chat_id)
    context = {'chat_id': chat_id}
    return render(request, "index.html", context)


async def websocket_view(socket, chat_id='general'):
    await socket.accept()
    CONNECTED_SOCKETS[chat_id].append(socket)
    while True:
        try:
            message = await socket.receive_json()
        except AssertionError:
            await socket.close()
            print('Socket was closed')
            CONNECTED_SOCKETS[chat_id].remove(socket)
            break
        if message['message'] != '':
            message['timestamp'] = str(datetime.now())
            for connected_socket in CONNECTED_SOCKETS[chat_id]:
                await connected_socket.send_json(message)
