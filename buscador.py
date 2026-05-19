import requests

# Seu Token Oficial
TOKEN = "APP_USR-7553899260576138-050520-154c2e718fbb2ce6e8626cf643d2117f-787436450"

def buscar_produtos_ml(termo_busca):
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={termo_busca}&limit=5"
    
    # O SEGREDO ESTÁ AQUI: O crachá (Token) + O disfarce (User-Agent)
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        dados = response.json()
        produtos = dados.get("results", [])
        
        print(f"\n✅ Conexão estabelecida! Ofertas para: '{termo_busca}'")
        print("-" * 50)
        
        for p in produtos:
            nome = p.get("title")
            preco = p.get("price")
            link = p.get("permalink")
            condicao = "Novo" if p.get("condition") == "new" else "Usado"
            
            print(f"📦 {nome}")
            print(f"💰 Preço: R$ {preco:.2f} ({condicao})")
            print(f"🔗 Link: {link}")
            print("-" * 50)
    else:
        print(f"❌ Erro ao acessar API: {response.status_code}")
        print("Detalhe:", response.text)

if __name__ == "__main__":
    buscar_produtos_ml("monitor gamer odyssey g3")