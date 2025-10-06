from config import engine

try:
    conn = engine.connect()
    print("Conexão com PostgreeSQL funcionando!")
    conn.close()
except Exception as e:
    print("Erro ao conectar: ", e)