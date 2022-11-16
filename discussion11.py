import unittest
import sqlite3
import json
import os
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# Creates list of species ID's and numbers
def create_species_table(cur, conn):

    species = ["Rabbit",
    "Dog",
    "Cat",
    "Boa Constrictor",
    "Chinchilla",
    "Hamster",
    "Cobra",
    "Parrot",
    "Shark",
    "Goldfish",
    "Gerbil",
    "Llama",
    "Hare"
    ]

    cur.execute("DROP TABLE IF EXISTS Species")
    cur.execute("CREATE TABLE Species (id INTEGER PRIMARY KEY, title TEXT)")
    for i in range(len(species)):
        cur.execute("INSERT INTO Species (id,title) VALUES (?,?)",(i,species[i]))
    conn.commit()

# TASK 1
# CREATE TABLE FOR PATIENTS IN DATABASE
def create_patients_table(cur, conn):
    cur.execute("DROP TABLE IF EXISTS Patients")
    cur.execute("""CREATE TABLE IF NOT EXISTS Patients (
    pet_id INTEGER PRIMARY KEY,
    name TEXT,
    species_id NUMBER,
    age INTEGER,
    cuteness INTEGER,
    aggressiveness NUMBER
    )""")
    conn.commit()

def add_fluffle(cur, conn):
    cur.execute("INSERT INTO Patients (pet_id, name, species_id, age, cuteness, aggressiveness) VALUES (?,?,?,?,?,?)", (0, "Fluffle", 0, 3, 90, 100))
    conn.commit()

# TASK 2
# CODE TO ADD JSON TO THE TABLE
# ASSUME TABLE ALREADY EXISTS
def add_pets_from_json(filename, cur, conn):
    
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(filename)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)

    # THE REST IS UP TO YOU
    pet_id = 1
    for item in json_data:
        cur.execute("SELECT id, title FROM Species")
        for row in cur:
            if row[1] == item['species']:
                species_id = row[0]
        insert_tup = (pet_id, item['name'], species_id, item['age'], item['cuteness'], item['aggressiveness'])
        print(insert_tup)
        cur.execute("INSERT INTO Patients (pet_id, name, species_id, age, cuteness, aggressiveness) VALUES(?,?,?,?,?,?)", insert_tup)
        pet_id += 1
        conn.commit()




# TASK 3
# CODE TO OUTPUT NON-AGGRESSIVE PETS
def non_aggressive_pets(aggressiveness, cur, conn):
    return_list = []
    table_pull = cur.execute("SELECT name FROM Patients WHERE aggressiveness < 10")
    print(table_pull)
    for row in table_pull:
        return_list.append(row)

    return return_list
    



def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('animal_hospital.db')
    create_species_table(cur, conn)

    create_patients_table(cur, conn)
    add_fluffle(cur, conn)
    add_pets_from_json('pets.json', cur, conn)
    ls = (non_aggressive_pets(10, cur, conn))
    print(ls)
    
    
if __name__ == "__main__":
    main()

