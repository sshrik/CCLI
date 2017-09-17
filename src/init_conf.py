import os

homeDir = os.environ['HOME']
f = open(homeDir + '/.bashrc', 'a')
f.writelines('export CCLI=$HOME/ccli_conf')
f.writelines('alias memo=\'python3 ~/$CCLI/ccli_bin/memo.py\'')
f.writelines('alias todo=\'python3 ~/$CCLI/ccli_bin/todo.py\'')
f.writelines('alias diary=\'python3 ~/$CCLI/ccli_bin/diary.py\'')
