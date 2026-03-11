import os
import requests

def fetch_repos(username, token):
    url = f"https://api.github.com/users/{username}/repos?sort=pushed&direction=desc&per_page=10"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
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

def generate_svg(repos):
    # Marquee Animation Constants
    width = 800
    height = 60
    
    repo_strings = []
    for repo in repos:
        name = repo['name']
        lang = repo.get('language', 'Other')
        emoji = get_tech_emoji(lang)
        repo_strings.append(f"{emoji} {name}")
    
    marquee_text = "  •  ".join(repo_strings)
    # Duplicate for seamless loop
    display_text = f"{marquee_text}  •  {marquee_text}"
    
    svg_template = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .marquee {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      font-weight: 700;
      font-size: 24px;
      fill: #00D9FF;
      white-space: nowrap;
    }}
    .animate {{
      animation: marquee 30s linear infinite;
    }}
    @keyframes marquee {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-50%); }}
    }}
    .background {{
      fill: #0D1117;
      rx: 10;
    }}
  </style>
  <rect width="{width}" height="{height}" class="background" />
  <g class="animate">
    <text y="50%" x="20" dominant-baseline="middle" class="marquee">{display_text}</text>
  </g>
</svg>'''
    return svg_template

def update_readme(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    # Update title and embed SVG
    pattern = r'## 🌟 Featured Projects.*?<!-- END_SECTION:recent-repos -->'
    replacement = '''## 🚀 Recent Works

<div align="center">
  <img src="./recent_works.svg" width="100%" alt="Recent Works Marquee" />
</div>

<!-- START_SECTION:recent-repos -->
<!-- END_SECTION:recent-repos -->'''
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(updated_content)

if __name__ == "__main__":
    username = "ankushsingh003"
    token = os.environ.get("GITHUB_TOKEN")
    
    try:
        repos = fetch_repos(username, token)
        svg_content = generate_svg(repos)
        
        with open("recent_works.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
        
        update_readme("README.md")
        print("Successfully generated recent_works.svg and updated README.md.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
