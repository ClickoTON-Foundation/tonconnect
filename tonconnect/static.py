from dataclasses import dataclass
from .options import BaseRequestOption

@dataclass
class Metadata:
    manifest_url: str
    items: list[BaseRequestOption]
    
    def to_dict(self):
        return {
            'manifestUrl': self.manifest_url,
            'items': [item.to_dict() for item in self.items]
        }
