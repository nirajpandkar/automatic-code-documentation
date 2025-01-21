#!/bin/zsh
# .git/hooks/pre-add
python run_update_doc.py --diff "$1"