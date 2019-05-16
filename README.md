# TestChamber
This repository contains the python software which controls the different compents of the TestChamber MBE system. Hardware software interface is done by using a DAQ unit from the company Labjack. 



## Requirements
* Python 3.x with x >= 5
* Labjack USB driver
* LabjackPython package

## Required packages
* LabjackPython package
* numpy
* SciPy
* thermocouples_reference
* MatPlotLib

Instructions on how to install exodriver and LabjackPython are given in the section *How to install Labjack USB driver and Python package* below.


## How to install Labjack USB driver and Python package

Being able to communicate with the Labjack DAQ units a USB driver and the LabjackPython library needs to be installed. USB driver installation varies for Windows, Mac and Linux. Different drivers can be found [here](https://labjack.com/support/software/installers/ud).

Step-by-step installation for Linux:
1. **Install exodriver**: necessary for USB communication with Linux. To do so, follow the steps [here](https://labjack.com/support/software/installers/exodriver).
If problems occure during the driver build consult the detailed installation instruction provided in the *INSTALL.Linux* file on the [exodriver github page](https://github.com/labjack/exodriver/blob/master/INSTALL.Linux)
2. **Install LabjackPython package**: necessary to communicate with device via python. Instructions can be found [here](https://labjack.com/support/software/examples/ud/labjackpython)

For Windows and Mac the first step will be different. Check [here](https://labjack.com/support/software/installers/ud).


