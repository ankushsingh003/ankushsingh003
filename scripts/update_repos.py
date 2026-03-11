import os
import requests
import re

def fetch_repos(username, token):
    url = f"https://api.github.com/users/{username}/repos?sort=pushed&direction=desc&per_page=10"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # Filter out the profile README repo itself
    return [repo for repo in response.json() if repo['name'] != username][:5]

def get_tech_emoji(lang):
    lang_map = {
        "Python": "🐍",
        "C++": "⚙️",
        "JavaScript": "📜",
        "TypeScript": "🟦",
        "HTML": "🌐",
        "CSS": "🎨",
        "Jupyter Notebook": "📓",
        "Shell": "🐚"
    }
    return lang_map.get(lang, "🚀")

def generate_card_svg(repo, index):
    width = 400
    height = 60
    name = repo['name']
    lang = repo.get('language', 'Other')
    emoji = get_tech_emoji(lang)
    
    text = f"{emoji} {name}"
    # Duplicate for seamless marquee if name is long, or just center if short.
    # For variety, let's keep the marquee but per card.
    display_text = f"{text}  •  {text}  •  {text}"
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .marquee {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      font-weight: 700;
      font-size: 20px;
      fill: #00D9FF;
      white-space: nowrap;
    }}
    .animate {{
      animation: marquee 15s linear infinite;
    }}
    @keyframes marquee {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-33.33%); }}
    }}
    .background {{
      fill: #0D1117;
      stroke: #1B2331;
      stroke-width: 2;
      rx: 10;
    }}
  </style>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" class="background" />
  <g class="animate">
    <text y="50%" x="20" dominant-baseline="middle" class="marquee">{display_text}</text>
  </g>
</svg>'''
    return svg

def update_readme(repos):
    filename = "README.md"
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate the grid of cards
    card_markdown = '<div align="center">\n\n'
    for i, repo in enumerate(repos):
        card_name = f"work_{i+1}.svg"
        card_markdown += f'<a href="{repo["html_url"]}"><img src="./{card_name}" width="390" alt="{repo["name"]}" /></a>\n'
        if (i + 1) % 2 == 0 and (i + 1) != len(repos):
            card_markdown += '<br/>\n'
    card_markdown += '\n</div>'

    pattern = r'<!-- START_SECTION:recent-repos -->.*?<!-- END_SECTION:recent-repos -->'
    replacement = f'<!-- START_SECTION:recent-repos -->\n{card_markdown}\n<!-- END_SECTION:recent-repos -->'
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(updated_content)

if __name__ == "__main__":
    username = "ankushsingh003"
    token = os.environ.get("GITHUB_TOKEN")
    
    try:
        repos = fetch_repos(username, token)
        
        # Generate individual SVGs
        for i, repo in enumerate(repos):
            svg_content = generate_card_svg(repo, i)
            with open(f"work_{i+1}.svg", "w", encoding="utf-8") as f:
                f.write(svg_content)
        
        update_readme(repos)
        print(f"Successfully generated {len(repos)} cards and updated README.md.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
