import mysql.connector
from faker import Faker

conn_relacional = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="0101",
    database="relacional",
)

conn_dimensional = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="0101",
    database="dimensional",
)

cursor_relacional = conn_relacional.cursor()
cursor_dimensional = conn_dimensional.cursor()

# Pais insert
cursor_relacional.execute(
    "INSERT INTO pais (idPais, nmPais) VALUES (%s, %s)",
    (1, 'Brasil',)
)

# Qualidade video insert

qualidade_video = [
    (1, 'SD'),
    (2, 'HD'),
    (3, 'Full HD'),
    (4, '4K'),
]

cursor_relacional.executemany(
    "INSERT INTO qualidadevideo (idQualidade, descricao) VALUES (%s, %s)",
    qualidade_video
)

# Plano insert
planos = [
    (1, 'Normal', 15.90, 1, 1),
    (2, 'Normal+', 49.90, 2, 1),
    (3, 'Premium', 49.99, 2, 2),
    (4, 'Premium+', 69.90, 4, 3),
    (5, 'PremiumPlus+', 99.90, 1, 4),
]
cursor_relacional.executemany(
    "INSERT INTO plano (idPlano, nmPlano, precoMensal, numTelas, Qualidadevideo_idQualidade) VALUES (%s, %s, %s, %s, %s)",
    planos
)

# SituacaoAssinatura insert
situacoes = [
    (1, 'Ativo'),
    (2, 'Inativo')
]
cursor_relacional.executemany(
    "INSERT INTO situacaoassinatura (idSituacao, descricao) VALUES (%s, %s)",
    situacoes
)

fake = Faker('pt_BR')

for i in range(1, 6):
    # Estado e cidade insert
    estado = fake.state()
    cidade = fake.city()

    cursor_relacional.execute(
        "INSERT INTO estado (idEstado, nmEstado) VALUES (%s, %s)",
        (i, estado)
    )

    cursor_relacional.execute(
        "INSERT INTO cidade (idCidade, nmCidade) VALUES (%s, %s)",
        (i, cidade)
    )
    
    # Usuario insert
    nome_usuario = fake.name()
    email_usuario = fake.email()
    dt_nascimento_usuario = fake.date_of_birth(minimum_age=18, maximum_age=80)
    sexo_usuario = fake.random_element(elements=('M', 'F'))
    cursor_relacional.execute(
        "INSERT INTO usuario (idUsuario, nome, email, dtNascimento, sexo, pais_idPais, cidade_idCidade, estado_idEstado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (i, nome_usuario, email_usuario, dt_nascimento_usuario, sexo_usuario, 1, i, i)
    )

    # Assinatura insert
    dt_inicio_assinatura = fake.date_between(start_date='-10y', end_date='-5y')
    dt_fim_assinatura = fake.date_between(start_date=dt_inicio_assinatura, end_date='-5y')
    situacao = fake.random_element(elements=(1, 2))
    cursor_relacional.execute(
        "INSERT INTO assinatura (idAssinatura, dtInicio, dtFim, Usuario_idUsuario, Plano_idPlano, SituacaoAssinatura_idSituacao) VALUES (%s, %s, %s, %s, %s, %s)",
        (i, dt_inicio_assinatura, dt_fim_assinatura, i, i, situacao)
    )

    # Pagamento insert
    dt_pagamento = fake.date_between(start_date=dt_inicio_assinatura, end_date=dt_fim_assinatura)
    valor_recebido = planos[i-1][2]
    cursor_relacional.execute(
        "INSERT INTO pagamento (idPagamento, dtPagamento, vlrRecebido, Assinatura_idAssinatura) VALUES (%s, %s, %s, %s)",
        (i, dt_pagamento, valor_recebido, i)
    )

conn_relacional.commit()
'''
    # Função insert
    desc = fake.random_element(elements=('Câmera', 'Compositor', 'Ator', 'Diretor', 'Produtor', "Roterista", "Editor"))
    cursor_relacional.execute(
        "INSERT INTO funcao (idFuncao, descFuncao) VALUES (%s, %s)",
        (i, desc,)
    )

    # Artista insert
    nome_artista = fake.name()
    cursor_relacional.execute(
        "INSERT INTO artista (idArtista, nmArtista) VALUES (%s, %s)",
        (i, nome_artista,)   
    )
    
    cursor_relacional.execute(
        "INSERT INTO artistaconteudo (Artista_idArtista, Conteudo_idConteudo, )"
    )
'''
    
        
    
    
    
    