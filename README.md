# json2csv

Conversor de archivos JSON a CSV. Proyecto de la materia Calidad de Software
(UFASTA).

## Estado

- Versión: `1.0 build 000`
- Python: `3.12`
- Licencia: `MIT`

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

La entrada puede ser un arreglo de objetos JSON o un único objeto. Ante una
entrada inválida (JSON malformado, archivo inexistente, registros que no son
objetos) la herramienta lanza un error controlado.

## Entorno de desarrollo

```bash
python -m venv .venv312
source .venv312/bin/activate    # Windows: .venv312\Scripts\activate
python -m pip install -r requirements.txt
python -m pip install -e .
```
