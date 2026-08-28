import requests

# Seu código TG capturado!
CODIGO_TG = "COLOQUE_SEU_CODIGO_TG_AQUI"

url = "https://api.mercadolibre.com/oauth/token"

payload = {
    "grant_type": "authorization_code",
    "client_id": "COLOQUE_SEU_CLIENT_ID_AQUI",
    "client_secret": "COLOQUE_SEU_CLIENT_SECRET_AQUI",
    "code": CODIGO_TG,
    "redirect_uri": "https://www.google.com"
}

headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=payload, headers=headers)

if response.status_code == 200:
    dados = response.json()
    print("✅ SUCESSO! Guarde estes dados:")
    print("-" * 30)
    print(f"ACCESS_TOKEN: {dados.get('access_token')}")
    print(f"REFRESH_TOKEN: {dados.get('refresh_token')}")
    print("-" * 30)
else:
    print(f"❌ Erro {response.status_code}: {response.text}")
