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
```

Ante una entrada inválida (JSON malformado, archivo inexistente, registros que
no son objetos) el comando termina con un mensaje de error y código de salida
distinto de cero.

## Uso como librería

```python
from json2csv import JsonToCsvConverter

converter = JsonToCsvConverter()
csv_text = converter.convert_text('[{"name": "Ada", "age": "32"}]')
print(csv_text)
# name,age
# Ada,32
```

También puede convertir archivos:

```python
from pathlib import Path
from json2csv import ConversionOptions, ConversionRequest, JsonToCsvConverter

JsonToCsvConverter().convert_file(
    ConversionRequest(
        source=Path("entrada.json"),
        destination=Path("salida.csv"),
        options=ConversionOptions(),
    )
)
```

## Entorno de desarrollo

```bash
python -m venv .venv312
source .venv312/bin/activate    # Windows: .venv312\Scripts\activate
python -m pip install -r requirements.txt
python -m pip install -e .
```
