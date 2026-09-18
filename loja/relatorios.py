"""Relatórios da loja.

Regras do negócio: veja REGRAS.md, seção "Relatório de clientes".
"""


def relatorio_clientes(conn):
    """(nome, cidade, qtd_pedidos) de cada cliente, em ordem de nome.

    Conta só os pedidos feitos a partir de 2026 (veja REGRAS.md).
    """
    # O filtro de data fica no ON, não no WHERE: num LEFT JOIN, condicionar
    # a tabela da direita no WHERE descarta as linhas em que ela é NULL e
    # transforma o LEFT JOIN em INNER JOIN — era isso que sumia com quem
    # nunca comprou e com quem só comprou antes de 2026 (REGRAS.md).
    # COUNT(p.id) ignora NULL, então esses clientes aparecem com qtd 0.
    sql = """
        SELECT c.nome, c.cidade, COUNT(p.id) AS qtd
        FROM clientes c
        LEFT JOIN pedidos p
               ON p.cliente_id = c.id
              AND p.feito_em >= '2026-01-01'
        GROUP BY c.id
        ORDER BY c.nome
    """
    return [tuple(r) for r in conn.execute(sql).fetchall()]
