# MurmurWall

To run offsite data manager, make sure Python3.4 is installed: 

```sh
$ cd Offsite/
$ python3.4 server.py
```

To run main animation: 

```sh
$ cd Onsite/Raspi/
$ python setup.py build_ext --inplace
$ setsid python animation.py < /dev/zero &> log.txt &
```