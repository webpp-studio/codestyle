#!/usr/bin/env python
"""Test file."""


class Foo(object):
    """Foo class."""

    def __init__(self):
        """Init method."""
        number = 3
        self.baz = f'{number}'

    async def async_test(self):
        """Async method."""
        return 'async'
