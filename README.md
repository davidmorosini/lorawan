# Py2Solve - Lorawan Decoder

Biblioteca em python com decodificadores de mensagens da rede LoRaWan fornecidos pela empresa 2Solve.

---

## Utilização da biblioteca

```python
from py2Solve import Decoder

Decoder.decode("gB1A9P30gCQAAAAAgB5DxIAAgCUAAAAAgB9C1AAAgCYAAAAAgCNCA6PXgCcAAAAA")

# Resposta
{
    'json2sense': {
        'drainage_PH': 7.656,
        'drainage_PH_SD': 0.0,
        'drainage_Turbidity': 393.0,
        'drainage_Turbidity_SD': 0.0,
        'drainage_Conductivity': 106.0,
        'drainage_Conductivity_SD': 0.0,
        'drainage_Temp': 32.91,
        'drainage_Temp_SD': 0.0
    }
}
```

## Configurando o ambiente local

- Instale uma distribuição python em seu ambiente local.
   
- Crie um environment conda com uma versão `3.10` do python (**Apenas para usuários do pacote Anaconda**):
    ```powershell
    # Criando um ambiente virtual de nome 'py310' com a versão 3.10 do python
    conda create -n py310 python=3.10 -y
    ```

    ```powershell
    conda env list
    ```

    A saída será parecida com esta abaixo:
    ```powershell
    # conda environments:
    #
    base                  *  D:\amdskit\dev\anaconda3
    py310                    D:\amdskit\dev\anaconda3\envs\py310
    ```

    Selecione o diretório do ambiente virtual criado `py310` para utilizarmos como referência do executável python no próximo passo. Neste exemplo será o diretório `D:\amdskit\dev\anaconda3\envs\py310\python.exe`.

- Crie um ambiente virtual python com nome `.venv`, para isso basta executar o pacote `venv` (ou `virtualenv`):

    ```powershell
    # Primeiro Navegue até o diretório que deseja criar o .venv e em seguida execute o comando abaixo
    D:\amdskit\dev\anaconda3\envs\py310\python.exe -m venv .venv

    # Ou diretamente caso não esteja usando conda
    python -m venv .venv
    ```

    ```powershell
    # execute este comando para ativar em seu terminal atual, a versão do python contida dentro do ambiente virtual criado
    .venv\Scripts\activate

    # Note que o seu terminal terá o seguinte layout, (.venv) PS D:\...>

    # Após, atualize o pip e por fim, instale o pacote poetry
    pip install --upgrade pip
    pip install poetry
    ```

- Instale o ambiente Poetry

    ```powershell
    poetry install --no-interaction
    ```

Seu ambiente local para desenvolvimento e testes está pronto.

---

## Executando Ambiente de QAS e Testes Locais

Basta executar os scripts contidos no arquivo `Makefile.bat` caso esteja no ambiente Windows, no caso de estar no Linux utilize a mesma lógica apontando para o arquivo `Makefile (make)`. Ssando como parâmetro, algum items abaixo:

```
qas    -> Executa todas as formatações de linteres, checagem do pyproject e testes automatizados

black  -> Executa a formatação do Black

isort  -> Executa a formatação do Isort

autoflake -> Executa a formatação do Autoflake

tests     -> Executa os testes unitários

poetry_check -> Executa a verificação do arquivo pyproject.toml
```

Exemplo de execução:

```powershell
# Windows
.\Makefile.bat qas
```

```bash
# linux
make qas
```


---
