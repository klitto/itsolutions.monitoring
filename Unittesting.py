from Monitoring import *
import unittest
import logging
import sys
import psutil

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO, stream=sys.stdout)

class MonitoringTestCase(unittest.TestCase):
       
    def testRAMUsag(self):
        testObject = Monitoring()
        ergebnis = testObject.checkRAMUsage(unittest=True)
        self.assertLess(0, ergebnis)
    def testCPUUsage(self):
        testObject = Monitoring()
        ergebnis = testObject.checkCPUUsage(unittest=True)
        self.assertLess(0, ergebnis)
    def testDiskUsage(self):
        testObject = Monitoring()
        ergebnis = testObject.checkDiskUsage(unittest=True)
        self.assertGreater(101, ergebnis)
        self.assertEqual(ergebnis, psutil.disk_usage("/")[3])
    def testProcesses(self):
        testObject = Monitoring()
        ergebnis = testObject.checkProcesses(unittest=True)
        self.assertLess(0, ergebnis)
        self.assertEqual(ergebnis, len(psutil.pids()))
    def testStartTime(self):
        testObject = Monitoring()
        ergebnis = testObject.checkStartTime(unittest=True)
        self.assertEqual(ergebnis, round(int(time.time() - psutil.boot_time())  / 100 / 60 / 60))

if __name__ == "__main__":
    unittest.main()

