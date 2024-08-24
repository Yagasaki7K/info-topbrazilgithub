import os
from github import Github

# Configurações
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Certifique-se de definir este token no ambiente
REPO_FILE_PATH = 'README.md'

# Inicialize o cliente GitHub com o token
g = Github(GITHUB_TOKEN)

def fetch_top_users():
    query = 'location:Brazil sort:followers-desc'
    users = g.search_users(query)[:50]  # Pegue os 50 usuários mais seguidos
    return users

def generate_markdown(users):
    content = "# Top 50 Brazilian GitHub Users\n\n"
    content += "| Username | Profile | Commits |\n"
    content += "|----------|---------|------------|\n"
    for user in users:
        content += f"| {user.login} | [Link]({user.html_url}) | {user.get_contributions()} |\n"
    return content

def update_readme(content):
    with open(REPO_FILE_PATH, 'w') as file:
        file.write(content)

def main():
    users = fetch_top_users()
    markdown_content = generate_markdown(users)
    update_readme(markdown_content)
    print("README.md updated successfully.")

if __name__ == "__main__":
    main()
