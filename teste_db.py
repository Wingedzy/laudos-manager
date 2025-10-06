from app.config import engine

try:
    conn = engine.connect()
    print("Conexão com PostgreSQL funcionando!")
    conn.close()
except Exception as e:
    print("Erro ao conectar:", e)

