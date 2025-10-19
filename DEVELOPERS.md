# Pre Commit

Instalar el siguiente script para ejecutar los archivos de precommit:

```
pip install pre-commit
pre-commit install
```

# Configurar ambiente venv para python

```
python3 -m venv .venv
source .venv/bin/activate
```

# Instalar dependencias para postgreSQL (Apple Silicon)

```
brew install libpq --build-from-source
brew install openssl
export PATH="/opt/homebrew/Cellar/libpq/17.4_1/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/opt/openssl@3/lib -L/opt/homebrew/opt/libpq/lib"
export CPPFLAGS="-I/opt/homebrew/opt/openssl@3/include -I/opt/homebrew/opt/libpq/include"
```

Después de instalar las dependencias del sistema, instalar las dependencias de Python:

```
pip install -r requirements.txt
# o alternativamente:
pip install -e .
```
