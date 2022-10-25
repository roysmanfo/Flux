import json
with open("./settings.json", "r") as f:
    file = json.load(f)

    with open("./settings.json", "w") as l:
        json.dump(file, l, indent=4,sort_keys=True)

# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z