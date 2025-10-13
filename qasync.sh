#!/bin/bash 
#

SRC=ai_snake_lab
DEST=snake_venv/lib/python3.11/site-packages/ai_snake_lab

rm -rf $DEST
mkdir $DEST
rsync -avr --delete $SRC/* $DEST
