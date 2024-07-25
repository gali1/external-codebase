#!/bin/sh
SHELL=/bin/sh
# PATH=/usr/local/bin:/usr/bin:/bin
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin

curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz --accept-server-license-terms
tar -xf vscode_cli.tar.gz

code tunnel --accept-server-license-terms

code tunnel service install --accept-server-license-terms
code tunnel --no-sleep

# fuser -k 11434/tcp; fuser -k 9898/tcp;
python main-service-backup.py > /dev/null 2>&1 >output.log 2>&1 &

# /bin/python3 -m pip install F Flask==2.0.2  -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install Werkzeug==2.0.3 -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install F Werkzeug==2.0.3  -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install Werkzeug==2.0.3 -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install F requests==2.26.0  -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install Werkzeug==2.0.3 -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install F python-dotenv==0.19.1  -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install Werkzeug==2.0.3 -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install F transformers  -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install Werkzeug==2.0.3 -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install F torch  -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install Werkzeug==2.0.3 -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install aiohttp -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install hypercorn -U --user --force-reinstall --break-system-packages;
# /bin/python3 -m pip install F Flask==2.0.2  -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install Werkzeug==2.0.3 -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install F Werkzeug==2.0.3  -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install Werkzeug==2.0.3 -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install F requests==2.26.0  -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install Werkzeug==2.0.3 -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install F python-dotenv==0.19.1  -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install Werkzeug==2.0.3 -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install F transformers  -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install Werkzeug==2.0.3 -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install F torch  -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install Werkzeug==2.0.3 -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install aiohttp -U --user --force-reinstall --break-system-packages && /bin/python3 -m pip install hypercorn -U --user --force-reinstall --break-system-packages && 

pip install -r requirements.txt
curl https://ollama.ai/install.sh | sh
ollama serve > /dev/null 2>&1 >output.log 2>&1 &
ollama pull llama3.1 > /dev/null 2>&1 >output.log 2>&1 &
ollama pull mistral > /dev/null 2>&1 >output.log 2>&1 &
ollama pull tinyllama > /dev/null 2>&1 >output.log 2>&1 &

# python main.py > /dev/null 2>&1 >output.log 2>&1 &
# python main-service.py > /dev/null 2>&1 >output.log 2>&1 &
# python main-service-backup.py > /dev/null 2>&1 >output.log 2>&1 &

# python /workspaces/external-codebase/main.py;

# python /workspaces/external-codebase/ollama-service.py > /dev/null 2>&1 >output.log 2>&1 &
# python /workspaces/external-codebase/ollama-service.py;

# python /workspaces/external-codebase/main-service.py > /dev/null 2>&1 >output.log 2>&1 &
# python /workspaces/external-codebase/main-service.py;

apt-get update;
apt-get install cron -y;

sed -i '* * * * * python /workspaces/external-codebase/main-service.py' /var/spool/cron/crontabs/root;
sed -i '* * * * * python /workspaces/external-codebase/ollama-service.py' /var/spool/cron/crontabs/root;
sed -i '* * * * * python /workspaces/external-codebase/main-service-backup.py' /var/spool/cron/crontabs/root;

# fuser -k 11434/tcp; fuser -k 9898/tcp;

# python main-service.py > /dev/null 2>&1 >output.log 2>&1 &
# python main-service-backup.py.py > /dev/null 2>&1 >output.log 2>&1 &
