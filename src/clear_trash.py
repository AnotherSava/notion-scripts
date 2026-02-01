"""
Clear Notion Trash

Permanently deletes all pages in the trash across all workspaces.
"""

import argparse

import requests


class NotionClient:
    """Simple Notion API client using token_v2 cookie authentication."""

    def __init__(self, token_v2: str):
        self.session = requests.Session()
        self.session.cookies.set('token_v2', token_v2)
        self.session.headers['Content-Type'] = 'application/json'

    def post(self, endpoint: str, data: dict) -> requests.Response:
        """Send a POST request to the Notion API."""
        if not endpoint.startswith('/'):
            endpoint = f'/api/v3/{endpoint}'
        return self.session.post(f'https://www.notion.so{endpoint}', json=data)


def get_spaces(client: NotionClient) -> dict[str, str]:
    """Retrieve all workspaces accessible to the user.

    Returns:
        Mapping of space_id to space_name.
    """
    response = client.post('loadUserContent', {}).json()
    if 'recordMap' not in response:
        raise SystemExit(f"Auth error: {response}")
    spaces = response['recordMap']['space']
    return {space_id: data['value']['name'] for space_id, data in spaces.items()}


def get_trashed_blocks(client: NotionClient, space_id: str) -> list[str]:
    """Retrieve all block IDs in the trash for a specific workspace."""
    query = {
        'type': 'BlocksInSpace',
        'query': '',
        'filters': {
            'isDeletedOnly': True,
            'excludeTemplates': False,
            'isNavigableOnly': True,
            'requireEditPermissions': False,
            'ancestors': [],
            'createdBy': [],
            'editedBy': [],
            'lastEditedTime': {},
            'createdTime': {},
            'inTeams': [],
            'includePublicPagesWithoutExplicitAccess': False,
            'navigableBlockContentOnly': True,
        },
        'sort': {'field': 'lastEdited', 'direction': 'desc'},
        'limit': 1000,
        'spaceId': space_id,
        'source': 'trash',
    }
    results = client.post('/api/v3/search', query).json()
    return [block['id'] for block in results['results']]


def delete_blocks_permanently(
    client: NotionClient,
    block_ids: list[str],
    chunk_size: int = 10,
) -> None:
    """Permanently delete blocks in batches."""
    if not block_ids:
        print('\tNo pages found.')
        return

    for i in range(0, len(block_ids), chunk_size):
        batch = block_ids[i:i + chunk_size]
        try:
            client.post('deleteBlocks', {'blockIds': batch, 'permanentlyDelete': True})
            print(f'\tDeleted: {batch}')
        except Exception as e:
            print(f'\tFailed: {batch} ({e})')


def main() -> int:
    parser = argparse.ArgumentParser(description='Clear Notion trash')
    parser.add_argument('token', help="Notion token_v2 cookie value")
    args = parser.parse_args()

    client = NotionClient(args.token)
    spaces = get_spaces(client)

    if input('Confirm? (yes/no) ') != 'yes':
        return 1

    for space_id, space_name in spaces.items():
        print(space_name)
        block_ids = get_trashed_blocks(client, space_id)
        delete_blocks_permanently(client, block_ids)
        print()

    print('Done.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
