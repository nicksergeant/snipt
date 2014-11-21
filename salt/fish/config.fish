# Directories {{{ 

function l
    tree --dirsfirst -ChFL 1 $args
end
function ll
    tree --dirsfirst -ChFupDaL 1 $args
end

# }}}
# Directories {{{ 

set -g -x fish_greeting ''
set -g -x EDITOR vim

# }}}
# Git and Mercurial functions {{{

function gca 
    git commit -a $argv
end
function gco 
    git checkout $argv
end
function gd 
    git diff HEAD
end
function gl
    git pull $argv
end
function gp 
    git push $argv
end
function gst 
    git status $argv
end

# }}}
# Programs {{{ 

function logs
    sudo supervisorctl tail -f snipt stdout
end
function pm 
    python manage.py $argv
end
function run
    sudo supervisorctl restart snipt
    sudo supervisorctl tail -f snipt stdout
end
function rs
    sudo supervisorctl restart snipt
end
function ssc 
    sudo supervisorctl $argv
end
function wo
    workon (cat .venv) $argv
end

# }}}
# Prompt {{{ 

set -x fish_color_command 005fd7\x1epurple
set -x fish_color_search_match --background=purple

function prompt_pwd --description 'Print the current working directory, shortend to fit the prompt'
    echo $PWD | sed -e "s|^$HOME|~|"
end

function virtualenv_prompt
    if [ -n "$VIRTUAL_ENV" ]
        printf '\033[0;37m(%s) ' (basename "$VIRTUAL_ENV") $argv
    end
end

function fish_prompt
    z --add "$PWD"
    echo ' '
    printf '\033[0;31m%s\033[0;37m on ' (whoami)
    printf '\033[0;31m%s ' (hostname -f)
    printf '\033[0;32m%s' (prompt_pwd)
    echo
    virtualenv_prompt
    printf '\033[0;37m> '
end

# }}}
# Virtualenv {{{ 

set -x WORKON_HOME '/var/www/.virtualenvs'
. ~/.config/fish/virtualenv.fish

# }}}
# Z {{{ 

. /etc/z.fish

function j
    z $argv
end

# }}}
