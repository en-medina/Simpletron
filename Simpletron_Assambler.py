__author__ = 'Enmanuel Medina'

"""
     SIMPLETRON ASSAMBLER
---------------------------------------------------------------------------
"""

"""        Simpletron Assambler
****************************************"""

def Simpletron_Assambler():
    WelcomeMessage()
    ubication = ""
    ubication = raw_input()

    if ubication == "\\_runningprogramming":
        print "ok"
    else:
        _AssambleIt(ubication)

"""
     PRINCIPAL ASSAMBLER FUNCTION
---------------------------------------------------------------------------
"""
"""         Assambler function
****************************************"""
def _AssambleIt(ubication):
    _runmode = chk_mode(ubication)
    _AssambleIt.pc = 0
    FirstInstruction = False
    for command in searchfile(ubication):
        _AssambleIt.pc += 1
        command = CommentAnalizer(command)
        if command == "" or ("#MODE" in command and not FirstInstruction):
            continue
        if _runmode == mode.auto:
            _AssambleIt.assambler[_AutoAssambler.pc] = _AutoAssambler(command)
        elif _runmode == mode.manual:
            _AssambleIt.assambler[_ManualAssambler.pc] = _ManualAssambler(command)
        FirstInstruction = True
    _AssamblerPresentation()
    savefile(ubication)
    return
_AssambleIt.pc = 0
_AssambleIt.assambler = ["0000" for c in range(100)]
"""
    GUI MANAGER FUNCTIONS
---------------------------------------------------------------------------
"""

"""         Welcome Messager
****************************************"""
def WelcomeMessage():
    print"""
*** Welcome to simpletron's compiler***
please write the ubication of your program to compiler
or type:
        \\_runningprogramming
to do your program in on live compiling
    """
    return


"""         Assambler Presentation
****************************************"""

def _AssamblerPresentation():
    print "\t\tMEMORY:\n\t\t",
    for c in range(10):
        print "\t ", str(c),
    print ""

    for c in range(10):
        print "\t\t",
        if c == 0:
            print str(c*10)+"0",
        else:
            print str(c*10),
        print "\t",
        for d in range(10):
            a = int(_AssambleIt.assambler[d+c*10])
            signal = "+"
            if a < 0:
                signal = "-"
            print signal + str(_AssambleIt.assambler[d+c*10]), "\t",
        print ""

"""
    FILE MANAGER FUNCTIONS
---------------------------------------------------------------------------
"""

"""         File discovery
****************************************"""
def searchfile(directory):
    """
    Serching the file that is going to compile
    """
    fx = file
    #Check if that file exist
    try:
        fx = open(directory, 'r')
    #unknow file ubication
    except:
         errorfound(-1003, "")

    #return a list of command
    commands = []
    for c in fx.readlines():
        r = c.strip()
        r = r.upper()
        commands.append(r)
    return commands

"""         File Save
****************************************"""
def savefile(ubication):
    NewUbi=""
    if "." in ubication:
        NewUbi = ubication[:ubication.index(".")]
    else:
         NewUbi = ubication
    NewUbi += ".sml"
    f1 = open(NewUbi, "w")
    for c in _AssambleIt.assambler:
        f1.write(c)
    f1.close()

"""
    MODE IDENTIFIERS FUNCIONS
---------------------------------------------------------------------------
"""

"""         Mode identifier
****************************************"""
def mode(instruction):
    """
    Mode of compile of simpletron
    """
    if instruction == "":
        return mode.auto
    word = ""
    instruction = instruction.replace('\t', ' ')
    word = Delete_space(instruction.split(" "))
    if len(word) != 2:
        errorfound(-1002, instruction)

    if word[0] != "#MODE":
         errorfound(-1002, instruction)
    command = word[1]

    #Automatic program counter
    if command == "AUTO":
        return mode.auto

    #Manual program counter
    elif command == "MANUAL":
        return mode.manual
    #unknow command
    else:
         errorfound(-1002, instruction)
mode.auto = 1
mode.manual = 2

