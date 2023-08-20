from views import InlineQueryView

__all__ = (
    'ClientConnectorErrorInlineQueryView',
    'ServerAPIErrorInlineQueryView',
)


class ClientConnectorErrorInlineQueryView(InlineQueryView):
    text = '❌ Ошибка подключения к серверу, попробуйте позже'
    title = '❌ Ошибка подключения к серверу'
    thumbnail_url = 'https://i.imgur.com/UrtkjND.jpg'
    thumbnail_width = 100
    thumbnail_height = 100


class ServerAPIErrorInlineQueryView(InlineQueryView):
    text = '❌ Ошибка API сервера, попробуйте позже'
    title = '❌ Ошибка API сервера'
    thumbnail_url = 'https://i.imgur.com/C2KrlBI.jpeg'
    thumbnail_width = 100
    thumbnail_height = 100
