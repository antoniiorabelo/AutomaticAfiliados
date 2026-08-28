import requests
import json

TOKEN = "COLOQUE_SEU_TOKEN_AQUI"

def testar_acesso_api():
    # Essa rota devolve os dados básicos de quem é o dono do Token
    url = "https://api.mercadolibre.com/users/me"
    
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), indent=4))

if __name__ == "__main__":
    testar_acesso_api()
