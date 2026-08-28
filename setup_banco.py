import psycopg2

def criar_tabela():
    try:
        # Conectando ao banco de dados no seu Docker
        conexao = psycopg2.connect(
            host="localhost",
            database="ofertas_db",
            user="admin",
            password="COLOQUE_SUA_SENHA_DO_BANCO_AQUI",
            port="5433"
        )
        cursor = conexao.cursor()
        
        # Comando SQL para criar a tabela se ela não existir
        comando_sql = '''
        CREATE TABLE IF NOT EXISTS historico_ofertas (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            preco NUMERIC NOT NULL,
            link TEXT UNIQUE NOT NULL,
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        
        cursor.execute(comando_sql)
        conexao.commit()
        
        print("✅ Sucesso! Tabela 'historico_ofertas' criada ou já existente no banco de dados.")
        
    except Exception as e:
        print(f"❌ Erro ao conectar no banco de dados: {e}")
    finally:
        if 'conexao' in locals():
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    criar_tabela()
