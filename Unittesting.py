from Monitoring import *
import unittest
import logging
import sys
import psutil

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, stream=sys.stdout)

class MonitoringTestCase(unittest.TestCase):

    '''
    Compares the results of the monitoring class functions with a separate check
    '''
    def testRAMUsage(self):
        testObject = Monitoring()
        ergebnis = testObject.checkRAMUsage(unittest=True)
        self.assertLess(0, ergebnis)
        print("Gemessener RAM-Testwert: " + str(ergebnis))
    def testCPUUsage(self):
        testObject = Monitoring()
        ergebnis = testObject.checkCPUUsage(unittest=True)
        self.assertLess(0, ergebnis)
        print("Gemessener CPU-Testwert: " + str(ergebnis))
    def testDiskUsage(self):
        testObject = Monitoring()
        ergebnis = testObject.checkDiskUsage(unittest=True)
        self.assertGreater(101, ergebnis)
        self.assertEqual(ergebnis, psutil.disk_usage("/")[3])
        print("Gemessener Disk-Usage-Testwert: " + str(ergebnis))
    def testProcesses(self):
        testObject = Monitoring()
        ergebnis = testObject.checkProcesses(unittest=True)
        self.assertLess(0, ergebnis)
        self.assertEqual(ergebnis, len(psutil.pids()))
        print("Gemessener Prozess-Testwert: " + str(ergebnis))
    def testStartTime(self):
        testObject = Monitoring()
        ergebnis = testObject.checkStartTime(unittest=True)
        self.assertEqual(ergebnis, round(int(time.time() - psutil.boot_time())  / 100 / 60 / 60))
        print("Gemessener Starttime-Testwert: " + str(ergebnis))

if __name__ == "__main__":
    unittest.main()

