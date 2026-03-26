# SIVIG - Sistema Integrado de Vigilância Sanitária

O SIVIG é uma aplicação Single Page (SPA) leve e rápida focada na triagem epidemiológica, desenvolvida para ser utilizada por fiscais em pontos de entrada no país.

O sistema foi desenhado para dispensar instalações complexas: todo o frontend (HTML, Tailwind CSS, Alpine.js) está incorporado diretamente ao arquivo `main.py`, sem a necessidade de banco de dados ou arquivos separados para uso imediato em operação.

## 🚀 Como Executar Localmente

### 1. Pré-requisitos
- O único requisito no sistema é ter o [Python 3.8+](https://www.python.org/downloads/) (ou superior) instalado.

### 2. Instale as Dependências
Utilize o `pip` para instalar os pacotes necessários especificados:

```bash
pip install -r requirements.txt
```

### 3. Inicie o Servidor
Com o ambiente configurado, basta rodar o arquivo `main.py`:

```bash
python main.py
```

### 4. Acesse o Sistema
Abra seu navegador de preferência (como Chrome, Firefox ou Edge) e acesse:

👉 **http://localhost:8000**

---

## 🛠️ Tecnologias Utilizadas
- **Backend**: [Python](https://www.python.org/) + [FastAPI](https://fastapi.tiangolo.com/) (rápido e moderno) + Servidor [Uvicorn](https://www.uvicorn.org/)
- **Frontend**: HTML5, [Tailwind CSS](https://tailwindcss.com/) (estilização) e [Alpine.js](https://alpinejs.dev/) (reatividade sem recarregamento de página)

## 📌 Funcionalidades
- **Registro de Inspeção:** Coleta de dados de passageiros e do transporte (Aeronave/Embarcação).
- **Triagem Epidemiológica Automática:** Caso o viajante apresente risco de contágio ou venha de áreas específicas com surto (como China, Itália ou Irã), o sistema gera um *ALERTA SANITÁRIO* pulsante visível.
- **Tabela Dinâmica:** Os registros aparecem na tela de inspeção em tempo real.
- **Armazenamento em Memória:** Os dados populados durante o runtime ficam contidos na memória do próprio Python. Nenhuma configuração adicional de Banco de Dados de terceiros.
