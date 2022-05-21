#Luogo di test per le funzionalità del programma prima che vengano implementate 

#Calcolatrice
#print(eval(input()))
import json,os
print(os.getcwd())
os.chdir(r'users')
with open(r'Users.json', 'r') as fileCredenziali:
    new_file = json.load(fileCredenziali)

with open('Users.json', 'w') as fileCredenziali:
    
    User = {
        "User2": {
            "name": 'Test2',
            "password": '5465737450617373776f7264',
            "email": None,
            "role": 'Guest',
            "status": 'Active'
        }
    }
    #list(new_file)
    new_file.update(User)

    json.dump(new_file, fileCredenziali, indent=4)