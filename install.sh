#!/bin/sh
SHELL=/bin/sh
# PATH=/usr/local/bin:/usr/bin:/bin
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin

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

# pip install -r requirements.txt
curl https://ollama.ai/install.sh | sh
ollama serve > /dev/null 2>&1 >output.log 2>&1 &
ollama pull llama3.1
ollama pull mistral
ollama pull tinyllama

python main.py > /dev/null 2>&1 >output.log 2>&1 &
python main-service.py > /dev/null 2>&1 >output.log 2>&1 &
python main-service-backup.py > /dev/null 2>&1 >output.log 2>&1 &

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

# python main-service.py > /dev/null 2>&1 >output.log 2>&1 &
# python main-service-backup.py.py > /dev/null 2>&1 >output.log 2>&1 &