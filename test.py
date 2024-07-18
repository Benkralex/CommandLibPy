from command import *

if __name__ == '__main__':
    # Create a new command line
    commandLine = CommandLine()

    #add x + y command
    def add(args: list[object]) -> None:
        if len(args) == 2:
            print(args[0] + args[1])
        elif len(args) == 3:
            print(args[0] + args[1] + args[2])
    commandLine.addCommand(Command(0, "add", [CommandArgument("x", "The first number", True, "int"), CommandArgument("y", "The second number", True, "int"), CommandArgument("z", "The third number", False, "int")], "Adds two numbers", add))

    #sqrt x command
    def sqrt(args: list[object]) -> None:
        print(args[0] ** 0.5)
    commandLine.addCommand(Command(1, "sqrt", [CommandArgument("x", "The number", True, "int")], "Calculates the square root of a number", sqrt))

    def benjamin(args: list[object]) -> None:
        print(f'Benjamin is a {args[0] if len(args) == 1 else ""} cool guy')

    commandLine.addCommand(Command(2, "benjamin", [CommandArgument("adjective", "The adjective", False, "str")], "Prints a message about Benjamin", benjamin))

    def greet(args: list[object]) -> None:
        if len(args) == 1:
            print(f'Hello, {args[0]}!')
        else:
            print(f'Hello, World!')
    
    commandLine.addCommand(Command(3, "greet", [CommandArgument("name", "The name", False, "str")], "Greets a person", greet))

    def falko(args: list[object]) -> None:
        print(f'Falko is a {args[0] if len(args) == 1 else ""} cool guy')

    commandLine.addCommand(Command(4, "falko", [CommandArgument("adjective", "The adjective", False, "str")], "Prints a message about Falko", falko))

    while True:
        inp = input("Enter command: ")
        if inp == "exit":
            break
        commandLine.parseInput(inp)
