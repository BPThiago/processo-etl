import mysql.connector
from faker import Faker

conn_relacional = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="0101",
    database="relacional",
)

cursor_relacional = conn_relacional.cursor()

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

localidades_ids = []

# Criando buffer de pais, estado e cidade
for i in range(1, 6):
    # Pais, estado, cidade insert
    pais = fake.country()
    estado = fake.state()
    cidade = fake.city()

    # Pais insert
    cursor_relacional.execute(
        "INSERT INTO pais (idPais, nmPais) VALUES (%s, %s)",
        (i, pais)
    )

    # Estado insert
    cursor_relacional.execute(
        "INSERT INTO estado (idEstado, nmEstado) VALUES (%s, %s)",
        (i, estado)
    )

    # Cidade insert
    cursor_relacional.execute(
        "INSERT INTO cidade (idCidade, nmCidade) VALUES (%s, %s)",
        (i, cidade)
    )
    localidades_ids.append(i)

for i in range(1, 101):
    # Usuario insert
    nome_usuario = fake.name()
    email_usuario = fake.email()
    dt_nascimento_usuario = fake.date_of_birth(minimum_age=18, maximum_age=40) # Limitar um pouco a faixa etária :D
    sexo_usuario = fake.random_element(elements=('M', 'F'))
    localidade_selecionada = fake.random_element(elements=localidades_ids)
    cursor_relacional.execute(
        "INSERT INTO usuario (idUsuario, nome, email, dtNascimento, sexo, pais_idPais, cidade_idCidade, estado_idEstado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (i, nome_usuario, email_usuario, dt_nascimento_usuario, sexo_usuario, localidade_selecionada, localidade_selecionada, localidade_selecionada)
    )

    # Assinatura insert
    dt_inicio_assinatura = fake.date_between(start_date='-12y', end_date='-7y')
    dt_fim_assinatura = fake.date_between(start_date=dt_inicio_assinatura, end_date='-7y')
    situacao = fake.random_element(elements=(1, 2))
    plano_escolhido = fake.random_element(elements=(1, 2, 3, 4, 5))
    cursor_relacional.execute(
        "INSERT INTO assinatura (idAssinatura, dtInicio, dtFim, Usuario_idUsuario, Plano_idPlano, SituacaoAssinatura_idSituacao) VALUES (%s, %s, %s, %s, %s, %s)",
        (i, dt_inicio_assinatura, dt_fim_assinatura, i, plano_escolhido, situacao)
    )

    # Pagamento insert
    dt_pagamento = fake.date_between(start_date=dt_inicio_assinatura, end_date=dt_fim_assinatura)
    valor_recebido = planos[plano_escolhido-1][2]
    cursor_relacional.execute(
        "INSERT INTO pagamento (idPagamento, dtPagamento, vlrRecebido, Assinatura_idAssinatura) VALUES (%s, %s, %s, %s)",
        (i, dt_pagamento, valor_recebido, i)
    )

conn_relacional.commit()