__author__ = 'Enmanuel Medina'

"""
    Simpletron Operantion
---------------------------------------------------------------------------
"""

"""         SIMPLETRON OPERATION CODE
****************************************"""

def ADD(Address):
    Interpreter.ACC += Interpreter.Memory[Address]
    ACC_checker()
    return

def SUBB(Address):
    Interpreter.ACC -= Interpreter.Memory[Address]
    ACC_checker()
    return

def LOAD(Address):
    Interpreter.ACC = Interpreter.Memory[Address]

def STORE(Address):
    Interpreter.Memory[Address] = Interpreter.ACC

def DIVIDE(Address):
    try:
        Interpreter.ACC /= Interpreter.Memory[Address]
    except:
        errorfound(-1010, "")
        return False

def MULTIPLY(Address):
    Interpreter.ACC *= Interpreter.Memory[Address]
    ACC_checker()

def BRANCH(Address):
    Interpreter.PC = Address
    Interpreter.PC -= 1

def BRANCHNEG(Address):
    if Interpreter.ACC < 0:
        BRANCH(Address)

def BRANCHZERO(Address):
    if Interpreter.ACC == 0:
        BRANCH(Address)

def HALF(Address):
    Interpreter.PC -= 1
    return True

def READ(Address):
    read = 0
    while True:
        try:
            read = int(raw_input("Write down a number: "))
        except:
            print "That is not a number"
            continue
        if abs(read) > 9999:
            print "The absolute value of that number is greater than 9999"
        else:
            break
    Interpreter.Memory[Address] = read
    return

def WRITE(Address):
    Interpreter.OutPut += Int_to_String(Interpreter.Memory[Address]) + "\n"
    return

# print "0"*(4-len (str(a))) + str(a)

"""
    Simpletron Interpreter
---------------------------------------------------------------------------
"""
def Interpreter():
    temp = []
    while temp == []:
        temp = searchfile()
    Interpreter.Memory = temp
    options = ""
    Show_State_Flag = False
    Half_Found = None
    while options != '4':
        if Interpreter.Error:
            print "Please check your code and reassamble it"
        MainScreen()
        if Half_Found:
            print "A Half was found"
        if Show_State_Flag:
            Show_State_Flag = False
            Show_State()

        print "Program Ouput: "
        print Interpreter.OutPut

        options = raw_input("Type one of this numbers: ")

        if options == '1' and not Half_Found and not Interpreter.Error:
            Half_Found = Execute()
        elif options == '2' and not Half_Found and not Interpreter.Error:
            Half_Found = Execute_All()
        elif options == '3':
            Show_State_Flag = True
        elif options != '4':
            print "That is not a correct option"
    return

Interpreter.Error = False
Interpreter.ACC = 0
Interpreter.PC = 0
Interpreter.Memory = [100]
Interpreter.OutPut = ""
Interpreter.Operations = {
    10: (READ, "READ"),
    11: (WRITE, "WRITE"),
    20: (LOAD, "LOAD"),
    21: (STORE, "STORE"),
    30: (ADD, "ADD"),
    31: (SUBB, "SUBTRACT"),
    32: (DIVIDE, "DIVIDE"),
    33: (MULTIPLY, "MULTIPLY"),
    40: (BRANCH, "BRANCH"),
    41: (BRANCHNEG, "BRANCHNEG"),
    42: (BRANCHZERO, "BRANCHZERO"),
    43: (HALF, "HALF")
}


"""         EXECUTE STEP BY STEP FUNCTION
****************************************"""
def Execute():
    Instruction = Interpreter.Memory[Interpreter.PC]
    chk = None
    if Interpreter.Operations.has_key(Instruction/100):
        chk = Interpreter.Operations[Instruction/100][0](Instruction % 100)
        if chk == False:
            Interpreter.Error = True
    else:
        errorfound(-1011, Instruction/100)
        Interpreter.Error = True
    Interpreter.PC += 1
    PC_CHK()
    return chk


"""         EXECUTE ALL FUNCTION
****************************************"""
def Execute_All():
    chk = None
    while not chk:
        chk = Execute()
        if Interpreter.Error:
            return False
    return True


