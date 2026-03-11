import os
import re
import requests

def fetch_repos(username, token):
    url = f"https://api.github.com/users/{username}/repos?sort=pushed&direction=desc&per_page=10"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # Filter out the profile README repo itself
    return [repo for repo in response.json() if repo['name'] != username][:4]

def generate_markdown(repos):
    content = '<div align="center">\n\n'
    for i, repo in enumerate(repos):
        name = repo['name']
        owner = repo['owner']['login']
        # Using Socialify for visual impact
        img_url = f"https://socialify.git.ci/{owner}/{name}/image?description=1&font=Inter&name=1&owner=1&pattern=Plus&theme=Dark"
        content += f'<a href="{repo["html_url"]}"><img src="{img_url}" width="400" /></a>\n'
        if (i + 1) % 2 == 0 and (i + 1) != len(repos):
            content += '<br/>\n'
    content += '\n</div>'
    return content

def update_readme(filename, new_content):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'(<!-- START_SECTION:recent-repos -->).*?(<!-- END_SECTION:recent-repos -->)'
    replacement = f'\\1\n{new_content}\n\\2'
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(updated_content)

if __name__ == "__main__":
    username = "ankushsingh003"
    token = os.environ.get("GITHUB_TOKEN")
    readme_path = "README.md"
    
    try:
        repos = fetch_repos(username, token)
        markdown = generate_markdown(repos)
        update_readme(readme_path, markdown)
        print("Successfully updated README.md with recent repos.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
