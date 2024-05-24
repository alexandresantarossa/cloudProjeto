from flask import Flask, render_template, request
from botocore.exceptions import ClientError
import uuid
import boto3
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, template_folder='frontend')

# Configurar boto3 para se conectar ao DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('DynamoDBTable')

@app.route('/', methods=['GET', 'POST'])
def resposta():
    artist = None
    song = None
    album = None
    entradas = []

    if request.method == 'POST':
        artist = request.resposta.get('artist')
        song = request.resposta.get('song')
        album = request.resposta.get('album')

        # Gerar um UUID para o item
        item_id = str(uuid.uuid4())

        # Inserir os dados no DynamoDB
        try:
            table.put_item(
                Item={
                    'id': item_id,
                    'artist': artist,
                    'song': song,
                    'album': album
                }
            )
            logging.info("Dados inseridos com sucesso no DynamoDB")
        except ClientError as e:
            logging.error(e)
            return "Erro ao inserir dados no DynamoDB", 500

    # Recuperar todos os dados do DynamoDB para exibição
    try:
        response = table.scan()
        entradas = response.get('Items', [])
    except ClientError as e:
        logging.error(e)
        return "Erro ao recuperar dados do DynamoDB", 500

    return render_template('site.html', artist=artist, song=song, album=album, entries=entradas)

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
