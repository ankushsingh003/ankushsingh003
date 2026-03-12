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
        "Shell": "🐚",
        "C": "🧱",
        "Java": "☕",
        "Go": "🐹",
        "Rust": "🦀",
        "PHP": "🐘",
        "Ruby": "💎"
    }
    return lang_map.get(lang, "🚀")

def generate_header_svg():
    width = 800
    height = 100
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .header {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      font-weight: 800;
      font-size: 38px;
      fill: url(#paint0_linear);
      text-transform: uppercase;
      letter-spacing: 2px;
    }}
    .subtext {{
      font-family: 'Inter', sans-serif;
      font-size: 16px;
      fill: #8BADC1;
    }}
  </style>
  <defs>
    <linearGradient id="paint0_linear" x1="0" y1="0" x2="{width}" y2="0" gradientUnits="userSpaceOnUse">
      <stop stop-color="#00D9FF"/>
      <stop offset="1" stop-color="#0055FF"/>
    </linearGradient>
  </defs>
  <text x="50%" y="45%" dominant-baseline="middle" text-anchor="middle" class="header">🚀 Recent Works</text>
  <text x="50%" y="75%" dominant-baseline="middle" text-anchor="middle" class="subtext">Automatically updated dashboard of my latest activity</text>
</svg>'''
    return svg

def generate_card_svg(repo, index):
    width = 390
    height = 70
    name = repo['name']
    lang = repo.get('language', 'Other')
    emoji = get_tech_emoji(lang)
    
    text = f"{emoji} {name}"
    display_text = f"{text}  •  {text}  •  {text}"
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <style>
    .marquee {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      font-weight: 700;
      font-size: 18px;
      fill: #00D9FF;
      white-space: nowrap;
    }}
    .animate {{
      animation: marquee 12s linear infinite;
    }}
    @keyframes marquee {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-33.33%); }}
    }}
    .card-background {{
      fill: #0D1117;
      stroke: url(#card_border_{index});
      stroke-width: 2;
      rx: 12;
    }}
    .glow {{
      filter: blur(4px);
      opacity: 0.3;
    }}
  </style>
  <defs>
    <linearGradient id="card_border_{index}" x1="0" y1="0" x2="{width}" y2="{height}" gradientUnits="userSpaceOnUse">
      <stop stop-color="#00D9FF"/>
      <stop offset="1" stop-color="#0055FF"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="{width-4}" height="{height-4}" class="card-background" />
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
        card_markdown += f'<a href="{repo["html_url"]}"><img src="./{card_name}" width="380" alt="{repo["name"]}" /></a>\n'
        if (i + 1) % 2 == 0 and (i + 1) != len(repos):
            card_markdown += '<br/>\n'
    card_markdown += '\n</div>'

    # Remove the old section and replace with polished one
    pattern = r'## 🚀 Recent Works.*?<!-- END_SECTION:recent-repos -->'
    replacement = f'''## 🚀 Recent Works

<div align="center">
  <img src="./works_header.svg" width="100%" alt="Recent Works Hero" />
</div>

<!-- START_SECTION:recent-repos -->
{card_markdown}
<!-- END_SECTION:recent-repos -->'''
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(updated_content)

if __name__ == "__main__":
    username = "ankushsingh003"
    token = os.environ.get("GITHUB_TOKEN")
    
    try:
        repos = fetch_repos(username, token)
        
        # Generate Header SVG
        header_svg = generate_header_svg()
        with open("works_header.svg", "w", encoding="utf-8") as f:
            f.write(header_svg)
            
        # Generate individual SVGs
        for i, repo in enumerate(repos):
            svg_content = generate_card_svg(repo, i)
            with open(f"work_{i+1}.svg", "w", encoding="utf-8") as f:
                f.write(svg_content)
        
        update_readme(repos)
        print(f"Successfully generated header and {len(repos)} cards. Updated README.md.")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
