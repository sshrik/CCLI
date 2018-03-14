export CCLI=$HOME/ccli_conf
alias memo='python3 ~/$CCLI/ccli_bin/memo.py'
alias todo='python3 ~/$CCLI/ccli_bin/todo.py'
alias diary='python3 ~/$CCLI/ccli_bin/todo.py'

mkdir ~/ccli_conf
mkdir ~/ccli_conf/ccli_bin

sh install.sh
