# Relatório do Projeto de Cloud 24-1

**Aluno: Alexandre Rodrigues Santarossa**

# Introdução

Com o objetivo de implementar uma infraestrutura utilizando um código de CloudFormation, utilizamos a AWS juntamente com uma Aplicação de Load Balancer, um Banco de Dados DynamoDB e instâncias EC2. Deste modo, por meio de uma pilha que é criada com base nas minhas especificações definidas no código, foi criado o insper.FM.

# Componentes

**- Application Load Balancer**</p>
    - É usado para distribuir o tráfego entre as instâncias EC2, configurado para utilizar a porta 80 e protocolo HTTP
        
**- EC2 utilizando Auto Scaling Group**</p>
    - É usado para lançar as configurações das instâncias que estão definidas no código, utilizando:</p>
        - Regiões us-east-1a e us-east-2a </p>
        - Instância t1.micro </p>
        - Imagem ami-0e001c9271cf7f3b9 </p>

**- Banco de Dados DynamoDB**</p>
    - É usado para armazenar e mostrar ao usuário as informações adicionadas pelo mesmo, e por meio da configuração do Security Group, garante a conexão entre as instâncias EC2 e o Banco de Dados

# Execução

***É necessário a instalação do AWS CLI*** </p>
***Altere os valores abaixo conforme a necessidade do seu uso*** </p>
*- Gerar Key-Pair*
```bash
aws ec2 create-key-pair --key-name <NomeDaSuaChave> --query 'KeyMaterial' --output text > <NomeDaSuaChave>.pem
```
*- Criar a pilha com CloudFormation*
```bash
aws cloudformation create-stack --stack-name minha-pilha --template-body file://config.yaml --parameters ParameterKey=KeyName,ParameterValue=<NomeDaSuaChave> --capabilities CAPABILITY_IAM
```

*Caso o caminho não funcione, utilize o caminho completo*

# Custos

## Segue o gráfico dos custos atuais e da previsão para o meu projeto

![alt text](/imgs/image.png)

# Link para o repositório
## https://github.com/alexandresantarossa/cloudProjeto