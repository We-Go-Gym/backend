"""Módulo de testes unitários para as funções de criptografia de senha"""
import pytest
from app.routes.aluno import criptografa_senha, chave_criptografada


def test_criptografa_senha():
    """Testa a criptografia e a verificação de uma única senha"""

    senha_plana = "minhasenha123"
    senha_hash = criptografa_senha(senha_plana)

    assert senha_plana != senha_hash
    assert chave_criptografada.verify(senha_plana, senha_hash) is True
    assert chave_criptografada.verify("senhaerrada", senha_hash) is False


@pytest.mark.parametrize(
    "senha_plana",
    [
        ("senha_forte_123"),
        ("outra&senha!com@caracteres"),
        ("123456"),
        (""),
    ],
)
def test_criptografa_multiplas_senhas(senha_plana):
    """Testa a criptografia para um conjunto parametrizado de senhas"""

    senha_hash = criptografa_senha(senha_plana)

    assert senha_plana != senha_hash
    assert chave_criptografada.verify(senha_plana, senha_hash) is True
