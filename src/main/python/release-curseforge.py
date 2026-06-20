import json
import os
from contextlib import ExitStack
from pathlib import Path

import markdown
import requests

def main():
    metadata = {
        'changelog': markdown.Markdown(extensions=['extra']).convert(Path('CHANGELOG.md').read_text(encoding='utf-8')),
        'changelogType': 'html',
        'displayName': f"{os.environ.get('MOD_NAME')} {os.environ.get('MOD_VERSION')}",
        'gameVersions': [11779],  # Minecraft 1.21.1
        'gameVersionNames': ['Client', 'Server', 'NeoForge', '1.21.1'],
        'releaseType': os.environ.get('RELEASE_TYPE'),
        'relations': {
            'projects': []
        }
    }

    try:
        with open('src/main/python/dependencies.curseforge.json', 'r', encoding='utf-8') as dependencies_file:
            metadata['relations']['projects'] = json.load(dependencies_file)
    except FileNotFoundError:
        pass

    for jar in Path('artifacts').glob('*.jar'):
        with jar.open('rb') as jar_file:
            response = requests.post(
                f"https://minecraft.curseforge.com/api/projects/{os.environ.get('CURSEFORGE_PROJECT_ID')}/upload-file",
                headers={
                    'X-Api-Token': os.environ.get('CURSEFORGE_TOKEN'),
                    'User-Agent': f"{os.environ.get('REPOSITORY')}/{os.environ.get('MOD_VERSION')}"
                },
                data={
                    'metadata': json.dumps(metadata)
                },
                files={
                    'file': (
                        jar.name,
                        jar_file,
                        'application/java-archive'
                    )
                }
            )
            print(response.text)
            response.raise_for_status()


if __name__ == '__main__':
    main()
