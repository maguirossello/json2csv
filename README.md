# json2csv

`json2csv` es un paquete y CLI para convertir archivos JSON a CSV. Proyecto de
prueba para mostrar elementos de integración continua para la materia Calidad de
Software - UFASTA - Mar del Plata.

## Estado

- Versión: `1.0 build 000`
- Python: `3.12`
- Licencia: `MIT`

## Funciones disponibles

- Conversión de JSON a CSV en memoria.
- Conversión de archivos JSON a archivos CSV.
- Soporte de entrada como arreglo JSON, objeto único o JSON Lines.
- Unión y ordenamiento de columnas; serialización de valores anidados, nulos y booleanos.
- CLI separada de la lógica del dominio.
- Validaciones, tipado estático, pruebas e integración continua.

## Estructura

```text
src/        paquete Python
tests/      pruebas automáticas
docs/       documentación base y salida generada
script/     utilidades auxiliares fuera del alcance del workflow
ejemplos/   ejemplos fuera del alcance del workflow
```

## Uso por línea de comandos

```bash
json2csv entrada.json --output salida.csv
json2csv entrada.json --output salida.csv --delimiter ";"
json2csv entrada.jsonl --output salida.csv --json-lines
json2csv entrada.json --output salida.csv --sort-keys
```

Opciones: `--output` (obligatorio), `--delimiter`, `--json-lines`, `--sort-keys`,
`--ensure-ascii`. Ante una entrada inválida (JSON malformado, archivo inexistente,
registros que no son objetos) el comando termina con error y código distinto de cero.

## Uso como librería

```python
from json2csv import ConversionOptions, JsonToCsvConverter

converter = JsonToCsvConverter()
csv_text = converter.convert_text(
    '[{"name": "Ada", "age": 32, "tags": ["x", "y"]}]',
    ConversionOptions(sort_keys=True),
)
```

Los valores anidados se serializan como JSON dentro de la celda; los nulos quedan
como celda vacía y los booleanos como `true`/`false`.

## Entorno de desarrollo

```bash
python -m venv .venv312
source .venv312/bin/activate    # Windows: .venv312\Scripts\activate
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Calidad local

```bash
python -m ruff check src tests
python -m black --check src tests
python -m mypy src tests
python -m pyright src tests
python -m pytest --cov=src/json2csv --cov-fail-under=85
python -m bandit -r src -c pyproject.toml
```

## Documentación

```bash
python -m pdoc --output-directory docs/site src/json2csv
```
