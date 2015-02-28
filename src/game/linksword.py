__author__ = 'brad'

import src.engine as engine


class LinkSword(engine.GameObject):
    def __init__(self, *args, **kwargs):
        engine.GameObject.__init__(self, args, kwargs)