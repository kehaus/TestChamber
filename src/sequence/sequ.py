"""
contains short example of how to initialize hardware components with
the python classes from the TestChamber repository.



"""
__version__ = "0.0.1"
__author__ = "kha"



import queue

from ..daq.daqunit import DAQUnitBase
from ..daq.sm7022 import SM7022
from ..daq.pkr251 import PKR251
from ..daq.rs880varian import RS880Varian

from ..util.worker_thread import WorkerThread, WorkerTask

dd = DAQUnitBase()
sm = SM7022(dd)
pkr = PKR251(dd)
rs = RS880Varian(dd)


###

pkr_wt = WorkerTask(pkr.get_pressure, continuous=True, save=True, base_name='pkr251')
rs_wt = WorkerTask(rs.get_pressure, continuous=True, save=True, base_name='rs880')

q = queue.Queue()

q.put(pkr_wt)
q.put(rs_wt)

w = WorkerThread(q)






#class PKR251Task(WorkerTask):
#    """ """

    











