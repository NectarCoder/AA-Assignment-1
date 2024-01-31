#
# Class Name: StabilityChecker
# Class Variables:
#  1) [list] positions : the list of the names of the position for use by the Match class
#  2) [list] applicants : the list of names of the applicants for use by the Match class
#  3) [list] stabilityOutput : the stability matches
# Usage: checks the stability of the matches
#
class StabilityChecker:
    def __init__(self, applicants: list, positions: list, matches: list) -> None:
        self._positions = []
        self._applicants = []
        self._stabilityOutput = []
        for prospect in applicants:
            self._applicants.append(StabilityApplicant(prospect[0], prospect[1:]))
        for position in positions:
            self._positions.append(StabilityPosition(position[0], position[1], position[2:]))
        for match in matches:
            self._stabilityOutput.append(StabilityOutput(match._name, match._match))

    #
    # Method name: stabilityCheckType1
    # Formal Parameters: None
    # Return Value: list of unstability messages
    # Usage:
    # First type of instability: There are students s and s’, and a hospital h, so that
    # s is assigned to h, and s’ is assigned to no hospital, and h prefers s’ to s
    def stabilityCheckType1(self) -> list:
        unstableMatches = []
        assignedApplicants = []
        allApplicants = []

        # I need to get a list of assigned applicants
        for match in self._stabilityOutput:
            assignedApplicants.extend(match.getMatches())

        # I need all the applicants that where not assinged to a position
        for applicant in self._applicants:
            allApplicants.append(applicant.getName())
        unassignedApplicants = list(filter(lambda x: x not in assignedApplicants, allApplicants))

        # First type of instability: Does a hospital have a student assigned that is lower on their
        # wish list than any student that is not assigned?
        for match in self._stabilityOutput:
            position = next((position for position in self._positions if position.getName() == match.getPositionName()))
            result = match.isPositionStable(unassignedApplicants, position)
            if len(result) > 0:
                unstableMatches.append(result)
        return unstableMatches

    #
    # Method name: stabilityCheckType2
    # Formal Parameters: None
    # Return Value: list of unstability messages
    # Usage:
    # Second type of instability: There are students s and s’, and a hospitals h and h’, so that
    # s is assigned to h, and s’ is assigned to h’, and h prefers s’ to s, and s’ prefers h to h’
    def stabilityCheckType2(self) -> list:
        unstableMatches = []

        # Second type of instability: For M=[{H-1,R-3},{H-2,R-4}], both the positions and applicants wish list prefer the other, so it
        # should be M=[{H-1,R-4},{H-2,R-3}] where H-1 prefers R-4 and R-4 prefers H-1 and the same for H-2 and R-3.
        for match in self._stabilityOutput:
            results = match.isEveryOneInAggrement(self._positions, self._applicants)
            if len(results) > 0:
                unstableMatches.extend(results)

        return unstableMatches

    #
    # Method name: stabilityCheckAll
    # Formal Parameters: None
    # Return Value: list of unstability messages
    # Usage: checks for type 1 and type 2 instability
    #
    def stabilityCheckAll(self) -> list:
        unstableMatches = []

        unstableMatches.extend(self.stabilityCheckType1())

        unstableMatches.extend(self.stabilityCheckType2())

        return unstableMatches


#
# Class Name: StabilityPosition
# Class Variables:
#  1) [str] name : the name of the position
#  2) [str] opening : the amount of opened positions of the position
#  3) [list] preference : the list of preferenced applicants by the position
# Usage: stores the data of the position to be used by the stability checker class
#
class StabilityPosition:
    def __init__(self, name: str, opening: int, preferences: list) -> None:
        self._name = name
        self._openings = int(opening)
        self._preferences = preferences

    def getName(self) -> str:
        return self._name

    def getPreferences(self) -> list:
        return self._preferences


#
# Class Name: StabilityApplicant
# Class Variables:
#  1) [str] name : the name of the applicant
#  2) [list] preference : the list of preferences of the student
# Usage: stores the information of the applicant to be used by the stability checker class
#
class StabilityApplicant:
    def __init__(self, name: str, preferences: list) -> None:
        self._name = name
        self._preferences = preferences

    def getName(self) -> str:
        return self._name

    def getPreferences(self) -> list:
        return self._preferences


