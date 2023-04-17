from typing import Dict


class Serializable:
    def to_dict(self) -> Dict:
        raise NotImplementedError('Has to be overriden by subclass')

    @classmethod
    def from_dict(cls, data: Dict) -> 'Serializable':
        raise NotImplementedError('Has to be overriden by subclass')
