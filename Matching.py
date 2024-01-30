from xmlrpc.client import boolean

#
 # Class Name: position
 # Class Variables:
 #  1) [str] name : the name of the position
 #  2) [str] opening : the amount of opened positions of the position
 #  3) [list] preference : the list of preferenced applicants by the position
 #  4) [list] match : the list of matched applicants of the position
 # Usage: stores the data of the position to be used by the match class
 #
class position:
    def __init__(self,name:str,opening:str,preference:list):
        self._name=name
        self._openings=int(opening)
        self._preference=preference
        self._match=[]
        for elements in range(int(opening)):
            self._match.append(None)
    #
    # Method name: getPreference
    # Formal Parameters: None
    # Return Value: list
    # Usage: returns the preference of the position
    #
    def getPreference(self,prioritynumber)->list:
        return self._preference[prioritynumber]
    #
     # Method name: getOpenings
     # Formal Parameters: None
     # Return Value: int
     # Usage: returns the openings of the position
     #
    def getOpenings(self)->int:
        return self._openings
    #
     # Method name: increaseOpenings
     # Formal Parameters: None
     # Return Value: int
     # Usage: increase openings for the position by one.
     #
    def increaseOpenings(self)->None:
        self._openings+=1
    #
     # Method name: decreaseOpenings
     # Formal Parameters: None
     # Return Value: None
     # Usage: decreases the openings of the position by one
     #
    def decreaseOpenings(self)->None:
        self._openings-=1
    #
     # Method name: addMatch
     # Formal Parameters:
     #  1) [str] name: the name of the applicant that is matched to the position
     # Return Value: None
     # Usage: adds an applicant to the matching list of the position
     #
    def addMatch(self,name:str)->None:
        counter=0
        while(self._match[counter]!=None):
            counter+=1
        self._match[counter]=name
        self.decreaseOpenings()
    #
     # Method name: removeMatch
     # Formal Parameters:
     #  1) [str] name: the name of the applicant that will be removed from the matching list
     # Return Value: None
     # Usage: removes the named applicant from the list
     #
    def removeMatch(self,name:str)->None:
        for counter in range(len(self._match)):
            if self._match[counter]==name:
                self._match[counter]=None
                self.increaseOpenings()
    #
     # Method name: getMatch
     # Formal Parameters: None
     # Return Value: list
     # Usage: gets the list of matches of the position
     #
    def getMatch(self)->list:
        return self._match
    #
     # Method name: full
     # Formal Parameters: None
     # Return Value: bool
     # Usage: checks to see if there anymore openings in the position
     #
    def full(self)->bool:
            return False if self._openings>0 else True 
    #
     # Method name: __str__
     # Formal Parameters: None
     # Return Value: str
     # Usage: returns a string of the method when the object is printed
     #
    def __str__(self)->str:
        container=f'{self._name},{",".join(self.getMatch())}'
        return container
#
 # Class Name: applicant
 # Class Variables:
 #  1) [str] name : the name of the applicant
 #  2) [list] preference : the list of preferences of the student
 #  3) [str|None] match : the matched position of the applicant
 # Usage: stores the information of the applicant to be used by the match class
 #
class applicant:
    def __init__(self,name:str,preference:list)->None:
        self._name=name
        self._preferences=preference
        self._match=None
    #
     # Method name: getPreference
     # Formal Parameters: None
     # Return Value: list
     # Usage: returns the preferences of the applicant
     #
    def getPreferences(self)->list:
        return self._preferences
    #
     # Method name: getName
     # Formal Parameters: None
     # Return Value: str
     # Usage: returns the name of the applicant
     #
    def getName(self)->str:
        return self._name
    #
     # Method name: setMatch
     # Formal Parameters:
     #  1) [str] position: the position that will be set as the match for the applicant
     # Return Value: None
     # Usage: sets the position as the match for the position
     #
    def setMatch(self,position:str)->None:
        self._match=position
    #
     # Method name: getMatch
     # Formal Parameters: None
     # Return Value: str|None
     # Usage: returns the match of the applicant
     #
    def getMatch(self)->str|None:
        return self._match
    #
     # Method name: checkPriority
     # Formal Parameters:
     #  1) [str] targetposition: the position that is being compared with the matched position to check which the applicant prefers
     # Return Value: bool
     # Usage: checks to see which position the applicant prefers by comparing indexed locations of the position within their preferences
     #
    def checkPriority(self,targetposition:str)->bool:
        matchindex=self._preferences.index(self._match)
        targetindex=self._preferences.index(targetposition)
        return True if matchindex>targetindex else False       # priority decided by index position, the lower the index the higher the preference
#
 # Class Name: Match
 # Class Variables:
 #  1) [dict] data : the dict of the names of applicants and positions with their assigned object data
 #  2) [list] positions : the list of the names of the position for use by the Match class
 #  3) [list] applicants : the list of names of the applicants for use by the Match class
 # Usage: uses the applicant and position data to find a stable match when the stableMatch function is called
 #
class Match:
    def __init__(self,applicants:list,positions:list)->None:
        self._data={}
        self._positions=[]
        self._applicants=[]
        for prospect in applicants:
            self._data[prospect[0]]=applicant(prospect[0],prospect[1:])
            self._applicants.append(prospect[0])
        for opening in positions:
            self._data[opening[0]]=position(opening[0],opening[1],opening[2:])
            self._positions.append(opening[0])
    #
     # Method name: checkMatch
     # Formal Parameters: None
     # Return Value: bool
     # Usage: checks to see if all positions have successfully matched with applicants or not
     #
    def checkMatch(self)->bool:
        for elements in self._positions:
            if not self._data[elements].full():
                return False
        return True
    #
     # Method name: stableMatch
     # Formal Parameters: None
     # Return Value: None
     # Usage: Using the Gale Algorithm, a perfect match is found between the positions available and the applications submitted
     #
    def stableMatch(self)->None:
        while not self.checkMatch():
            for position in self._positions:  
                applicantnumber=0                                                  # used to keep track of the index of the list of preferences from the position
                while not self._data[position].full():
                    studentname=self._data[position].getPreference(applicantnumber)  # pulls up the targeted applicant based on the position's preferences
                    student=self._data[studentname]                                    # targeted student object data pulled from dictionary and assigned
                    if student.getMatch()==None:                                
                        student.setMatch(position)
                        self._data[position].addMatch(student.getName())
                    elif student.checkPriority(position):                          # checkPriority function called to see if the student prefers the target position
                        temp=student.getMatch()
                        student.setMatch(position)
                        self._data[temp].removeMatch(student.getName())
                        self._data[position].addMatch(student.getName())
                    applicantnumber+=1

    #
     # Method name: getMatches
     # Formal Parameters: None
     # Return Value: list
     # Usage: returns the stable matching results
     #
    def getMatches(self)->list:
        matches=[]
        for elements in self._positions:
            matches.append(self._data[elements])
        return matches

    #
     # Method name: __str__
     # Formal Parameters: None
     # Return Value: str
     # Usage: returns a string of the object data when it is printed
     #
    def __str__(self)->str:
        container=''
        for elements in self._positions:
            container+=str(self._data[elements])+'\n'
        return container




                


    