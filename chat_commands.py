import subprocess
import webbrowser
import re
import validators
import sys

def process_commands(passed_commands, command):
    if "computer" in command.lower():
        print("Activated Command: Computer")
        passed_commands.text_output.insert(
            passed_commands.tk.END, "Activated Command: Computer" + "\n")
        passed_commands.submit(text_input=command)
        # listen_to_command()

        # Open a website
        #if command.lower().startswith("open website"):
        if "open website" in command.lower():
            # Extract the website URL from the command
            #url = command.replace("open website", "")
            url = command.partition("open website")
            # access third tuple element
            url = url[2]
            url = url.strip() # Strip whitespace on both ends. Not working? As there is a space in the leading part of the URL variable after this.
            # Test for http:// or https:// and add http:// to the URL if missing.
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
            
            print("Trying to open website: " + url)

            # Validating if the URL is correct
            if validators.url(url):
                webbrowser.open(url, new=0, autoraise=True)
                
                passed_commands.text_output.insert(
                    passed_commands.tk.END, "Opening website: " + url + "\n")
            else:
                print("Invalid URL command. URL: " + url)
                passed_commands.text_output.insert(
                    passed_commands.tk.END, "Invalid URL command. URL: " + url + "\n")

        return

def process_commands(passed_commands, command):
    if "computer" in command.lower():
        print("Activated Command: Computer")
        passed_commands.text_output.insert(
            passed_commands.tk.END, "Activated Command: Computer" + "\n")
        passed_commands.submit(text_input=command)
        # listen_to_command()

        # Open an application
        if "run program" in command.lower():
            # Extract the application name from the command
            app_name = command.partition("run program")[2]
            app_name = app_name.strip()

            print("Trying to open program: " + app_name)

            try:
                subprocess.Popen(app_name)
                passed_commands.text_output.insert(
                    passed_commands.tk.END, "Opening program: " + app_name + "\n")
            except FileNotFoundError:
                print("Program not found: " + app_name)
                passed_commands.text_output.insert(
                    passed_commands.tk.END, "Program not found: " + app_name + "\n")

            return

        print("Invalid command")
        passed_commands.text_output.insert(
            passed_commands.tk.END, "Invalid command" + "\n")


    # Testing
    # Stop listening to the microphone
    if command.lower() == "stop listening":
        passed_commands.text_output.insert(
            passed_commands.tk.END, "Stopping the microphone." + "\n")
        # What goes here?

        return

    # Testing
    # Allow program exit via voice.
    if command.lower() == "stop program":
        passed_commands.text_output.insert(
            passed_commands.tk.END, "Stopping the program." + "\n")
        
        sys.exit()

        return
