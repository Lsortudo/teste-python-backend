# Desafio Técnico - Desenvolvedor Backend _PT_

### Desafio
Você deve desenvolver um sistema que ofereça uma conexão via WebSocket para clientes, com funcionalidades específicas de envio de dados, processamento de algoritmos e gestão de clientes conectados.

### Requisitos
Desenvolver um client WebSocket;  
Desenvolver um server WebSocket que aceite multiplos clients;  
Data atual no servidor para enviar aos clientes conectados a data e hora atual, a cada segundo;  
Salvar em um banco de dados todos os usuários ATUALMENTE conectados ao sistema;  
Atualizar o banco sempre que um cliente conectar/desconectar;  
CMD via WebSocket pra algoritmos de Fibonacci;  
Cliente envia um value e o resultado do calculo de Fibonacci deve retornar SOMENTE ao cliente que fez a solicitacao;  
Dockerfile;  
Docker compose para multiplos servicos, tais como: app, banco.
### Tecnologias obrigatórias
- Python
- WebSocket
- Async fw e libs que suportem operações assíncronas
- Banco de Dados: Qualquer sistema de banco de dados relacional ou não relacional (ex: PostgreSQL, SQL Server, MongoDB, Redis)
- Dockerfile, Docker compose
- Audio explicando o codigo e decisoes

#### Formato de entrega
O projeto deve ser enviado ao email que enviou o teste técnico, enviar como um link para o repositório no Github;  
Readme com instrucoes para rodar o projeto;  
Aúdio explicativo no email que enviou o teste técnico;  

## Minha solucao

## Para utilizacao em Local

**Antes de executar Server/Client entre na pasta app**
```bash
cd .\app\
```
**Instale as dependencias**
```bash
pip install -r requirements.txt
```
#### Exemplo da execucao do Server
```bash
env:WS_HOST="localhost"  
env:WS_PORT="8080"  
env:DB_USER="postgres"  
env:DB_PASSWORD=12345  
env:DB_DATABASE="websocketdb"  
env:DB_HOST="localhost:8089"  
python server.py  
```
#### Exemplo da execucao do Client
```bash
env:USER="42"  
env:WS = 'ws://localhost:8080'  
env:SKIP_USER_INPUT = "true"  
python client.py  
```
#### Variaveis de ambiente
**WS_HOST** - Endereço do host onde o servidor WebSocket irá rodar (normalmente localhost em desenvolvimento)  
**WS_PORT** - Porta na qual o servidor WebSocket irá escutar as conexões  
**DB_USER** -   Nome de usuário para conexão com o banco de dados PostgreSQL  
**DB_PASSWORD** - Senha para conexão com o banco de dados PostgreSQL  
**DB_DATABASE** - Nome do banco de dados que será utilizado  
**DB_HOST** - Endereço e porta do servidor de banco de dados (formato host:port)  
**USER** - Identificador para simular o ID de um usuário. Numa aplicação em produção, este valor deveria vir de um processo de autenticação, mas para este exemplo foi colocado em uma variável de ambiente para cada cliente"  
**WS** - URL completa do WebSocket server (formato ws://host:port)  
**SKIP_USER_INPUT** - Booleano que retorna true ou false, true é pra rodar a aplicacao fazendo skip do userInput, que iria apenas receber o broadcast da data/hora atual. Já false habilita os dois, o broadcast de data/hora, e também aceita numeros pra prosseguir com a equacao de Fibonacci.
### Para utilizacao com o Docker

## Proximas melhorias
#### Melhoria no Readme
#### Refatoracao  
#### Testes  
#### Front basico para a sequencia de Fibo  