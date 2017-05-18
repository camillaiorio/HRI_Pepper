# Pepper tools

This repository contains different tools to manage the Softbank Pepper robot.

## Requirements
### C++

* Install **qibuild** following the instructions in:

     [http://doc.aldebaran.com/2-5/dev/cpp/install_guide.html#installation](http://doc.aldebaran.com/2-5/dev/cpp/install_guide.html#installation)

     Follow also the instructions there to prepare your worktree where you will have to install these pepper_tools.

* Install NAOqi SDK for C++ following the instructions in:

     [http://doc.aldebaran.com/2-5/dev/cpp/install_guide.html#installing-and-configuring-naoqi-sdk](http://doc.aldebaran.com/2-5/dev/cpp/install_guide.html#installing-and-configuring-naoqi-sdk)

### Python

* Install NAOqi SDK for Python following the instructions in:

http://doc.aldebaran.com/2-5/dev/python/install_guide.html

### How to record a dataset for Pepper
* First you need to disable the _"Autonomous Life"_ to have full control on Pepper and to avoid background programs interfering with Pepper movements. We use the **setstate** program with param ``disabled``
```bash
$ ./setstate <PEPPER_IP> <PEPPER_PORT> disabled
```
* After this, Pepper goes in posture _"Crouch"_. In order to have Pepper standing up, use the program **setposture** with param ``Stand``
```bash
$ ./setposture <PEPPER_IP> <PEPPER_PORT> Stand
```