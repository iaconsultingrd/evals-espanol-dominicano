"""Evalúa qué tan bien entiende Claude el español y el contexto dominicano.

Uso:
    export ANTHROPIC_API_KEY=...
    python evaluar.py                       # modelo por defecto
    python evaluar.py --modelo claude-haiku-4-5
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

import anthropic

PROMPT_JUEZ = """Eres un evaluador estricto pero justo.
Pregunta: {pregunta}
Respuesta de referencia: {referencia}
Respuesta a evaluar: {respuesta}

¿La respuesta a evaluar transmite el mismo significado esencial que la referencia?
Ignora el estilo y la longitud. Responde solo con una palabra: CORRECTO o INCORRECTO."""


def preguntar(cliente, modelo: str, texto: str, max_tokens: int = 300) -> str:
    r = cliente.messages.create(
        model=modelo, max_tokens=max_tokens, messages=[{"role": "user", "content": texto}]
    )
    return r.content[0].text.strip()


def evaluar(cliente, casos: list[dict], modelo: str, juez: str) -> list[dict]:
    resultados = []
    for caso in casos:
        respuesta = preguntar(cliente, modelo, caso["pregunta"])
        veredicto = preguntar(cliente, juez, PROMPT_JUEZ.format(respuesta=respuesta, **caso), 5)
        correcto = veredicto.upper().startswith("CORRECTO")
        resultados.append({**caso, "respuesta": respuesta, "correcto": correcto})
        print(f"{'✅' if correcto else '❌'} {caso['id']}: {caso['pregunta']}")
    return resultados


def resumen(resultados: list[dict]) -> dict:
    por_categoria = defaultdict(list)
    for r in resultados:
        por_categoria[r["categoria"]].append(r["correcto"])
    por_categoria["total"] = [r["correcto"] for r in resultados]
    return {c: f"{sum(v)}/{len(v)}" for c, v in por_categoria.items()}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--modelo", default="claude-sonnet-5-5")
    p.add_argument("--juez", default="claude-opus-5-5")
    p.add_argument("--casos", default=Path(__file__).parent / "casos.jsonl")
    p.add_argument("--salida", default="resultados.json")
    args = p.parse_args()

    casos = [json.loads(l) for l in Path(args.casos).read_text(encoding="utf-8").splitlines() if l.strip()]
    resultados = evaluar(anthropic.Anthropic(), casos, args.modelo, args.juez)
    Path(args.salida).write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nResumen:", resumen(resultados))
