'''Automated operations on yiban.cn, originated from YBTap.'''
__version__ = 'v1.0.5 Indev Rewrite2'
__author__ = 'Eric Zhang (EZForever), https://github.com/EZForever'

__all__ = [
    'YiBanAccount',
    'YiBanGroup',
    'YiBanArticle'
]

from .YiBanAccount import YiBanAccount
from .YiBanGroup import YiBanGroup
from .YiBanArticle import YiBanArticle

