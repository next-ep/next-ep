# next-ep

# MANUAL DE EXECUÇÃO LOCAL

1. Por boa prática criar virtual environment para o projeto, para isso basta abrir um terminal no diretório do projeto e executar o seguinte comando:
$ python -m venv .venv
2. Em sequência iniciar o ambiente virtual:
  2.1. Se estiver pelo cdc com o comando:
$ .venv\Scripts\activate.bat
  2.2. Caso esteja utilizando o powershell:
$ .venv\Scripts\activate.ps1

3. Com o ambiente virtual iniciado instalar os requirimentos com:
$ pip install -r requirements.txt

4. Com os requirements instalados basta criar o database, para isso basta executar:
$ flask db init
$ flask db migrate -m "Initial migration"
$ flask db upgrade

5. Feito isso basta executar o main.py com:
python main.py 
