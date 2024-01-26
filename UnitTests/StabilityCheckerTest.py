import sys
import unittest
sys.path.append("C:\\Users\\mhaye\\code\\School\\6045 Algorithms\\advanced-algorithms-work")
from StabilityChecker import StabilityChecker

class TestMatch:
    def __init__(self,name:str, match:list):
        self._name = name
        self._match = match
        
class StabilityCheckerTest(unittest.TestCase):

    def test_all_stable(self):
        #Setup
        matches=[TestMatch("H-1",["R-3","R-4"]),TestMatch("H-2",["R-1","R-2"])]

        positiondata=[]
        positiondata.append(["H-1","2","R-3","R-4","R-1","R-2","R-5"])
        positiondata.append(["H-2","2","R-1","R-2","R-3","R-4","R-5"])

        applicantdata=[]
        applicantdata.append(["R-1","H-2","H-1"])
        applicantdata.append(["R-2","H-2","H-1"])
        applicantdata.append(["R-3","H-1","H-2"])
        applicantdata.append(["R-4","H-1","H-2"])
        applicantdata.append(["R-5","H-2","H-1"])  
        
        #Act
        stabilityChecker = StabilityChecker(applicantdata, positiondata, matches)
        unstableMatches = stabilityChecker.stabilityCheckAll()

        #Assert
        self.assertEquals(len(unstableMatches), 0)
        #print(sys.path)

    # First type of instability: There are students s and s’, and a hospital h, so that
    # s is assigned to h, and s’ is assigned to no hospital, and h prefers s’ to s
    def test_type_1_unstable(self):
        #Setup
        matches=[TestMatch("H-1",["R-3","R-5"]),TestMatch("H-2",["R-1","R-2"])]

        positiondata=[]
        positiondata.append(["H-1","2","R-3","R-4","R-1","R-2","R-5"])
        positiondata.append(["H-2","2","R-1","R-2","R-3","R-4","R-5"])

        applicantdata=[]
        applicantdata.append(["R-1","H-2","H-1"])
        applicantdata.append(["R-2","H-2","H-1"])
        applicantdata.append(["R-3","H-1","H-2"])
        applicantdata.append(["R-4","H-1","H-2"])
        applicantdata.append(["R-5","H-2","H-1"])  

        #Act
        stabilityChecker = StabilityChecker(applicantdata, positiondata, matches)
        unstableMatches = stabilityChecker.stabilityCheckType1()

        #Assert
        self.assertEqual(len(unstableMatches), 1)
        self.assertEqual(unstableMatches[0], "Type 1 Instability: H-1 has applicants matched to positions that are lower on their wish list then applicants that did not get matched at all.")
        #print(sys.path)

    # Second type of instability: There are students s and s’, and a hospitals h and h’, so that
    # s is assigned to h, and s’ is assigned to h’, and h prefers s’ to s, and s’ prefers h to h’
    def test_type_2_unstable(self):
        #Setup
        matches=[TestMatch("H-1",["R-1","R-2"]),TestMatch("H-2",["R-3","R-4"])]

        positiondata=[]
        positiondata.append(["H-1","2","R-3","R-4","R-1","R-2","R-5"])
        positiondata.append(["H-2","2","R-1","R-2","R-3","R-4","R-5"])

        applicantdata=[]
        applicantdata.append(["R-1","H-2","H-1"])
        applicantdata.append(["R-2","H-2","H-1"])
        applicantdata.append(["R-3","H-1","H-2"])
        applicantdata.append(["R-4","H-1","H-2"])
        applicantdata.append(["R-5","H-2","H-1"])    

        #Act
        stabilityChecker = StabilityChecker(applicantdata, positiondata, matches)
        unstableMatches = stabilityChecker.stabilityCheckType2()

        #Assert
        unstableMatchesMessages =[]
        unstableMatchesMessages.append("Type 2 Instability: For, M={H-1,R-1,R-2}. H-2 prefers R-1 over H-1, and R-1 prefers H-2 over the currently matched H-1")
        unstableMatchesMessages.append("Type 2 Instability: For, M={H-1,R-1,R-2}. H-2 prefers R-2 over H-1, and R-2 prefers H-2 over the currently matched H-1")
        unstableMatchesMessages.append("Type 2 Instability: For, M={H-2,R-3,R-4}. H-1 prefers R-3 over H-2, and R-3 prefers H-1 over the currently matched H-2")
        unstableMatchesMessages.append("Type 2 Instability: For, M={H-2,R-3,R-4}. H-1 prefers R-4 over H-2, and R-4 prefers H-1 over the currently matched H-2")

        self.assertEqual(len(unstableMatches), len(unstableMatchesMessages))
        self.assertEqual(unstableMatches[0], unstableMatchesMessages[0])
        self.assertEqual(unstableMatches[1], unstableMatchesMessages[1])
        self.assertEqual(unstableMatches[2], unstableMatchesMessages[2])
        self.assertEqual(unstableMatches[3], unstableMatchesMessages[3])
