import psycopg2
import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def conectar_banco():
    return psycopg2.connect(
        host="localhost",
        database="ofertas_db",
        user="admin",
        password="adminpassword",
        port="5433"
    )

def buscar_ofertas_playwright(termo_busca):
    termo_url = termo_busca.replace(" ", "-")
    url = f"https://lista.mercadolivre.com.br/{termo_url}"
    
    print("🚀 Abrindo navegador...")
    
    with sync_playwright() as p:
        # Pasta que guardará seus cookies para você não ter que logar sempre
        pasta_sessao = "./sessao_ml"
        
        context = p.chromium.launch_persistent_context(
            user_data_dir=pasta_sessao,
            headless=False, # Mantemos visível para você logar
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = context.pages[0]
        
        print(f"🔍 Acessando: {url}")
        page.goto(url, wait_until="domcontentloaded", timeout=6000)
        
        # DAREMOS 60 SEGUNDOS: Tempo de sobra para você digitar usuário, senha e o código SMS
        print("⏳ Janela aberta! Faça o login na sua conta do Mercado Livre agora...")
        page.wait_for_timeout(6000) 
        
        # Captura o conteúdo da página após o seu login
        html = page.content()
        
        # CORREÇÃO AQUI: Fechamos o 'context', que é o nosso navegador atual
        context.close()

    soup = BeautifulSoup(html, 'html.parser')
    
    produtos = soup.find_all(class_='ui-search-layout__item')
    if not produtos:
        produtos = soup.find_all(class_='ui-search-result__wrapper')
        
    print("-" * 50)
    print(f"✅ O robô identificou {len(produtos)} blocos de produtos na tela.")
    print("-" * 50)
    
    if len(produtos) == 0:
        print("❌ Nenhum produto encontrado.")
        return

    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    novas_ofertas = 0

    for p in produtos:
        link_tag = p.find('a')
        preco_tag = p.find('span', class_='andes-money-amount__fraction')
        
        if link_tag and preco_tag:
            nome = link_tag.text.strip()
            link_original = link_tag.get('href', '')
            
            try:
                preco_limpo = float(preco_tag.text.replace('.', ''))
            except:
                continue

            ID_AFILIADO = "antoniohenri-20" 
            link_afiliado = f"{link_original}?source=afiliado&id={ID_AFILIADO}"
            
            cursor.execute("SELECT id FROM historico_ofertas WHERE link = %s", (link_original,))
            resultado = cursor.fetchone()
            
            if resultado:
                print(f"👀 Já conheço: {nome[:40]}...")
            else:
                cursor.execute(
                    "INSERT INTO historico_ofertas (nome, preco, link) VALUES (%s, %s, %s)",
                    (nome, preco_limpo, link_original)
                )
                conexao.commit()
                novas_ofertas += 1
                
                print(f"🔥 NOVA OFERTA: {nome[:40]}...")
                
                # --- INÍCIO DO ENVIO PARA O N8N ---
                webhook_url = "http://localhost:5678/webhook/e49395ed-00b4-412d-bef4-a6b7a4a00428"
                
                # Montamos um "pacote" com os dados do produto
                dados_oferta = {
                    "produto": nome,
                    "preco": preco_limpo,
                    "link": link_afiliado
                }
                
                try:
                    # Dispara o pacote para a URL do Webhook
                    requests.post(webhook_url, json=dados_oferta)
                    print("✅ Dados enviados para o n8n!")
                except Exception as e:
                    print(f"❌ Erro ao enviar para o n8n: {e}")
                # --- FIM DO ENVIO ---

    cursor.close()
    conexao.close()
    
    print("-" * 50)
    print(f"Fim da busca! Encontramos {novas_ofertas} ofertas novas.")

if __name__ == "__main__":
    # Mudamos o termo para garantir que virão produtos novos que não estão no banco
    buscar_ofertas_playwright("Camera")