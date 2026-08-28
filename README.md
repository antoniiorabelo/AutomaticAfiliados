# Automatic Afiliados 🚀

Um robô inteligente de **web scraping** para monitoramento de ofertas no Mercado Livre, com disparo de alertas em tempo real via Telegram.

O projeto implementa um fluxo completo de captura, persistência de dados e integração de sistemas em um ambiente isolado.

## 🛠️ Tecnologias e Arquitetura

- **Scraping:** Python, Playwright e BeautifulSoup4
- **Banco de Dados:** PostgreSQL
- **Orquestração de Automação:** n8n
- **Infraestrutura:** Docker e Docker Compose
- **Notificações:** Telegram Bot API via Webhook (HTTP POST)
- **Gerenciamento Visual do Banco:** DBeaver

## 🔄 Como o Fluxo Funciona

1. **Captura:**  
   O script Python utiliza o Playwright para renderizar páginas dinâmicas e o BeautifulSoup4 para extrair produtos, preços e links de afiliado.

2. **Validação e Persistência:**  
   Os dados são validados no PostgreSQL. Se a oferta for inédita, ela é salva no histórico, evitando envios duplicados no futuro.

3. **Integração:**  
   O Python envia um payload JSON para um Webhook disponibilizado pelo n8n.

4. **Notificação:**  
   O n8n processa os dados e consome a API do Telegram, entregando um card formatado com o link direto da oferta no celular do usuário.

## ⚙️ Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

- [Python 3.10 ou superior](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

## 🚀 Como Executar o Projeto Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/antoniiorabelo/AutomaticAfiliados.git
cd AutomaticAfiliados
```

### 2. Inicie a infraestrutura

O comando abaixo iniciará o PostgreSQL e o n8n:

```bash
docker compose up -d
```

### 3. Configure o ambiente virtual Python

#### Windows — Prompt de Comando

```bash
python -m venv venv
venv\Scripts\activate
```

#### Windows — PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Linux ou macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install psycopg2-binary requests playwright beautifulsoup4
playwright install
```

### 5. Configure o n8n

1. Acesse [http://localhost:5678](http://localhost:5678) no navegador.
2. Importe o fluxo de Webhook para Telegram.
3. Configure as credenciais do Telegram Bot.
4. Informe o seu Chat ID.
5. Atualize a variável `webhook_url` no arquivo `scraper_ml.py` com o endereço do Webhook gerado pelo n8n.

### 6. Execute o robô

Primeiro, crie as tabelas do banco de dados:

```bash
python setup_banco.py
```

Depois, execute o scraper:

```bash
python scraper_ml.py
```

## 🔒 Segurança

Por motivos de segurança, nenhuma credencial, senha ou token deve ser armazenado diretamente no código.

Utilize um arquivo `.env` para armazenar informações sensíveis, como:

- Usuário e senha do PostgreSQL
- Token do Telegram Bot
- Chat ID do Telegram
- URL do Webhook do n8n

Adicione o arquivo `.env` ao `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

O arquivo `docker-compose.yml` e os scripts Python podem ser versionados, desde que não contenham credenciais diretamente. Utilize variáveis de ambiente nesses arquivos.

## 📱 Demonstração do Projeto

Confira o vídeo de demonstração mostrando o funcionamento da infraestrutura, a persistência dos dados no banco e o disparo das mensagens:

👉 [Assistir à demonstração no LinkedIn](https://lnkd.in/p/djiydm47)
