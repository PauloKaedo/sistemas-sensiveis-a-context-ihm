import face_recognition
import random
import faker
import json
import secrets

PHOTOS = [
    "C:/Users/Java/Desktop/future_armors/faces/jack1.jpg",
    "C:/Users/Java/Desktop/future_armors/faces/jack2.jpg",
    "C:/Users/Java/Desktop/future_armors/faces/jack3.jpg",

    "C:/Users/Java/Desktop/future_armors/faces/jon1.jpg",
    "C:/Users/Java/Desktop/future_armors/faces/jon2.jpg",
    "C:/Users/Java/Desktop/future_armors/faces/jon3.jpg",

    "C:/Users/Java/Desktop/future_armors/faces/stallone1.jpg",
    "C:/Users/Java/Desktop/future_armors/faces/stallone2.jpg",
    "C:/Users/Java/Desktop/future_armors/faces/stallone3.jpg",

    "C:/Users/Java/Desktop/future_armors/faces/vin1.jpg",
    "C:/Users/Java/Desktop/future_armors/faces/vin2.jpg",
    "C:/Users/Java/Desktop/future_armors/faces/vin3.jpg"
]

CONFIG_FILE = "C:/Users/Java/Desktop/future_armors/config.json"

ENLISTMENT_TIME = 600
PATENT_TIME = 60
EQUIP_TIME = 200
TIME_TO_GO_WAR = 100


def start():
    
    recognized_soldiers = {}
    
    equipped_soldiers = {}
    patent_soldiers = {}

    armor_storage = {
        'Bronze Armor': (random.randint(1,3)),
        'Steel Armor': (random.randint(1,3)),
        'Platinum Armor': (random.randint(1,2)),
        'Diamond Scale Armor': (random.randint(1,3)),
    }

    config = None

    with open(CONFIG_FILE, 'r') as conf_file:
        config = json.load(conf_file)

    return config, patent_soldiers, equipped_soldiers, recognized_soldiers, armor_storage

def simule_enlistment(photo):
    person = {
        "photo": photo
    }

    return person

def is_soldier(person, config):

    fake_data_generator = faker.Faker(locale="pt-BR")

    person_photo = face_recognition.load_image_file(person["photo"])
    person_photo_encoded = face_recognition.face_encodings(person_photo)[0]

    soldier_recognized = False

    for soldier in config["soldiers"]:
        photo_database = soldier["photos"]
        total_recognized = 0

        for photo in photo_database:
            data_photo = face_recognition.load_image_file(photo)
            data_encoded = face_recognition.face_encodings(data_photo)[0]

            if face_recognition.compare_faces([person_photo_encoded], data_encoded):
                total_recognized += 1
        if total_recognized/len(photo_database) > 0.70:
            soldier_recognized = True

            person["soldiers"] = {}
            person["soldiers"]["name"] = fake_data_generator.name()
            person["soldiers"]["age"] = random.randint(18,50)
            person["soldiers"]["equipped"] = False
            person["soldiers"]["inMission"] = False
        
        return soldier_recognized, person
    
    return soldier_recognized, person

def print_soldier_data(soldier):
    print("Nome: ", soldier["soldiers"]["name"])
    print("Idade: ", soldier["soldiers"]["age"])

def recognitize_person(person, config):
    recognized, soldier = is_soldier(person, config)
    recognized_soldier = {}
    
    return recognized, soldier

def indentify_patent(recognized_soldiers, random_patent):

    patent_soldier = []

    for id, soldier in list(recognized_soldiers.items()):
        if random_patent == '1':
            soldier["soldiers"]["patent"] = "Recruit"
            patent_soldier = soldier

        elif random_patent == '2':
            soldier["soldiers"]["patent"] = "Solid"
            patent_soldier = soldier
        
        elif random_patent == '3':
            soldier["soldiers"]["patent"] = "General"
            patent_soldier =  soldier

        elif random_patent == '4':
            soldier["soldiers"]["patent"] = "Major"
            patent_soldier =  soldier

        return True, patent_soldier['soldiers']


def select_armor(patent_soldiers, armor_storage):
    
    equipped_soldier = {}
    
    for id, soldier in list(patent_soldiers.items()):
        patent = soldier["patent"]

        if patent == 'Recruit':
            
            if armor_storage['Bronze Armor'] > 0:
                soldier["armor"] = "Bronze Armor"
                soldier["equipped"] = True
                equipped_soldier = soldier
            else: 
                soldier["armor"] = "Commum Armor"
                soldier["equipped"] = True
                equipped_soldier = soldier

        elif patent == 'Solid':
            if armor_storage['Steel Armor'] > 0:
                soldier["armor"] = "Steel Armor"
                soldier["equipped"] = True
                equipped_soldier = soldier
            else: 
                soldier["armor"] = "Commum Armor"
                soldier["equipped"] = True
                equipped_soldier = soldier

        elif patent == 'General':
            if armor_storage['Platinum Armor'] > 0:
                soldier["armor"] = "Platinum Armor"
                soldier["equipped"] = True
                equipped_soldier = soldier
            else: 
                soldier["armor"] = "Commum Armor"
                soldier["equipped"] = True
                equipped_soldier = soldier       

        elif patent == 'Major':
            if armor_storage['Diamond Scale Armor'] > 0:
                soldier["armor"] = "Diamond Scale Armor"
                soldier["equipped"] = True
                equipped_soldier = soldier
            else: 
                soldier["armor"] = "Commum Armor"
                soldier["equipped"] = True
                equipped_soldier = soldier

    return True, equipped_soldier
    
def provide_armor(equipped_soldiers):
    sucess = False
    in_mission = {}

    for id, soldier in list(equipped_soldiers.items()):
        
        if not soldier["inMission"]:
            soldier["inMission"] = True
        sucess = True
        in_mission = soldier

    return sucess, in_mission
