import unittest
from command import *

class TestCommandArgument(unittest.TestCase):

    def test_valid_string_argument(self):
        arg = CommandArgument("name", True, "str")
        result = arg.parseString("test")
        self.assertEqual(result, ["test", True])

    def test_invalid_int_argument(self):
        arg = CommandArgument("count", True, "int")
        result = arg.parseString("abc")
        self.assertEqual(result[1], False)
        self.assertTrue("ValueError" in result[0])

    def test_valid_bool_argument(self):
        arg = CommandArgument("active", True, "bool")
        result = arg.parseString("true")
        self.assertEqual(result, [True, True])

    def test_invalid_bool_argument(self):
        arg = CommandArgument("flag", True, "bool")
        result = arg.parseString("invalid")
        self.assertEqual(result[1], False)
        self.assertTrue("ValueError" in result[0])

    def test_valid_list_string_argument(self):
        arg = CommandArgument("names", True, "list[str]")
        result = arg.parseString("alice, bob, charlie")
        self.assertEqual(result, [["alice", "bob", "charlie"], True])

    def test_invalid_list_int_argument(self):
        arg = CommandArgument("numbers", True, "list[int]")
        result = arg.parseString("1, 2, abc")
        self.assertEqual(result[1], False)
        self.assertTrue("ValueError" in result[0])

    def test_valid_list_bool_argument(self):
        arg = CommandArgument("flags", True, "list[bool]")
        result = arg.parseString("true, false, 1, no")
        self.assertEqual(result, [[True, False, True, False], True])

    def test_invalid_type_argument(self):
        with self.assertRaises(ValueError):
            arg = CommandArgument("invalid", True, "invalid_type")

class TestCommand(unittest.TestCase):

    def test_command_syntax_generation(self):
        args = [
            CommandArgument("arg1", True, "str"),
            CommandArgument("arg2", False, "int"),
            CommandArgument("arg3", True, "list[bool]")
        ]
        command = Command(1, "test", args, "Test command", lambda x: None)
        syntax_str = command.getSyntaxStr()
        expected_syntax = "Command Syntax for test\n"
        expected_syntax += "test <arg1> [arg2] <arg3> \n"
        self.assertEqual(syntax_str, expected_syntax)

    def test_command_initialization(self):
        args = [
            CommandArgument("arg1", True, "str"),
            CommandArgument("arg2", False, "int"),
            CommandArgument("arg3", True, "list[bool]")
        ]
        command = Command(1, "test", args, "Test command", lambda x: None)
        self.assertEqual(command.id, 1)
        self.assertEqual(command.name, "test")
        self.assertEqual(command.syntax, args)
        self.assertEqual(command.desc, "Test command")
        self.assertTrue(callable(command.func))

    def test_command_invalid_syntax(self):
        with self.assertRaises(ValueError):
            args = [
                CommandArgument("arg1", True, "str"),
                CommandArgument("arg2", False, "invalid_type"),
                CommandArgument("arg3", True, "list[bool]")
            ]
            Command(1, "test", args, "Test command", lambda x: None)

if __name__ == '__main__':
    #unittest.main()
    args = [
        CommandArgument("str", "Adding a test for command syntax validation Example: Implementing a new method in the Command class. This is arg1", True, "str"),
        CommandArgument("int", "Adding a test for command syntax validation Example: Implementing a new method in the Command class. This is arg2", True, "int"),
        CommandArgument("bool[]", "Adding a test for command syntax validation Example: Implementing a new method in the Command class. This is arg3", False, "list[bool]")
    ]
    command = Command(1, "test", args, "Test command", lambda x:print(f"str: {type(x[0])}, {x[0]}; int: {type(x[1])}, {x[1]}; bool: {type(x[2])}, {x[2]}"))
    syntax_str = command.getSyntaxStr()
    print(syntax_str)
    cmd = CommandLine()
    cmd.addCommand(command)
    cmd.parseInput(input("Enter command: "))

