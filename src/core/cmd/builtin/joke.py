"""
# `joke`

This command tells a random programming joke
"""

import json
import os
from ...helpers.commands import CommandInterface
import random


class Command(CommandInterface):
    
    def setup(self):
        self.jokes: list[str] = []
        jpath = os.path.join(self.sysinfo.syspaths.LOCAL_FOLDER, "jokes", "jokes.json")
        try:
            with open(jpath) as f:
                jokes_data = json.load(f)
                self.jokes = jokes_data["jokes"]
        
        except FileNotFoundError:
            os.makedirs(os.path.dirname(jpath), exist_ok=True) # exists_ok=True in case just the file is missing
            with open(jpath, "w") as f:
                jokes_data = {"jokes" : JOKES}
                json.dump(jokes_data, f, indent=4)
                self.jokes = JOKES
            
        except PermissionError:
            self.error(self.errors.permission_denied(jpath))
        


    def run(self):
        """
        This command tells a random programming joke
        """
        self.sysinfo.syspaths.LOCAL_FOLDER


        self.print(random.choice(self.jokes))
        self.print()

# TODO: Not store jokes here but add an alternative method to restore jokes.json 
JOKES = [
    "Did you turn it off and on again?",
    "Works on my machine.",
    "Syntax error: between keyboard and chair.",
    "That's not a bug; it's a feature.",
    "404: Sense of humor not found.",
    "I don't always test my code, but when I do, I do it in production.",
    "When you accidentally close the terminal.",
    "Hello World! The programmer's first love.",
    "My code doesn't work, but I don't know why.",
    "I have no idea what I'm doing.",
    "Real programmers use Vim.",
    "Recursion: see Recursion.",
    "Why do Java developers wear glasses? Because they don't C#!",
    "Code so clean, it self-documents.",
    "99 little bugs in the code, 99 little bugs. Take one down, patch it around, 117 little bugs in the code.",
    "Programmer: A machine that turns coffee into code.",
    "There are only 10 types of people in the world: those who understand binary and those who don't.",
    "git commit -m 'Fix typo, please work now'",
    "Coffee: the code fuel.",
    "Code never lies; comments sometimes do.",
    "Debugging: like being the detective in a crime movie where you are also the murderer.",
    "Copy-paste: the developer's best friend and worst enemy.",
    "I'm not lazy; I'm just on 'energy-saving' mode.",
    "No, I will not fix your computer.",
    "99 bugs on the wall, 99 bugs. Take one down, patch it around, 127 bugs on the wall.",
    "Programming is like LEGO for adults.",
    "Syntax you understand, but semicolon you forget.",
    "When you find a stack overflow, but it's not the website.",
    "Trust me, I'm an engineer.",
    "Don't worry; I backed up my code… last month.",
    "If at first, you don't succeed, call it version 1.0.",
    "I see dead code.",
    "Will code for pizza.",
    "The only job where you can be fired for making your work too efficient.",
    "Optimist: the glass is half full. Pessimist: the glass is half empty. Programmer: the glass is twice as large as necessary.",
    "I don't need a debugger; my code is perfect.",
    "Programmers don't die; they just GOSUB without RETURN.",
    "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25!",
    "I got 99 problems, but a switch case ain't one.",
    "If you can't beat them, refactor them.",
    "The code works, but I have no idea why.",
    "Debugging is like an onion; the more layers you peel, the more you want to cry.",
    "There's no place like 127.0.0.1.",
    "A SQL query walks into a bar, walks up to two tables, and asks: 'Can I join you?'",
    "Why do programmers hate nature? It has too many bugs.",
    "99 little bugs in the code, 99 little bugs. Take one down, patch it around, 999 little bugs in the code.",
    "Programming: It's all fun and games until someone divides by zero.",
    "There are two ways to write error-free programs, only the third one works.",
    "Programmer's diet: pizza and merge conflicts.",
    "I'm not procrastinating; I'm just prioritizing my bugs.",
    "When you fix a bug, and five more show up.",
    "Abandon all hope, ye who enter legacy code.",
    "All I need is coffee and code.",
    "The best error message is the one that never shows up.",
    "There's no place like ~.",
    "I'm not slacking off; my code is compiling.",
    "The code was clean yesterday. What happened?",
    "Documentation is like sex: when it's good, it's very good, and when it's bad, it's better than nothing.",
    "Why do Java developers wear sandals? Because they don't C#!",
    "To err is human, to blame it on someone else is debugging.",
    "I'm not lazy; I'm just waiting for the build to finish.",
    "I don't always test my code, but when I do, I do it in production.",
    "My code has no bugs; it's just undocumented features.",
    "Don't worry; I fixed it in the dev environment.",
    "It's not a bug; it's an undocumented feature.",
    "99 little bugs in the code, 99 little bugs. Take one down, patch it around, 113 little bugs in the code.",
    "I don't need Stack Overflow; I can handle bugs on my own.",
    "Code review? Ain't nobody got time for that!",
    "Roses are #FF0000, violets are #0000FF, all my base are belong to you.",
    "I void warranties.",
    "I'm not a nerd; I'm a human search engine.",
    "The code you write at 4 AM is always the best.",
    "My code is flawless; my computer has bugs.",
    "When in doubt, blame the compiler.",
    "A byte walks into a bar, and the bartender asks: 'What's your order?' The byte replies: 'I'm just here for a bit.'",
    "It's not a bug; it's an undocumented feature.",
    "Programming is easy; it's people that are hard.",
    "Why do Java developers wear glasses? Because they can't C#!",
    "I don't always test my code, but when I do, I do it in production.",
    "My code doesn't work, but I don't know why.",
    "The best performance improvement is the delete key.",
    "It's not a bug; it's a feature request.",
    "What's the object-oriented way to become wealthy? Inheritance.",
    "That's not a bug; it's a feature.",
    "Code so clean, you could eat off it.",
    "It's not you; it's your code.",
    "I've got 99 problems, but floating-point errors ain't one.",
    "Why do programmers hate nature? It has too many bugs.",
    "I don't always write tests, but when I do, I run them in production.",
    "I'm sorry, Dave. I'm afraid I can't do that.",
    "Error: Keyboard not found. Press any key to continue.",
    "git commit -m 'Fixed a typo. Now code is perfect'",
    "When you realize you've been debugging for hours and forgot to press 'Play.'",
    "Writing code without testing is like cooking without tasting.",
    "The code compiles; let's ship it!",
    "Where there's a will, there's a runtime error.",
    "Debugging is like solving a puzzle where the pieces can change while you play.",
    "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25!",
    "I have a lot of Java jokes, but they're garbage collected.",
    "Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live.",
]