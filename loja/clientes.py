"""Busca de clientes."""


def buscar_por_email(conn, email):
    """Devolve (id, nome, cidade) do cliente com aquele e-mail, ou None."""
    # Consulta parametrizada: o e-mail viaja como VALOR, não como texto
    # concatenado no SQL. Isso fecha a injeção (o payload deixa de ser
    # interpretado como sintaxe) e faz o apóstrofo de e-mails legítimos
    # funcionar sem escape manual (REGRAS.md, "Busca por e-mail").
    sql = "SELECT id, nome, cidade FROM clientes WHERE email = ?"
    linha = conn.execute(sql, (email,)).fetchone()
    return tuple(linha) if linha else None
