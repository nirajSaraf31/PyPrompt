import sys
import os
import subprocess
import shlex


def main():
    paths = os.getenv("PATH").split(os.pathsep)

    while(True):
        sys.stdout.write("$ ")
        command = input()
        c = shlex.split(command)
        output_file = ""
        output = ""
        error = ""
        assign = ""
        of = [">", "1>", ">>", "1>>"]
        ef = ["2>", "2>>"]
        for ele in c:
            if ele in of:
                output_file = c[c.index(ele) + 1]
                c = c[:c.index(ele)]
                assign = ele
                break
        for ele in c:
            if ele in ef:
                output_file = c[c.index(ele) + 1]
                c = c[:c.index(ele)]
                assign = ele
                break
        commands = ["exit", "echo", "type", "pwd","cd"]
        Found = False

        if c[0] == "exit":
            if len(c) > 1 and c[1].isdigit():
                sys.exit(int(c[1]))
            else:
                sys.exit(0)
        elif c[0] == "echo":
            output = " ".join(c[1:])
        elif c[0] == "pwd":
            output = os.getcwd()
        elif c[0] == "cd":
            if os.path.isdir(c[1]):
                os.chdir(c[1])
            elif c[1] == "~":
                os.chdir(os.environ["HOME"])
            else:
                output = f"cd: {c[1]}: No such file or directory"

        elif c[0] == "type":
            if c[1] in commands:
                output = c[1] + " is a shell builtin"
                Found = True
            else:
                for path in paths:
                    if os.path.isfile(f"{path}/{c[1]}"):
                        output = f"{c[1]} is {path}/{c[1]}"
                        Found = True
                        break
            if not Found:
                output = c[1] + ": not found"

        else:
            Found = False
            for path in paths:
                if os.path.isfile(f"{path}/{c[0]}"):
                    result = subprocess.run(c, stdout=subprocess.PIPE,stderr=subprocess.PIPE, text = True)
                    output = result.stdout.rstrip()
                    error = result.stderr.rstrip()
                    Found= True
                    break
                if Found:
                    break
            if not Found:
                error = f"{c[0]}: command not found"

        if assign in ef:
            with open(output_file, "a") as f:
                if error:
                    f.write(error+"\n")
                error = ""
        elif assign in of:
            with open(output_file, "a") as f:
                if output:
                    f.write(output+"\n")
                output = ""
        if error:
            print(error)
        if output:
            print(output)


if __name__ == "__main__":
    main()
