import urllib.parse
from .static import Metadata

def get_url(app_url: str, id: str, metadata: Metadata) -> str:
    metadata_dict = metadata.to_dict()
    metadata_parsed = str(metadata_dict).replace(' ', '').replace('\'', '"')
    
    return f'https://{app_url}/ton-connect?v=2&id={id}&r={urllib.parse.quote(metadata_parsed)}'
