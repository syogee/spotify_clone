from configparser import ConfigParser

def config(file="database.ini",section='postgres'):
    praser = ConfigParser()
    praser.read(file)
    db={}
    if praser.has_section(section):
        for i in praser.items(section):
            db[i[0]]=i[1]
    else:
        print(section+"not found")
    return db
config()
