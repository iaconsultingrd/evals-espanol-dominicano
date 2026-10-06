# evals-espanol-dominicano 🇩🇴

Un pequeño conjunto de evaluaciones para medir **qué tan bien entienden los modelos de IA el español dominicano y el contexto local** de República Dominicana.

Los modelos se entrenan sobre todo con español "neutro". Si una persona en Santo Domingo pregunta por la guagua, el colmado o el ITBIS, ¿la IA la entiende? Este repo es un punto de partida para medirlo de forma abierta y reproducible.

## Qué mide

| Categoría | Ejemplos |
| - | - |
| `vocabulario` | guagua, concho, colmado, zafacón, "dame un chin", "está en olla" |
| `contexto` | tasa del ITBIS, dígitos de la cédula y el RNC, códigos de área, moneda |

Son 20 casos en [`casos.jsonl`](casos.jsonl), cada uno con una pregunta y una respuesta de referencia.

## Cómo funciona

1. El modelo evaluado responde cada pregunta.
2. Un segundo modelo, el juez, compara la respuesta con la referencia y decide si es `CORRECTO` o `INCORRECTO`.
3. El script imprime un resumen por categoría y guarda el detalle en `resultados.json`.

## Uso

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=tu_clave
python evaluar.py
python evaluar.py --modelo claude-haiku-4-5 --juez claude-opus-5-5
```

## Contribuir

¡Se buscan más casos! Sobre todo de:

- Expresiones regionales (Cibao, Sur, Este).
- Trámites comunes (DGII, JCE, TSS).
- Preguntas donde una respuesta incorrecta podría causar daño real (salud, legal, finanzas).

Abre un *pull request* agregando líneas a `casos.jsonl` con un `id` único y una referencia verificada.

## Limitaciones

- 20 casos son una muestra, no un benchmark completo.
- Usar un modelo como juez puede introducir sesgos: revisa a mano los casos dudosos.

---

Hecho con Claude Code por [Juan Navarro](https://www.linkedin.com/in/juandanielnavarro/) · Licencia MIT.
