import json

with open('firebase.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

config['hosting']['headers'] = [
    {
      "source": "**/*.@(html|js|css)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "no-cache, no-store, must-revalidate"
        }
      ]
    }
]

with open('firebase.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2)

print('Firebase headers updated')
