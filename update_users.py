from github import Github
from datetime import datetime, timedelta
import time

# Inicialize o cliente GitHub com o token
g = Github('GITHUB_TOKEN')

# Verifique o limite de taxa
rate_limit = g.get_rate_limit().core
if rate_limit.remaining == 0:
    reset_time = rate_limit.reset - datetime.now()
    sleep_time = max(reset_time.total_seconds(), 0)
    print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
    time.sleep(sleep_time)

# Defina o intervalo de datas
today = datetime.now()
start_of_week = today - timedelta(days=today.weekday())
end_of_week = start_of_week + timedelta(days=6)

# Busque usuários
query = 'location:Brazil sort:followers-desc'
try:
    result = g.search_users(query)[:50]
except Exception as e:
    print(f"Error fetching users: {e}")
    result = []

# Processar usuários
for user in result:
    print(user.login)  # Exemplo de processamento
