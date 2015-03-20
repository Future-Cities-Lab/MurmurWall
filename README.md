# MurmurWall

To run offsite data manager, migrate to Offsite/, run command 'python3.4 server.py'.

To run main animation: 
ssh pi@10.0.1.123
password: *Industrial Complex Password
cd to Onsite/Raspi/, run command 'setsid python animation.py < /dev/zero &> log.txt &'.
or
python animation.py *to see output on screen