"""         Mode Checker
****************************************"""
def chk_mode(ubication):
    for c in searchfile(ubication):
        _AssambleIt.pc += 1
        if c == "":
            continue
        elif "#MODE" in c:
            return mode(CommentAnalizer(c))
        elif "//" in c:
            continue
        else:
            return mode("")

"""
    COMMAND ANALIZER FUNCIONS
---------------------------------------------------------------------------
"""

"""         Auto Assambler Analizer
****************************************"""
def _AutoAssambler(instruction):
    _AutoAssambler.pc += 1
    instruction = instruction.replace('\t', ' ')
    separate = Delete_space(instruction.split(" "))
    if not SpecialCase(instruction):
        if len(separate) != 2:
            errorfound(-1007, instruction)
        return Command(separate[0].strip(" ")) + checkNumber(separate[1].strip(" "))
    if len(separate) != 1:
        errorfound(-1007, instruction)
    return Command(separate[0].strip(" ")) + "00"
_AutoAssambler.pc = -1

"""         Manual Assambler Analizer
****************************************"""
def _ManualAssambler(instruction):
    instruction = instruction.replace('\t', ' ')
    separate = Delete_space(instruction.split(" "))
    if not SpecialCase(instruction):
        if len(separate) != 3:
            errorfound(-1006, instruction)

        _ManualAssambler.pc = int(checkNumber(separate[0].strip(" ")))

        return Command(separate[1].strip(" "))+checkNumber(separate[2].strip(" "))

    if len(separate) != 2:
        errorfound(-1006, instruction)

    _ManualAssambler.pc = int(checkNumber(separate[0].strip(" ")))

    return Command(separate[1].strip(" "))+"00"
_ManualAssambler.pc = 0

"""         Special Function Detector
****************************************"""
def SpecialCase(instruction):
    if "HALF" in instruction:
        return True
    return False
"""         Command Cleaner
****************************************"""
def Delete_space(a):
    clean =[]
    for c in a:
        if c == "":
            continue
        clean.append(c)
    return clean

"""         Integer Checker
****************************************"""
def checkNumber(a):
    num = 0
    try:
        num = int(a)
    except:
        errorfound(-1004, a)
    if num < 0 or num >= 100:
        errorfound(-1005, a)
    if num < 10 and len(a) == 1:
        a = "0"+a
    return a

"""         Comment Analizer
****************************************"""
def CommentAnalizer(a):
    if "//"in a:
        pos = a.index("//")
        return a[:pos]
    return a
"""         Command identifier
****************************************"""
def Command(command):
    """
This are the commands that the simpletron understand
    """
    word = command
    # Inputs/outputs operations
    if word == "READ":
        return "10"
    elif word == "WRITE":
        return "11"

    #Load and Store operations
    elif word == "LOAD":
        return "20"
    elif word == "STORE":
        return "21"

    #Arithmetic operations
    elif word == "ADD":
        return "30"
    elif word == "SUBTRACT":
        return "31"
    elif word == "DIVIDE":
        return "32"
    elif word == "MULTIPLY":
        return "33"

    #Transfer of control operations
    elif word == "BRANCH":
        return "40"
    elif word == "BRANCHNEG":
        return "41"
    elif word == "BRANCHZERO":
        return "42"
    elif word == "HALF":
        return "43"
    #Unknow command
    errorfound(-1001, word)

"""
    ERRORS DETECTION FUNCION
---------------------------------------------------------------------------
"""
def errorfound(error, line):
    ErrorsDictionary = {
         -1001: ("Unknown Command"),
         -1002: ("The word \"#MODE\" did not found or is not a valid MODE"),
         -1003: ("Unknown file ubication"),
         -1004: ("That is not an integer number"),
         -1005: ("That integer number is greater than 99 or lower than 0"),
         -1006: ("The instruction is not valid in Manual Mode"),
         -1007: ("The instruction is not valid in Automatic Mode"),
         }
    print "\t\tERROR", str(error)
    print ErrorsDictionary[error]+"."
    if _AssambleIt.pc != 0:
        print "On line", str(_AssambleIt.pc),
    if len(line) != 0:
        print "is wrote:", "\"" + line + "\"",
    exit()

Simpletron_Assambler()

#sys.argv
