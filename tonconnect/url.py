import urllib.parse
from .static import Metadata

def get_url(app_url: str, id: str, metadata: Metadata):
    metadata = metadata.to_dict()
    metadata = str(metadata).replace(' ', '').replace('\'', '"')
    
    return f'https://{app_url}/ton-connect?v=2&id={id}&r={urllib.parse.quote(metadata)}'
