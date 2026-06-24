# CONTEXT

Este archivo preserva las metareglas de creación del proyecto y debe reiterarse al iniciar cada nueva secuencia de construcción (uso en Vibe Coding).

## Reglas base de construcción

- Python objetivo: `3.12`.
- Implementación sobre un esqueleto de proyecto estilo cookiecutter.
- Crear dos directorios adicionales en la estructura: `script/` y `ejemplos/`.
- El contenido de `script/` y `ejemplos/` no debe incluirse en el workflow de validación de push.
- Preservar este archivo `CONTEXT.md` en el repositorio.
- Generar un `README.md` básico y mantenerlo actualizado con cada push exitoso.
- Generar un `CHANGELOG.md` y mantenerlo actualizado con cada push exitoso para trazabilidad.
- Registrar en `STORIES.md` los requerimientos que produzcan un nuevo push, con timestamp.
- Agregar licencia MIT.
- Generar documentación automáticamente con `pdoc`.
- Comenzar con versión `1.0 build 000`.
- Cada push exitoso aumenta en `1` el número de build y se actualiza en `README.md` y `CHANGELOG.md`.

## Requisitos de validación y CI

Workflow de validación que ejecuta:

- `ruff` para validar reglas y detectar errores.
- `black` para validar formato consistente.
- Validación de formato PEP8.
- Validación de convenciones PEP257 para docstrings, aceptando solo si no hay errores.
- `mypy` para módulos no excluidos explícitamente.
- `pyright` para módulos no excluidos explícitamente.
- `pytest` con tests unitarios e hipótesis, exigiendo cobertura de `85%` o superior.
- `bandit` para evaluación básica de seguridad sin observaciones.
- No usar `trufflehog`.
- Generar y mantener documentación básica del módulo.
- Mantener `requirements.txt` actualizado.
- Automatizar un workflow de GitHub integrando la fase completa de CI/CD.

## Reglas de diseño e implementación

- Separar la lógica funcional (core) de la de presentación e interacción (cli).
- Usar programación orientada a objetos.
- Gestionar excepciones de runtime y las excepciones específicas del dominio.
- Permitir uso como paquete de Python.
- Producir un archivo comprimido con toda la estructura para subir el proyecto a GitHub.

## Validaciones obligatorias antes de cada commit/push

- Revisar que las modificaciones se reflejen en todos los módulos afectados.
- Ejecutar localmente los mismos programas del workflow antes del push.
- Al introducir un nuevo argumento, variable global o librería, revisar su definición y uso en todos los módulos.
- Ante una modificación estructural, realizar análisis de impacto y actualizar el resto.
