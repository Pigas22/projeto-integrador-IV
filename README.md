## 📒 Sobre o Projeto:
A idealização do projeto foi proposta pelo professor [_Howard Roatti_](https://www.linkedin.com/in/howardroatti/) como uma avaliação durante a matéria, *`Projeto Integrador IV`* no 6° período do curso Sistemas de Informação no Centro Universitário, FAESA.

### 📚 Objetivo do Projeto: 
Desenvolver um chatbot impulsionado pela IA do Google, Gemini, onde o agente será utilizado para marcar consultas, consultar informações básicas e realizar uma pré-triagem do paciente, evitando, é claro, diagnósticos exagerados.

### 🛠️ Tecnologias e Ferramentas utilizadas no Projeto:
<div align="center">

![Python](https://img.shields.io/badge/Python-blue.svg?style=for-the-badge&logo=python&logoColor=yellow)
![SQLite](https://img.shields.io/badge/SQLITE-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-white?style=for-the-badge&logo=flask&logoColor=3BABC3)
![Gemini](https://img.shields.io/badge/Gemini-white?style=for-the-badge&logo=googlegemini)
![Git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white) 
![Vscode](https://img.shields.io/badge/Vscode-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)

</div>

## ❓ Como Rodar o Projeto:
Para configurar e inicilizar a aplicação de maneira correta, basta seguir os seguintes passos:

Clone o repositório nas pasta que desejar:
```cmd
cmd
git clone https://github.com/Pigas22/projeto-integrador-IV.git
```

Depois de clonado, será necessário abrir o terminar na pasta raiz do projeto, no caso deste exemplo:
```cmd
cmd
H:\projeto-integrador-IV>
```

<div style="
    border: 2px dashed #555;
    background-color: rgba(0, 0, 0, 0.05);
    padding: 12px;
    border-radius: 8px;
    width: 75%;
    margin: 15px auto;
    text-align: center;
    font-style: italic;
">
    <h4 style="margin: 0;">
        ⚠️ Obs.: As configurações abaixo podem não funcionar corretamente em todos os sistemas operacionais, pois foram feitas pensando no <code>Windows</code>.
    </h4>
</div>

Agora, execute o arquivo BAT (.bat), nomeado como [**initiate.bat**](https://github.com/Pigas22/projeto-integrador-IV/blob/main/initiate.bat), o qual irá confirar todo o ambiente e baixar as dependências. Durante a execução desse arquivo, será criado o arquivo `.env`, caso não exista, e o BAT irá solicitar sua chave de acesso à API do GEMINI, a qual deve ser informada no arquivo recém-criado (.env).

Caso ainda não tenha uma chave da API do Gemini, é necessário que logue com sua conta Google no seguinte site: _*<a href="https://aistudio.google.com/">https://aistudio.google.com/</a>*_ , navegar pelo fluxo : `Dashboard > Chaves de API`, será nessa tela que nossa chave ficará registrada, e clicar no botão no canto superior direito, chamado: `"Criar chave de API"`.

Feito isso, o site solicitará 2 informações, **`Nome da Chave`** e um **`Projeto`**, o nome é de escolha totalmente pessoal e, o projeto, caso não tenha, basta criar um através do próprio _dropdown_ do campo. Assim que informados ambos os campos, proseguir clicando em `Criar chave`, por último, basta copiar o token da chave criada e substituir a informação no arquivo `.env`. De modo que fique assim:
```python
.env
GEMINI_API_KEY="AIzaSyN9vK....H7uC1a" 
```

Dessa forma, caso todas as configurações tenham sido realizadas da maneira correta, basta abrir o link localhost em que o sistema está hospedado:
_*<a href="http://localhost:3050/">http://localhost:3050/</a>*_

<div>
<pre style="margin-left:auto; margin-right:auto; padding:15px; border-radius:10px; height:fit-content; width: fit-content;">
🥳 Pronto!!! Agora, a aplicação está configurada e pronta para ser utilizada. 🚀
</pre>
</div>

## Estrutura Básica do projeto:
```
PROJETO-INTEGRADOR-IV
├───.venv
│   └───Arquivos do Ambiente Virtual Python
├───docs
│   └───Arquivos complementares para orientação do projeto (PDF's e Docs)
├───project
│   ├───backend
│   │   └───Arquivos .py contendo conexão com banco e classes models
│   ├───static
│   │   └───Arquivos CSS (.css) e JavaScript (.js)
│   ├───tamplates
│   │    └───Arquivos HTML (.html)
│   └───app.py
├───initiate.bat
└───Outros Arquivos como (requirements.txt e README.md)
```

## 🫂 Participantes no Projeto:
- Davi Tambara Rodrigues;
- Samuel Eduardo Rocha de Souza;
- Thiago Holz Coutinho.