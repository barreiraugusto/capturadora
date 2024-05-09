import json

from channels.generic.websocket import WebsocketConsumer


class GrabacionConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # Recibe un mensaje desde el cliente
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Realiza cualquier lógica necesaria

        # Envía un mensaje de vuelta al cliente
        self.send(text_data=json.dumps({
            'message': 'Mensaje recibido correctamente'
        }))
