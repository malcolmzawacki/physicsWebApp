
objects = [
    "cactus","turtle","bowl of soup","block of ice","barrel of monkeys",
    "statue","boulder","Toyota Camry","washing machine","vacant doghouse","baseball","basketball",
    "football","tennis ball","golf ball","recliner","television","record player","magic mirror",
    "broken treadmill","villainous character","stunt-seeking daredevil","Minecraft villager",
    "mischievious rapscalion","clown","giant spider","miniature elephant","kitschy porcelain figurine","priceless artifact",
    "crown jewel","tuba","snare drum","block of concrete","kindergartener's action figure","bonsai tree", 
    "The Infamous Epi Demick","box of tnt", "physics student", "crazy karen", "yard stick"
    ]

def random_noun():
    import random
    return random.choice(objects)

proj_verbs = [
    "catapulted","cannon-fired","launched","chucked","thrown","propelled","kaboomed into the air",
    "hurled","pitched","tossed","flung","lobbed","blasted","ejected","deployed",
    "heaved","set into motion","put into flight","sent skyward", "exploded"
    ]

def random_proj_verb():
    import random
    return random.choice(proj_verbs)


error_messages = [
    "M'thinks thou hast miss'd the mark!","Oh mon Dieu, je suis désolé mais c'est terrible.",
    "Lo siento, esto no es correcto.","Soooo actually...you're wrong.","Yikes. Just, yikes.",
    "Oof, this is not it pal.","Swing and a miss, champ.", "Aw shucks :/","Aw drats!","Gosh dang it!",
    "Not quite..."
    ]

def random_error_message():
    import random
    return random.choice(error_messages)

correct_messages = [
    "Correct!","¡Excelente! Es correcto.", "C'est correct, bon travail!",
    "Hey hey hey, we got a smart one over here!","Not too shabby kid, not too shabby.",
    "Thine brains art formidable indeed", "Incroyable!","¡Increible!","Dataway!"
    ]

def random_correct_message():
    import random
    return random.choice(correct_messages)
