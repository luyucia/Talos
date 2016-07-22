pid=$(ps -ef|awk '/talos_listener.py$/{print $2}')
if [ -n "$pid" ];then
echo 'stop talos_listener'
kill $pid
sleep 1
echo $pid 'is killed'
fi

pid=$(ps -ef|awk '/talos_web_server.py$/{print $2}')
if [ -n "$pid" ];then
echo 'stop talos_web_server'
kill $pid
sleep 1
echo $pid 'is killed'
fi
nohup python talos_listener.py >> logs/talos_listener.log 2>&1 &
nohup python talos_web_server.py >> logs/talos_web_server.log 2>&1 &
echo "talos start ^_^"