'''Extended functionality for libyiban.'''
__version__ = 'v1.0.5 Indev Rewrite2'
__author__ = 'Eric Zhang (EZForever), https://github.com/EZForever'

__all__ = [
    'IdiomSolitaire',
    'QAppCommenter',
    'XinHuaNews'
]

from .IdiomSolitaire import IdiomSolitaire
from .QAppCommenter import QAppCommenter
import libyiban_ex.XinHuaNews

