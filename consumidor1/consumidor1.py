import pika
import time
import random

def conectar():
    credenciais = pika.PlainCredentials('user', 'password')
    parametros = pika.ConnectionParameters(host='rabbitmq', credentials=credenciais)
    while True:
        try:
            conexao = pika.BlockingConnection(parametros)
            return conexao
        except pika.exceptions.AMQPConnectionError:
            print("Aguardando o RabbitMQ iniciar...")
            time.sleep(3)

def analisar_rosto(imagem):
    return random.choice(["Feliz", "Triste"])

def callback(ch, method, properties, body):
    resultado = analisar_rosto(body)
    print(f"Imagem recebida (rosto): {body.decode()}. Resultado: {resultado}")
    time.sleep(4)  # IA lenta para simular fila enchendo
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirmar manualmente o processamento da mensagem

conexao = conectar()
canal = conexao.channel()

# EXCHANGE FIXA
canal.exchange_declare(exchange='imagens', exchange_type='topic')

# FILA FIXA
nome_fila = 'fila_face'
canal.queue_declare(queue=nome_fila)

# BIND FIXO
canal.queue_bind(exchange='imagens', queue=nome_fila, routing_key='rosto')

# CONSUMO
canal.basic_consume(queue=nome_fila, on_message_callback=callback, auto_ack=False)

print('Consumidor de rostos aguardando mensagens...')
canal.start_consuming()
