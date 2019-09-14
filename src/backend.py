#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author kern0bal_
from typing import List


def get_block(block_id: int) -> List:
    encrypted_data = open(f"/Users/jacob/Desktop/boat_bored/data_store/blocks/block_{block_id}", 'rb').read()
    filename = f"block_{block_id}"
    return [block_id, filename, encrypted_data]
