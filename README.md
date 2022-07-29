# Bitbucket API Consultant
Esse repositório foi criado para versionar o programa que consulta alguns dados da organização que serão utilizados para a migração do Github.

## Requisitos
python >= 3

## Dependências

1. Criando um [virtualenv](https://www.treinaweb.com.br/blog/criando-ambientes-virtuais-para-projetos-python-com-o-virtualenv) 
```sh
python -m venv venv
source venv/bin/activate
```

2. Instalando as depedências:
```
pip install -r requirements.txt
```

3. Criando a arquivo .env
```
cp .env.sample .env
```

#### Inputs:
| Argument  | Required/Optional  | Descripiton |
| :------------ |:---------------:| :-----:|
| WORKSPACE | Required | Nome do Workspace no Bitbucket (Exemplo: will-bank) |
| TOKEN | Required | Token de acesso para ter interatividade com a API |
| PAGES | Required | Numero de paginas do workspace |
| SYNC | Required | Flag para controlar a execução do programa |

### Token
Para o programa funcionar, precisamos de um Token. Para obter esse Token acesse esse endereço:

- https://bitbucket.org/site/oauth2/authorize?client_id=<CLIEND_ID>&response_type=token
- https://bitbucket.org/site/oauth2/authorize?client_id=<CLIEND_ID>&response_type=code

Quando o endereço for acessado, ele irá te retornar o token na url de resposta.

## Como rodar o programa
Para rodar o programa basta exutar o seguinte comando na raiz:
```sh
make run
charts-cli add-user --first-name "developer" --last-name "experience" --email "developer.experience@willbank.com" --password "willbankdx@2022" --role "UserAdmin"
```
