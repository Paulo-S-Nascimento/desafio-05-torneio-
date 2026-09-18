"""Cálculo do valor de um pedido.

Regras do negócio: veja REGRAS.md, seção "Total do pedido".
"""
from loja.banco import criar_conexao  # noqa: F401  (import usado nos testes)


def _linhas(conn, tabela, pedido_id):
    return conn.execute(
        f"SELECT * FROM {tabela} WHERE pedido_id = ?", (pedido_id,)
    ).fetchall()


def calcular_total(conn, pedido_id):
    """Devolve o valor final do pedido, com 2 casas decimais."""
    ped = conn.execute(
        "SELECT frete, cupom FROM pedidos WHERE id = ?", (pedido_id,)
    ).fetchone()
    frete_cheio, cupom = ped[0], ped[1]

    subtotal = 0.0
    for _id, _ped, _prod, qtd, preco in _linhas(conn, "itens", pedido_id):
        subtotal += qtd * preco

    estornado = 0.0
    for row in _linhas(conn, "estornos", pedido_id):
        estornado += row[2]

    frete = 0.0 if subtotal >= 150 else frete_cheio

    # O cupom desconta SÓ os produtos: o teto do desconto é o subtotal,
    # nunca o subtotal + frete (REGRAS.md, item 3). Sem o teto no subtotal
    # um cupom maior que os produtos consumia o frete e zerava o pedido.
    desconto = min(cupom, subtotal)
    total = (subtotal - desconto) + frete - estornado
    return round(total, 2)
