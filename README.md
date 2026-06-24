# json2csv

Conversor de archivos JSON a CSV. Proyecto de la materia Calidad de Software
(UFASTA).

## Estado

- Versión: `1.0 build 000`
- Python: `3.12`
- Licencia: `MIT`

## Uso por línea de comandos

```bash
json2csv entrada.json --output salida.csv
json2csv entrada.json --output salida.csv --delimiter ";"
json2csv entrada.jsonl --output salida.csv --json-lines
json2csv entrada.json --output salida.csv --sort-keys
```

Opciones disponibles:

- `--output` : archivo CSV de destino (obligatorio).
- `--delimiter` : delimitador de un carácter (por defecto `,`).
- `--json-lines` : leer la entrada como JSON Lines (un objeto por línea).
- `--sort-keys` : ordenar las columnas alfabéticamente.
- `--ensure-ascii` : escapar caracteres no ASCII al serializar valores anidados.

Ante una entrada inválida (JSON malformado, archivo inexistente, registros que
no son objetos) el comando termina con un mensaje de error y código distinto de cero.

## Uso como librería

```python
from json2csv import ConversionOptions, JsonToCsvConverter

converter = JsonToCsvConverter()
csv_text = converter.convert_text(
    '[{"name": "Ada", "age": 32, "tags": ["x", "y"]}]',
    ConversionOptions(sort_keys=True),
)
```

La entrada puede ser un arreglo de objetos JSON, un único objeto, o JSON Lines.
Los valores anidados (objetos/listas) se serializan como JSON dentro de la celda;
los nulos quedan como celda vacía y los booleanos como `true`/`false`.

## Entorno de desarrollo

```bash
python -m venv .venv312
source .venv312/bin/activate    # Windows: .venv312\Scripts\activate
python -m pip install -r requirements.txt
python -m pip install -e .
```
