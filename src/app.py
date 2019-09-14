#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: kern0bal_
import sys
import os
import re

from flask import Flask, render_template

BLOCKS_DIR='/Users/jacob/Desktop/boat_bored/data_store/blocks/'

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/blocks')
def display_blocks():
    blocks = []

    for file in os.listdir(BLOCKS_DIR):
        if file.endswith(".block"):
            blocks.append(
                (re.findall(r'\d+', file)[0], file, open(os.path.join(BLOCKS_DIR, file), 'rb').read())
            )
    
    return render_template('blocks.html', blocks=blocks)

