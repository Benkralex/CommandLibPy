# command.py
# Author: Benkralex

class TextStyler:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    RESET = "\033[0m"

    def wrap_text(text, max_line_length=87, indent=True):
        """
        Wraps text to a maximum line length with optional indentation.
        """
        words = text.split()
        wrapped_text = ""
        current_line = ""
        indent_spaces = "    " if indent else ""
        for word in words:
            if len(current_line) + len(word) + 1 <= max_line_length:
                current_line += (" " + word if current_line else indent_spaces + word)
            else:
                wrapped_text += current_line + "\n"
                current_line = indent_spaces + word
        if current_line:
            wrapped_text += current_line
        return wrapped_text

#CommandArg-Class -> Arguments for the Command-Class
class CommandArgument:
    def __init__(self, name:str, desc:str="", requierd: bool=True, type:str="str") -> None:
        """
        Types:
        - str
        - int
        - bool
        - list[str]
        - list[int]
        - list[bool]
        """
        if not (type in ["str", "int", "bool", "list[str]", "list[int]", "list[bool]"]):
            raise ValueError("Wrong Argument-Type: " + type)
        self.name = name
        self.requierd = requierd
        self.type = type
        self.desc = desc
        
    def __parseStringToList(self, s: str) -> list:
        """
        parses a string to a list
        """
        s = s.strip('() ')
        elements = [elem.strip() for elem in s.split(',')]
        return elements
    
    def parseString(self, s: str) -> list[object]:
        """
        returns a list with the parsed argument and a boolean, that indicates if the parsing was successful
        """
        t: str = self.type
        if t == "str":
            return [s, True]
        elif t == "int":
            try:
                return [int(s), True]
            except ValueError:
                return [("ValueError: " + s + " must be a vaild integer"), False]
        elif t == "bool":
            if s.lower() in ("true", "t", "1", "yes", "y"):
                return [True, True]
            elif s.lower() in ("false", "f", "0", "no", "n"):
                return [False, True]
            else:
                return [("ValueError: " + s + " must be a vaild boolean"), False]
        elif t == "list[str]":
            return [self.__parseStringToList(s), True]
        elif t == "list[int]":
            try:
                return [([int(x) for x in self.__parseStringToList(s)]), True]
            except ValueError:
                return [("ValueError: " + s + " must all be valid intergers"), False]
        elif t == "list[bool]":
            l: list[str] = self.__parseStringToList(s)
            bool_l: list[bool] = []
            for i in l:
                if i.lower() in ("true", "t", "1", "yes", "y"):
                    bool_l.append(True)
                elif i.lower() in ("false", "f", "0", "no", "n"):
                    bool_l.append(False)
                else:
                    return [("ValueError: " + s + " must all be vaild booleans"), False]
            return [bool_l, True]
        raise Exception("Wrong Argument-Type: " + t)
    
    def isReq(self) -> bool:
        """
        returns True if the argument is required
        """
        return self.requierd
    
    def getType(self) -> str:
        """
        returns the type of the argument
        """
        return self.type

    def getName(self) -> str:
        """
        returns the name of the argument
        """
        return self.name
    
    def getDesc(self) -> str:
        """"
        returns the description of the argument
        """
        return self.desc

#Command-Class
class Command:
    def __init__(self, id: int, name: str, syntax: list[CommandArgument], desc: str, func) -> None:
        self.id = id
        self.name = name
        self.syntax = syntax
        self.desc = desc
        self.func = func
        self.minArgsLength: int = 0
        for arg in self.syntax:
            if arg.isReq():
                self.minArgsLength += 1

    def getSyntaxStr(self) -> str:
        """
        returns a string with the syntax of the command
        """
        syntaxStr: str = TextStyler.GREEN + "\n---------------------------------------------------------------------------------------\n"
        syntaxStr += "Command Syntax for " + TextStyler.YELLOW + self.name + TextStyler.GREEN + ":\n\n"
        syntaxStr += TextStyler.YELLOW + self.name + TextStyler.GREEN
        firstArg: bool = True
        ArgDesc: str = "\n\n"
        for arg in self.syntax:
            if not firstArg:
                syntaxStr += ","
            else:
                firstArg = False
            if arg.isReq():
                name: str = TextStyler.RED + " <" + arg.getName() + ">" + TextStyler.GREEN
            elif not arg.isReq():
                name: str = TextStyler.CYAN + " [" + arg.getName() + "]" + TextStyler.GREEN
            syntaxStr += name
            ArgDesc += name + ":\n" + TextStyler.wrap_text(arg.getDesc().replace("\n", "\n")) + "\n"
        syntaxStr += ArgDesc
        return syntaxStr + "\n---------------------------------------------------------------------------------------\n" + TextStyler.RESET
    
    def parseStringToArguments(self, s: str) -> list[object]:
        """
        returns a list with the parsed arguments and a boolean, that indicates if the parsing was successful
        """
        args: list[str] = self.split_string_except_parentheses(s.split(" ", 1)[1])
        if len(args) < self.minArgsLength:
            return [("ValueError: " + self.name + " needs at least" + str(self.minArgsLength) + " arguments"), False]
        argList: list[object] = []
        for i in range(len(args)):
            arg: list[object] = self.syntax[i].parseString(args[i])
            if not arg[1]:
                return arg
            argList.append(arg[0])
        return [argList, True]

    def split_string_except_parentheses(self, s: str) -> list[str]:
        """
        splits a string by commas, but ignores commas inside parentheses
        """
        segments = []
        start_index = 0
        parentheses_count = 0
        for i, char in enumerate(s):
            if char == '(':
                parentheses_count += 1
            elif char == ')':
                parentheses_count -= 1
            elif char == ',' and parentheses_count == 0:
                segments.append(s[start_index:i].strip())
                start_index = i + 1
        segments.append(s[start_index:].strip())  # Add the last segment
        return segments

    def execute(self, s: str) -> None:
        """
        executes the command
        """
        args: list[object] = self.parseStringToArguments(s)
        if not args[1]:
            print(args[0])
            return
        self.func(args[0])

    def getDesc(self) -> str:
        """
        returns the description of the command
        """
        return self.desc

    def getName(self) -> str:
        """
        returns the name of the command
        """
        return self.name

#CommandLine-Class --> a virtual Comandline, that you can pass the user Input and it respondes with help, executes functions
class CommandLine:
    def __init__(self) -> None:
        self.commands: list[Command] = []

    def addCommand(self, command: Command) -> None:
        """
        adds a command to the CommandLine
        """
        self.commands.append(command)

    def commandExists(self, name: str) -> bool:
        """
        returns True if the command exists
        """
        for command in self.commands:
            if command.getName() == name:
                return True
        return False
    
    def parseInput(self, s: str) -> None:
        """
        parses the input and executes the command
        """
        args: list[str] = s.split()
        if not self.commandExists(args[0]):
            print("Command not found")
            return
        for command in self.commands:
            if command.getName() == args[0]:
                command.execute(s)
    #args in liste
    #welcher command
    #help/info
    #autocomplet

