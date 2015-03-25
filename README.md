# MurmurWall

To run main animation: 

```sh
$ cd Raspi/
$ python setup.py build_ext --inplace
$ setsid python animation.py < /dev/zero &> log.txt &
```