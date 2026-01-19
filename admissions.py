#This class is used to create an object that stores the document data

class studentDataClass:
    def __init__(self):
        self.stats = []
        self.grades = []
        self.names = []
        self.scores = []

def check_row_types(row):
    """
    # Provided code
    # This function checks to ensure that a list is of length
    # 8 and that each element is type float
    # Parameters:
    # row - a list to check
    # Returns True if the length of row is 8 and all elements are floats
    """
    if len(row) != 8:
        print("Length incorrect! (should be 8): " + str(row))
        return False
    ind = 0
    while ind < len(row):
        if type(row[ind]) != float:
            print("Type of element incorrect: " + str(row[ind]) + " which is " + str(type(row[ind])))
            return False
        ind += 1
    return True
	
# define your functions here

def convert_row_type(allDocInfo):
    """
    This function sorts through the raw document data, converts it to rows,
    and then returns both studentInfo and studentNames for further processing
    """
    studentInfo = []
    studentNames = []
    for i in range(len(allDocInfo)):
        studentInfo.append(allDocInfo[i].split(","))
    for x in range(len(studentInfo)):
        studentNames.append(studentInfo[x][0])
        studentInfo[x].pop(0)
        for y in range(len(studentInfo[x])):
            studentInfo[x][y] = float(studentInfo[x][y])
    return studentInfo, studentNames

def calculateScore(studentStats,test=False):
    """
    This function uses the given formula and given weight-scale to calculate the score
    If test == True, function will return an array of calculated, unweighted scores.
    Else, it weights them, adds them, and returns as one number
    """
    equalizerFormula = [1/160,2,1,1]
    weightScale = [0.3,0.4,0.1,0.2]
    scores = []
    for x in range(len(studentStats)):
        #If it is a test, their algorithm doesn't weight scale. Just equalized.
        if(test):
            scores.append(studentStats[x]*equalizerFormula[x])
        else:
            scores.append(studentStats[x]*equalizerFormula[x]*weightScale[x])
    if(test):
        return scores
    else:
        addedScore = 0
        for i in scores:
            addedScore += i
        return addedScore

def convertAllData(allDocInfo):
    """
    This function converts the data and rows, and stores it in an object made
    using the studentDataClass(). This object then is returned and is accessed in the rest of the program.

    Instead of having loose code and 2 functions, the 
    row formatting functions are in one overall conversion function.
    """
    studentData = studentDataClass()
    studentInfo, studentNames = convert_row_type(allDocInfo)
    #here the row_type can be checked. But it already has been
    for i in range(len(studentInfo)):
        studentData.stats.append(studentInfo[i][:4])
        studentData.grades.append(studentInfo[i][4:])
        studentData.names.append(studentNames[i])
    return studentData

def isOutlier(studentStats):
    """
    This function, using the parameters given for an 'outlier,'
    will calculate and compare scores. Only, calculateScore with a parameter of True
    returns the scores unadded, allowing for comparison. Returns True or False
    """
    scores = calculateScore(studentStats, True)
    gpa = scores[1]
    sat = scores[0]
    interest = scores[2]
    barToMeet = 2
    if(interest == 0 or (gpa -barToMeet) > sat):
        return True
    else:
        return False
    
def calculate_score_improved(studentStats):
    """
    This function calls the calculateScore and isOutlier function, returns True or False
    """
    score = calculateScore(studentStats)
    if(isOutlier(studentStats) or score >= 6):
        return True
    else:
        return False
    
def findLowestInArray(array):
    """
    This function takes any array and then returns the lowest value in that array.
    """
    lowestA = 0
    competitionA = -1
    for i in range(len(array)):
        if(i == 0):
            lowestA = array[i]
        elif(array[i] < lowestA):
            competitionA = array[i]
        if(lowestA > competitionA and competitionA > -1):
            lowestA = competitionA
    return lowestA

def grade_outlier(gradesList):
    """
    Determines if the lowest grade is an outlier, and then return True or False
    """
    lowestGrade = findLowestInArray(gradesList)
    lowestGradeIndex = gradesList.index(lowestGrade)
    isLowerThan = 0
    for i in range(len(gradesList)):
        if i != lowestGradeIndex:
            if lowestGrade < gradesList[i]-20:
                isLowerThan+=1
    return isLowerThan == 3

def grade_improvement(gradesList):
    """
    This function takes a list of grades [a,b,c,d], and the organizes them and 
    puts them into a new list (orderedGradesList) for comparison

    returns True or False
    """
    gradesListSub = gradesList.copy()
    orderedGradesList = []
    while(len(gradesListSub)>0):
        lowest = findLowestInArray(gradesListSub)
        orderedGradesList.append(lowest)
        lowestIndex = gradesListSub.index(lowest)
        gradesListSub.pop(lowestIndex)
    return orderedGradesList == gradesList

def main():
    """
    This function is where the code interacts with the file, calls functions, and loops
    through the studentData lists to append to new files based off the requirements
    """
    filename = "admission_algorithms_dataset.csv"
    input_file = open(filename, "r")    
    
    print("Processing " + filename + "...")
    # grab the line with the headers
    headers = input_file.readline()
    
    allDocInfo = input_file.readlines()
    studentData = convertAllData(allDocInfo)

    scoresFile = open("student_scores.csv","w")
    chosenStudentFile = open("chosen_students.csv","w")
    outLierFile = open("outliers.csv","w")
    chosenImprovedFile = open("chosen_improved.csv","w")
    betterImprovedFile = open("better_improved.csv","w")
    compositeChosenFile = open("composite_chosen.csv", "w")

    for i in range(len(studentData.stats)):
        score = calculateScore(studentData.stats[i])
        studentData.scores.append(round(score,2))
        scoresFile.write(f"{studentData.names[i]},{studentData.scores[i]:.2f}\n")
        if studentData.scores[i] >= 6:
            chosenStudentFile.write(f"{studentData.names[i]}\n")
        if isOutlier(studentData.stats[i]):
            outLierFile.write(f"{studentData.names[i]}\n")
        if studentData.scores[i] >= 6 or studentData.scores[i] >= 5 and isOutlier(studentData.stats[i]):
            chosenImprovedFile.write(f"{studentData.names[i]}\n")
        if(calculate_score_improved(studentData.stats[i])):
            betterImprovedFile.write(f"{studentData.names[i]},")
            for x in range(len(studentData.stats[i])):
                betterImprovedFile.write(f"{studentData.stats[i][x]}")
                if x == (len(studentData.stats[i])-1):
                    betterImprovedFile.write("\n")
                else:
                    betterImprovedFile.write(",")
        if(grade_outlier(studentData.grades[i]) or grade_improvement(studentData.grades[i]) or isOutlier(studentData.stats[i])):
            if(studentData.scores[i] >= 5):
                compositeChosenFile.write(f"{studentData.names[i]}\n")
        elif(studentData.scores[i] >= 6):
                compositeChosenFile.write(f"{studentData.names[i]}\n")

    scoresFile.close()
    chosenStudentFile.close()
    outLierFile.close()
    chosenImprovedFile.close()
    betterImprovedFile.close()
    compositeChosenFile.close()

    print("Done!")

# this bit allows us to both run the file as a program or load it as a
# module to just access the functions
if __name__ == "__main__":
    main()



