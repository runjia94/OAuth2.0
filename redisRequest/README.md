Request Limit
==============
If client sends lots of request in a short time, the server will breakdown.
So limit.py sets a limit request line and hungryclient.py sends request.
If number of requests hit the line, it will stop.

Pre-Request
------------
1. Install Redis.
In your vagrant VM, you should use these command lines to install redis:

```bash
cd ~
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo make install
```

2. Run in different console
First, you should type 
```bash
redis-server &
```
Then, push return. Then at the same console, run the limit.py file
```bash
python limit.py
```
Then, open a new console. Run the hungryclient.py
```bash
python hungryclient.py
```

ATTENTION
----------
These Codes from Udacity, Full Stack Nanodegree. 
I just test them for fun.