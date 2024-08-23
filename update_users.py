import requests
from github import Github
from datetime import datetime, timedelta

# Use GitHub's REST API to fetch user information
g = Github('YOUR_GITHUB_TOKEN')
users = []

# Verifica o limite de taxa
rate_limit = g.get_rate_limit()
print('Rate Limit:', rate_limit)

# Calculate the start and end dates of the current week
today = datetime.now()
start_of_week = today - timedelta(days=today.weekday())
end_of_week = start_of_week + timedelta(days=6)

query = 'location:Brazil sort:followers-desc'
try:
    result = g.search_users(query)[:50]
except Exception as e:
    print(f'Error fetching users: {e}')
    result = []

for user in result:
    repos = user.get_repos()
    languages = {}
    total_commits = 0
    for repo in repos:
        language = repo.language
        if language:
            languages[language] = languages.get(language, 0) + 1
        try:
            # Fetch commits for the week
            commits = repo.get_commits(since=start_of_week, until=end_of_week)
            total_commits += commits.totalCount
        except Exception as e:
            print(f'Error fetching commits for repo {repo.name}: {e}')

    users.append({
        'login': user.login,
        'languages': sorted(languages.items(), key=lambda item: item[1], reverse=True),
        'commits': total_commits
    })

try:
    with open('README.md', 'r') as file:
        readme = file.readlines()
except FileNotFoundError as e:
    print(f'Error reading README.md: {e}')
    readme = []

start_line = readme.index('<!-- START TOP USERS -->\n') if '<!-- START TOP USERS -->\n' in readme else 0
end_line = readme.index('<!-- END TOP USERS -->\n') if '<!-- END TOP USERS -->\n' in readme else len(readme)

new_content = ['<!-- START TOP USERS -->\n']
for user in users:
    new_content.append(f'- **{user["login"]}**: {", ".join([f"{lang} ({count})" for lang, count in user["languages"]])}, **Commits this week:** {user["commits"]}\n')
new_content.append('<!-- END TOP USERS -->\n')

readme[start_line:end_line+1] = new_content

try:
    with open('README.md', 'w') as file:
        file.writelines(readme)
except Exception as e:
    print(f'Error writing README.md: {e}')