"""
    GUI CONTROLLER FUNCTIONS
---------------------------------------------------------------------------
"""

"""         SHOW STATE FUNCTION
****************************************"""
def Show_State():
    print"\t\tAccumulator\t\t\t\t", Int_to_String(Interpreter.ACC)
    print "\t\tProgram Counter\t\t\t", zero_add(Interpreter.PC)
    print "\t\tInstruction Register\t", Int_to_String(Interpreter.Memory[Interpreter.PC])
    print "\t\tOperation Code\t\t\t", zero_add(Interpreter.Memory[Interpreter.PC] / 100), "  Operation Name:",
    if Interpreter.Operations.has_key(Interpreter.Memory[Interpreter.PC] / 100):
        print "\"" + Interpreter.Operations[Interpreter.Memory[Interpreter.PC] / 100][1] + "\""
    else:
        print "\"Unknow\""
    print "\t\tOperand \t\t\t\t", zero_add(Interpreter.Memory[Interpreter.PC] % 100),
    if abs(Interpreter.Memory[Interpreter.PC] % 100) < 100:
        print ""
    else:
        print "  Unknow Operand"
    _MemoryPresentation()

"""         MAIN SCREEN
****************************************"""
def MainScreen():
    print """
    Choose one of those numbers
            MENU
    1 - Execute step by step
    2 - Execute all
    3 - Show State
    4 - Quit
    """

"""         Memory Presentation
****************************************"""
def _MemoryPresentation():
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
            print Int_to_String(Interpreter.Memory[d+c*10]), "\t",
        print ""


"""
    FILE CONTROLLER FUNCTIONS
---------------------------------------------------------------------------
"""

"""         File discovery
****************************************"""

def searchfile():
    fx = file
    directory = raw_input("Please, type the ubication of the sml file: ")
    # Check if that file exist
    try:
        fx = open(directory, 'r')
    # unknow file ubication
    except:
        errorfound(-1003, "")
        return []
    listd = ""
    for c in fx.readlines():
        if c != "\n" and c != " " and c != "\t":
            listd += c
    fx.close()

    lenlistd = len(listd)
    if lenlistd % 4 != 0 and lenlistd != 400:
        errorfound(-1008, "")
        return []

    instruction = []
    temp = ""
    counter = 0
    for c in listd:
        if counter != 4:
            temp += c
        else:
            counter = 0
            try:
                instruction.append(int(temp))
            except:
                errorfound(-1008, "")
                return []
            temp = c
        counter += 1
    instruction.append(int(temp))
    return instruction


"""
    ERROR HANDLE FUNCTIONS
---------------------------------------------------------------------------
"""

"""         Error found
****************************************"""
def errorfound(error, line):
    line = str(line)
    print "\t\tERROR", str(error)
    print errorfound.ErrorsDictionary[error] + "."
    if Interpreter.PC != 0:
        print "On position:", str(Interpreter.PC)
    if len(line) != 0:
        print "is wrote:", "\"" + line + "\""
    Interpreter.PC = 0
    return
errorfound.ErrorsDictionary = {
         -1003: ("Unknown file ubication"),
         -1004: ("That is not an integer number"),
         -1005: ("That integer number is greater than 99 or lower than 0"),
         -1008: ("That is a crashed file, please assambler it again"),
         -1010: ("The division with zero is undefined, please check your code an ressamble again"),
         -1011: ("In that position there is not a correct instruction, please check your code an reassamble again")
         }

"""
    SIMPLETRON EXTRA FUNCTIONS
---------------------------------------------------------------------------
"""
"""         SIMPLETRON CHECKER FUNCTIONS
****************************************"""
def Int_to_String(num):
    if num < 0:
        num = abs(num)
        return "-" + "0" * (4 - len(str(num))) + str(num)
    else:
        return "+" + "0" * (4 - len(str(num))) + str(num)

def ACC_checker():
    Interpreter.ACC %= 10000

def PC_CHK():
    if Interpreter.PC == 100:
        Interpreter.PC = 0

def zero_add(num):
    if 0 <= num < 10:
        return "0" + str(num)
    elif 0 > num > -10:
        return "-" + "0" + str(abs(num))
    else:
        return str(num)

Interpreter()
