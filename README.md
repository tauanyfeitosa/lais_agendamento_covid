# Segunda Fase LAIS - Agendamento COVID-19

## Descrição

Este projeto foi desenvolvido como pré-requisito parcial no edital Nº028/2023 do LAIS/UFRN, para a vaga de Backend nível 1.

## Configuração do Projeto

### Passos para execução

1. Clone este repositório e crie um ambiente virtual:

    ```bash
    python -m venv venv
    ```

2. Ative o ambiente virtual:

    - No Windows:

        ```bash
        \venv\Scripts\activate
        ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure o banco de dados do projeto:

   - Utilize os arquivos `local_settings_sample` e `.env_sample` como modelos. Copie as informações de ambos os arquivos e crie os arquivos `local_settings` e `.env`, colando as respectivas informações.

5. Rode os comandos para carregar os dados necessários:

    ```bash
    python manage.py importar_estabelecimentos_saude
    python manage.py importar_grupos_atendimento
    ```

6. Execute as migrações:

    ```bash
    python manage.py migrate
    ```

Seu programa está pronto para ser executado!

## Resumo de Funcionamento

Para acompanhar e testar o funcionamento, consulte o seguinte edital: [Edital Nº028/2023 do LAIS/UFRN](https://lais.huol.ufrn.br/wp-content/uploads/2023/12/Edital_028.2023-Selecao-de-alunos-de-tecnologia1.pdf)

