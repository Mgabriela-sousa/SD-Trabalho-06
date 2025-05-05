import pika
import time
import random

def conectar():
    credenciais = pika.PlainCredentials('user', 'password')#credenciais
    parametros = pika.ConnectionParameters(host='rabbitmq', credentials=credenciais)
    while True:
        try:
            conexao = pika.BlockingConnection(parametros)#tenta se conectar com o rabbit
            return conexao
        except pika.exceptions.AMQPConnectionError:
            print("Aguardando o RabbitMQ iniciar...")
            time.sleep(3)# se ele ainda não estiver pronto espera 3 segundos

def gerar_mensagem():#simula a geração da imagem
    tipos = ["rosto", "time"]
    tipo = random.choice(tipos)#escolhe aleatoria entre rosto e time
    imagem = f"imagem_de_{tipo}"
    return tipo, imagem

conexao = conectar()#chama a função de se conectar com o rabbit
canal = conexao.channel()#cria canal de comunicação
canal.exchange_declare(exchange='imagens', exchange_type='topic')

while True:
    tipo, imagem = gerar_mensagem()#gera nova imagem
    canal.basic_publish(#publica img com a chave igual o tipo
        exchange='imagens',
        routing_key=tipo,
        body=imagem
    )
    print(f"Enviado: {imagem} como {tipo}")
    time.sleep(0.2)#espera 2 segundo para enviar a proxima
