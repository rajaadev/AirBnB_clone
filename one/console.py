#!/usr/bin/python3
"""Command Line Interpreter"""

import cmd
import json
import re
import sys
from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_EOF(self, line):
        """Usage: EOF
           Function: Exits the program
        """
        print()
        return True

    def do_quit(self, line):
        """Usage: quit
           Function: Exits the program
        """
        return True

    def do_create(self, line):
        """Usage: create <class name>
           Function: Creates an instance of the class
        """
        if not line:
            print("** class name missing **")
            return

        if line not in storage.classes():
            print("** class doesn't exist **")
        else:
            obj_instance = storage.classes()[line]()
            obj_instance.save()
            print(obj_instance.id)

    def do_show(self, line):
        """Usage: show <class name> <id>
           Function: Shows the instance details of the class
        """
        if not line:
            print("** class name missing **")
            return

        args = line.split()
        if len(args) < 2:
            print("** instance id missing **")
            return

        class_name, instance_id = args[0], args[1]
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return

        key = f"{class_name}.{instance_id}"
        if key not in storage.all():
            print("** no instance found **")
        else:
            print(storage.all()[key])

    def do_destroy(self, line):
        """Usage: destroy <class name> <id>
           Function: Deletes the instance of the class
        """
        if not line:
            print("** class name missing **")
            return

        args = line.split()
        if len(args) < 2:
            print("** instance id missing **")
            return

        class_name, instance_id = args[0], args[1]
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return

        key = f"{class_name}.{instance_id}"
        if key not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[key]
            storage.save()

    def do_all(self, line):
        """Usage: all [<class name>]
           Function: Prints the string representation of all instances
        """
        if line:
            if line not in storage.classes():
                print("** class doesn't exist **")
                return
            instance_list = [str(obj) for key, obj in storage.all().items() if key.startswith(line)]
        else:
            instance_list = [str(obj) for obj in storage.all().values()]

        print(instance_list)

    def do_update(self, line):
        """Usage: update <class name> <id> <attribute> <value> or update <class name> <id> <dictionary>
           Function: Updates the instance of the class
        """
        if not line:
            print("** class name missing **")
            return

        args = line.split(' ', 2)
        if len(args) < 2:
            print("** instance id missing **")
            return

        class_name, instance_id = args[0], args[1]
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return

        key = f"{class_name}.{instance_id}"
        if key not in storage.all():
            print("** no instance found **")
            return

        if len(args) == 3:
            match = re.match(r'^\{.*\}$', args[2])
            if match:
                update_dict = json.loads(args[2])
                instance = storage.all()[key]
                for attr, value in update_dict.items():
                    setattr(instance, attr, value)
                instance.save()
                return

            attr_val = args[2].split(' ', 1)
            if len(attr_val) < 2:
                print("** value missing **")
                return

            attribute, value = attr_val[0], attr_val[1]
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]

            instance = storage.all()[key]
            setattr(instance, attribute, value)
            instance.save()
        else:
            print("** attribute name missing **")

    def emptyline(self):
        """Overrides the default behavior to do nothing on an empty line"""
        pass

    def precmd(self, line):
        """Intercepts commands to test for class.syntax()"""
        if not sys.stdin.isatty():
            print()

        match = re.match(r"^(\w+)\.(\w+)\(([^)]*)\)$", line)
        if match:
            class_name, method, args = match.groups()
            if args:
                args = args.split(', ')
                args = " ".join(arg.strip('"') for arg in args)
                line = f"{method} {class_name} {args}"
            else:
                line = f"{method} {class_name}"

        return cmd.Cmd.precmd(self, line)

    def do_count(self, line):
        """Usage: count <class name>
           Function: Counts all the instances of the class
        """
        if line in storage.classes():
            count = sum(1 for key in storage.all() if key.startswith(line))
            print(count)
        else:
            print("** class doesn't exist **")


if __name__ == '__main__':
