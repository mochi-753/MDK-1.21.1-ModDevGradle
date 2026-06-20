import json
import os
from contextlib import ExitStack
from pathlib import Path

import requests

def main():
    data = {
        'name': f"{os.environ.get('MOD_NAME')} {os.environ.get('MOD_VERSION')}",
        'version_number': os.environ.get('MOD_VERSION').removeprefix('v'),
        'changelog': Path('CHANGELOG.md').read_text(encoding='utf-8'),
        'dependencies': [],
        'game_versions': ['1.21.1'],
        'version_type': os.environ.get('RELEASE_TYPE'),
        'loaders': ['neoforge'],
        'featured': True,
        'project_id': os.environ.get('MODRINTH_PROJECT_ID')
    }

    try:
        with open('src/main/python/dependencies.modrinth.json', 'r', encoding='utf-8') as f:
            data['dependencies'] = json.load(f)
    except FileNotFoundError:
        pass

    with ExitStack() as stack:
        files = {}
        file_parts = []

        for jar in Path('artifacts').glob('*.jar'):
            file = stack.enter_context(jar.open('rb'))
            file_part = jar.stem
            file_parts.append(file_part)
            files[file_part] = (jar.name, file, 'application/java-archive')

        if not file_parts:
            raise FileNotFoundError('No Jar files found.')

        data['file_parts'] = file_parts
        data['primary_file'] = file_parts[0]

        response = requests.post(
            'https://api.modrinth.com/v2/version',
            headers={
                'Authorization': os.environ.get('MODRINTH_TOKEN'),
                'User-Agent': f"{os.environ.get('REPOSITORY')}/{os.environ.get('MOD_VERSION')}"
            },
            data={
                'data': json.dumps(data)
            },
            files=files
        )
        print(response.text)
        response.raise_for_status()


if __name__ == '__main__':
    main()
