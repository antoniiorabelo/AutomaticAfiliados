import requests
import json

TOKEN = "APP_USR-7553899260576138-050520-154c2e718fbb2ce6e8626cf643d2117f-787436450"

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