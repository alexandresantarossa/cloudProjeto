from flask import Flask, render_template, request, redirect, url_for
from botocore.exceptions import ClientError
import uuid
import boto3
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, template_folder='frontend')

# Configurar boto3 para se conectar ao DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('DynamoDBTable')

def ensure_created_at(item):
    """Ensure the item has a createdAt field."""
    if 'createdAt' not in item:
        item['createdAt'] = datetime.now().isoformat()
    return item

@app.route('/', methods=['GET', 'POST'])
def resposta():
    if request.method == 'POST':
        nome = request.form.get('nome')
        artist = request.form.get('artist')
        song = request.form.get('song')
        album = request.form.get('album')

        # Gerar um UUID para o item
        item_id = str(uuid.uuid4())

        # Adicionar campo createdAt com a data e hora atual
        created_at = datetime.now().isoformat()

        # Inserir os dados no DynamoDB
        try:
            table.put_item(
                Item={
                    'id': item_id,
                    'nome': nome,
                    'artist': artist,
                    'song': song,
                    'album': album,
                    'createdAt': created_at
                }
            )
            logging.info("Dados inseridos com sucesso no Banco de Dados")
        except ClientError as e:
            logging.error(e)
            return "Erro ao inserir dados no Banco de Dados", 500

        # Redirecionar para evitar duplicação
        return redirect(url_for('resposta'))

    # Recuperar todos os dados do DynamoDB para exibição
    try:
        response = table.scan()
        entradas = response.get('Items', [])
        # Garantir que todos os itens têm um campo createdAt
        entradas = [ensure_created_at(item) for item in entradas]
        # Atualizar os itens no DynamoDB se necessário
        for item in entradas:
            if 'createdAt' not in item:
                table.put_item(Item=item)
        # Ordenar por createdAt
        entradas.sort(key=lambda x: x['createdAt'])
        # Adicionar numeração às entradas
        for idx, entrada in enumerate(entradas, start=1):
            entrada['num'] = idx
    except ClientError as e:
        logging.error(e)
        return "Erro ao recuperar dados do DynamoDB", 500

    return render_template('site.html', entries=entradas)

@app.route('/debug')
def debug():
    try:
        response = table.scan()
        entradas = response.get('Items', [])
        logging.info("Entradas no DynamoDB:")
        for entrada in entradas:
            logging.info(entrada)
        return "Check the logs for DynamoDB entries."
    except ClientError as e:
        logging.error(e)
        return "Erro ao recuperar dados do Banco de Dados", 500

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