#
# Class Name: StabilityOutput
# Class Variables:
#  1) [str] name : the positionName of the position
#  2) [list] matches : the list of applicants that are matched to the position
# Usage: stores and validates the stablity of the information of the matches to be used by the stability checker class
#
class StabilityOutput:
    def __init__(self, positionName: str, matches: list) -> None:
        self._positionName = positionName
        self._matches = matches

    # Method name: getPositionName
    # Formal Parameters: None
    # Return Value: str
    # Usage: returns the name of the match postion
    #
    def getPositionName(self) -> str:
        return self._positionName

    # Method name: getMatches
    # Formal Parameters: None
    # Return Value: list
    # Usage: returns the matches of applicants to the position
    #
    def getMatches(self) -> list:
        return self._matches

    #
    # Method name: stabilityCheckType1
    # Formal Parameters: None
    # Return Value: list of unstability messages
    # Usage:
    # First type of instability: There are students s and s’, and a hospital h, so that
    # s is assigned to h, and s’ is assigned to no hospital, and h prefers s’ to s
    def isPositionStable(self, unassignedApplicants: list, position: StabilityPosition) -> str:

        # Find the MIN index of the unassigned applicates
        unassignedIndices = [i for i, item in enumerate(position.getPreferences()) if item in unassignedApplicants]
        minUnassingedIndex = min(unassignedIndices)

        # Find the MAX index of the assigned applicants
        indices = [i for i, item in enumerate(position.getPreferences()) if item in self._matches]
        assignedMaxIndex = max(indices)

        # You should not have any assigned applicant index larger then the unassigned.
        if assignedMaxIndex > minUnassingedIndex:
            return f"Type 1 Instability: {position.getName()} has applicants matched to positions that are lower on their wish list then applicants that did not get matched at all."

        return ""

    #
    # Method name: isEveryOneInAggrement
    # Formal Parameters: None
    # Return Value: list of unstability messages
    # Usage:
    # Second type of instability algorithm: There are students s and s’, and a hospitals h and h’, so that
    # s is assigned to h, and s’ is assigned to h’, and h prefers s’ to s, and s’ prefers h to h’
    def isEveryOneInAggrement(self, positions: list, applicants: list) -> list:
        # I want to return a list of all unstable matches so that we can troubleshoot any issues.
        unstableMatches = []

        # Get the hospital that is associated with this Match - self._positionName
        currentPosition = next((position for position in positions if position.getName() == self._positionName))

        # Step 1: For each match, lets determine if there is another hospital that has this applicant higher in their wish list.
        for currentApplicantName in self._matches:
            # Find the wish list index of the current applicant within the self._positionName position
            indexOfCurrentApplicantInPositionWishList = next(
                i for i, item in enumerate(currentPosition.getPreferences()) if item == currentApplicantName)
            # Iterate across all other positions and find their wish list index of the current applicant.
            for otherPosition in positions:
                if otherPosition.getName() != self._positionName:
                    indexOfTheOtherPositionsApplicant = next(
                        i for i, item in enumerate(otherPosition.getPreferences()) if item == currentApplicantName)
                    # If there is another postion that had this applicant higher in their wish list, then we need to see what the applicant prefers.
                    if indexOfCurrentApplicantInPositionWishList > indexOfTheOtherPositionsApplicant:
                        # Find the applicant in question and see who they prefer
                        applicantInQuestion = next(
                            (applicant for applicant in applicants if applicant.getName() == currentApplicantName))
                        indexOfCurrentApplicantsPosition = next(
                            i for i, item in enumerate(applicantInQuestion.getPreferences()) if
                            item == self._positionName)
                        indexOfTheOtherApplicantsPosition = next(
                            i for i, item in enumerate(applicantInQuestion.getPreferences()) if
                            item == otherPosition.getName())
                        if indexOfCurrentApplicantsPosition > indexOfTheOtherApplicantsPosition:
                            # We have an instability! self._positionName had the current applicant lower in their wish list then the other position and the applicant
                            # had the other position higher in their wish list than the current position. Put another way, they are swapped!!   
                            unstableMatches.append(
                                f"Type 2 Instability: For, M={{{currentPosition.getName()},{','.join(self._matches)}}}. {otherPosition.getName()} prefers {currentApplicantName} over {currentPosition.getName()}, and {currentApplicantName} prefers {otherPosition.getName()} over the currently matched {currentPosition.getName()}")

        return unstableMatches
