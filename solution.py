import datetime
import requests


def cotar():
    hoje = datetime.date.today()
    inicio = hoje - datetime.timedelta(days=364)

    consulta_inicio = inicio - datetime.timedelta(days=10)

    data_inicial = consulta_inicio.strftime("%m-%d-%Y")
    data_final = hoje.strftime("%m-%d-%Y")

    url = (
        "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        "CotacaoDolarPeriodo(dataInicial=@dataInicial,"
        "dataFinalCotacao=@dataFinalCotacao)"
    )

    params = {
        "@dataInicial": f"'{data_inicial}'",
        "@dataFinalCotacao": f"'{data_final}'",
        "$format": "json",
        "$top": 1000
    }

    resposta = requests.get(url, params=params)
    resposta.raise_for_status()
    dados = resposta.json()["value"]

    cotacoes = {}

    for item in dados:
        data = datetime.datetime.strptime(
            item["dataHoraCotacao"][:10], "%Y-%m-%d"
        ).date()

        cotacoes[data] = item["cotacaoCompra"]

    resultado = []
    ultima_cotacao = None
    total_dias = (hoje - consulta_inicio).days + 1

    for i in range(total_dias):
        data = consulta_inicio + datetime.timedelta(days=i)

        if data in cotacoes:
            ultima_cotacao = cotacoes[data]
        if data >= inicio and ultima_cotacao is not None:
            resultado.append(ultima_cotacao)

    return resultado
