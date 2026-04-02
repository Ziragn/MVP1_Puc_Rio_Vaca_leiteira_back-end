 # Minha API

.Um mini-projeto sobre um cadastro simples de vacas leiteiras. 
.Aqui só se encontra a parte Back-End do projeto (parte frond-end em outro repositório)

> O projeto possui como funcionalidades principais:
- Cadastro de vacas
- Listagem de vacas cadastradas
- Busca de vaca por nome
- Remoção de vaca
- Registro de produção leiteira por data
- Listagem de registros de produção por vaca
- Cálculo da média de produção leiteira

> São duas as entidades principais, sendo estas: Vaca e RegistroProducao
. Vaca: Id, nome, raca
. RegistroProducao: id, data_registro, litros, vaca_id(chave estrangeira da tabela Vaca, relacionamento 1xN)

---
## Como executar 

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas. Obs: o 'requirements_2.txt possui as bibliotecas com suas versões'
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
Passos a serem seguidos, caso você utilize o VsCode:(Para criação do ambiente virtual)
1- py -m venv meu-env (usar no terminal integrado)
2- .\meu-env\Scripts\activate (caso der erro, vá para o passo 3, caso não, ignore.)
3- Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass  e depois .\meu-env\Scripts\Activate.ps1 
4- Caso apareça 'meu-env' de cor verde no terminal, significa que deu tudo certo.

Após já ter criado o ambiente virtual, utilize o seguinte comando para instalar as bibliotecas do requirements.txt:
.pip install -r requirements.txt


Para executar a API  basta executar:
flask run --host 0.0.0.0 --port 5000


Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte: 
flask run --host 0.0.0.0 --port 5000 --reload


Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
