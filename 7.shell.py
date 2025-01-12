import os
import shlex
import subprocess

def execute_command(command):
    try:
        # Parse the command into parts
        parts = shlex.split(command)
        
        # Check for IO redirection or pipes
        if '|' in parts:
            # Handle piping
            processes = []
            commands = command.split('|')
            for i, cmd in enumerate(commands):
                cmd_parts = shlex.split(cmd.strip())
                if i == 0:
                    # First command, no input redirection
                    processes.append(subprocess.Popen(cmd_parts, stdout=subprocess.PIPE))
                else:
                    # Use output of previous command as input for the next
                    processes.append(subprocess.Popen(cmd_parts, stdin=processes[-1].stdout, stdout=subprocess.PIPE))
                    processes[-2].stdout.close()  # Allow the previous process to receive a SIGPIPE if it exits

            # Get the output of the final process
            output, _ = processes[-1].communicate()
            print(output.decode())
        elif '>' in parts or '<' in parts:
            # Handle redirection
            if '>' in parts:
                cmd, outfile = command.split('>')
                outfile = outfile.strip()
                cmd_parts = shlex.split(cmd.strip())
                with open(outfile, 'w') as f:
                    subprocess.run(cmd_parts, stdout=f)
            elif '<' in parts:
                cmd, infile = command.split('<')
                infile = infile.strip()
                cmd_parts = shlex.split(cmd.strip())
                with open(infile, 'r') as f:
                    subprocess.run(cmd_parts, stdin=f)
        else:
            # Execute simple commands
            result = subprocess.run(parts, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
    except FileNotFoundError:
        print(f"Command not found: {parts[0]}")
    except Exception as e:
        print(f"Error executing command: {e}")

def main():
    print("Custom Shell - Enter 'exit' to quit.")
    while True:
        try:
            # Display prompt
            command = input("shell> ").strip()
            if command.lower() == 'exit':
                break
            if command:
                execute_command(command)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit the shell.")
        except EOFError:
            break

if __name__ == "__main__":
    main()
