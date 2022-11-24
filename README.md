# Next EP
Se trata de um sistema de controle pessoal de séries. Com ele é possível registrar o progresso de episódios assistidos e ainda deixar comentários.

### Setup local

- Por boa prática criar virtual environment para o projeto, para isso basta abrir um terminal no diretório do projeto e executar o seguinte comando: ``` $ python -m venv .venv ```
- Em sequência iniciar o ambiente virtual:
    - Se estiver executando pelo cmd com o comando: ``` $ .venv\Scripts\activate.bat ```
    - Ou caso esteja utilizando o powershell: ``` $ .venv\Scripts\activate.ps1 ```

-  Com o ambiente virtual iniciado instalar os requirimentos com: ``` $ pip install -r requirements.txt ```

- Setup do banco de dados postgres em Docker
    - Primeiro, é necessário instalar o docker na maquina: https://docs.docker.com/desktop/install/windows-install/
    - Baixar a imagem do postgres com esse comando: ``` docker pull postgres:13.8-alpine ```
    - Executar o container com o comando: ``` docker run --name next-ep-db -e POSTGRES_DB=next-ep -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -p 5432:5432 -d postgres:13.8-alpine ```
    - Neste ponto, o banco está pronto para ser acessado. Para testar, a sugestão de ferramenta é o PgAdmin: https://www.pgadmin.org/
    - Renomei o arquivo .env-example para .env

-  Com os requirements instalados basta criar o database, para isso basta executar:
    ```
    $ flask db init
    $ flask db migrate -m "Initial migration"
    $ flask db upgrade
    ```

- Feito isso basta executar o main.py com: ``` $ python main.py ```