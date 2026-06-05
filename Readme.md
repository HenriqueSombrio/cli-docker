# Docker Cleaner CLI (cli-docker)

Uma interface de linha de comando (CLI) interativa para gerenciar e limpar recursos do Docker (containers, imagens, volumes) e também diretórios de volumes locais do seu projeto.

## Requisitos

- Python >= 3.8
- Docker instalado e rodando
- Permissões de superusuário (root/sudo) para algumas operações de remoção de arquivos locais (`.volumes`).

## Instalação

Para utilizar a ferramenta facilmente de qualquer lugar, recomenda-se a instalação local via `pip`.

1. Navegue até o diretório do projeto:
   ```bash
   cd /var/www/html/ferramentas/cli-docker
   ```

2. Instale o pacote (recomendado usar um ambiente virtual ou instalação de usuário):
   ```bash
   pip install -e .
   ```

## Como Executar

### Opção 1: Usando o comando instalado (Recomendado)

Se você instalou o pacote usando o `pip`, um executável será adicionado ao seu path. Basta rodar:

```bash
mydocker
```

### Opção 2: Executando o script diretamente pelo Python

Caso não queira instalar o projeto globalmente ou no seu ambiente atual, você pode executá-lo diretamente através do Python estando na raiz do projeto:

```bash
python -m cli.main
```

## Funcionalidades

Ao executar a ferramenta, um menu interativo será exibido com as seguintes opções:

- **Remover Containers:** Lista todos os containers e permite múltipla seleção para remoção forçada.
- **Remover Imagens:** Lista imagens Docker disponíveis para seleção e remoção.
- **Remover Volumes Docker:** Lista volumes nativos do Docker para limpeza.
- **Remover Volumes Locais (.docker/.volumes):** Procura por pastas locais em `/var/www/html/*/.docker/.volumes` para excluir dados persistidos em disco.
- **Limpar Tudo (prune):** Executa `docker system prune -a --volumes -f` para limpeza completa.
- **Sair:** Encerra a aplicação.
