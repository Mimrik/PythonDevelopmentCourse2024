import cmd
import shlex
import cowsay


custom_tongue = ["__", "..", "=="]
custom_eyes = ["xx", "..", "oo"]


class MyCmd(cmd.Cmd):
    @staticmethod
    def do_list_cows(arg):
        """
        Lists all cow file names in the given directory
        Example: list_cows ~
        """
        if arg:
            print(cowsay.list_cows(cow_path=arg))
        else:
            print(cowsay.list_cows())

    @staticmethod
    def do_make_bubble(arg):
        """
        Wraps text if wrap_text is True, then pads text and sets inside a bubble.
        Example: make_bubble "test"
        """
        print(cowsay.make_bubble(text=shlex.split(arg)[0]))

    def do_cowsay(self, arg):
        """
        Same to cowsay command. Returns the resulting cowsay string
        Example: cowsay "test" default xx "  "
        """
        message, args = self._cast_message_and_args(arg)
        print(cowsay.cowsay(message=message, **args))

    def do_cowthink(self, arg):
        """
        Same to cowthink command. Returns the resulting cowthink string
        Example: cowthink "test" default xx "  "
        """
        message, args = self._cast_message_and_args(arg)
        print(cowsay.cowthink(message=message, **args))

    @staticmethod
    def complete_list_cows(prefix):
        if not prefix:
            return ["~"]

    def complete_cowsay(self, prefix, line):
        return self._complete(prefix, line)

    def complete_cowthink(self, prefix, line):
        return self._complete(prefix, line)

    @staticmethod
    def _cast_message_and_args(arg):
        names = ["cow", "eyes", "tongue"]
        defaults = ["default", "oo", "  "]
        args = shlex.split(arg)
        message, defaults[:len(args) - 1] = args[0], args[1:]
        args = dict(list(zip(names, defaults)))
        return message, args

    @staticmethod
    def _complete(prefix, line):
        s = shlex.split(line)
        if len(s) == 3:
            return [i for i in cowsay.list_cows() if i.startswith(prefix)]
        elif len(s) == 4:
            return [i for i in custom_eyes if i.startswith(prefix)]
        elif len(s) == 5:
            return [i for i in custom_tongue if i.startswith(prefix)]


if __name__ == "__main__":
    MyCmd().cmdloop()
