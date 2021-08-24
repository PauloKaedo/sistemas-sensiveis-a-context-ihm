import face_recognition
import random
import faker
import json
import simpy
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
    global config
    global patent_soldiers
    global equipped_soldiers
    global recognized_soldiers
    global armor_storage 
    global fake_data_generator

    fake_data_generator = faker.Faker(locale="pt-BR")
    
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


def simule_enlistment():
    person = {
        "photo": random.choice(PHOTOS)
    }

    return person

def is_soldier(person):
    global config 
    global fake_data

    print("Iniciando reconhecimento da pessoa...")
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
        print("acertos:", total_recognized, len(photo_database) )
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

def recognitize_person(env):
    global recognized_soldiers

    while True:
        print("Reconhecendo Soldado em: ", env.now)
        
        person = simule_enlistment()
        recognized, soldier = is_soldier(person)

        if recognized:
            id = secrets.token_hex(nbytes=4).upper()
            recognized_soldiers[id] = soldier

            print("Um Soldado foi reconhecido. Soldier Token: ", id)
            print_soldier_data(soldier)
        else:
            print("Não foi reconhecido como soldado")
        yield env.timeout(ENLISTMENT_TIME)

def indentify_patent(env):
    global recognized_soldiers
    global patent_soldiers

    while True:
        if len(recognized_soldiers):
            print("Verificando patente do soldado em ciclo ", env.now)
            for id, soldier in list(recognized_soldiers.items()):
                random_patent = random.randint(1,4)
                if random_patent == 1:
                    soldier["soldiers"]["patent"] = "Recruit"
                    print(soldier["soldiers"]["name"], " é reconhecido(a) como: ", soldier["soldiers"]["patent"])
                    patent_soldiers[id] =  soldier

                elif random_patent == 2:
                    soldier["soldiers"]["patent"] = "Solid"
                    print(soldier["soldiers"]["name"], " é reconhecido(a) como: ", soldier["soldiers"]["patent"])
                    patent_soldiers[id] =  soldier
                
                elif random_patent == 3:
                    soldier["soldiers"]["patent"] = "General"
                    print(soldier["soldiers"]["name"], " é reconhecido(a) como: ", soldier["soldiers"]["patent"])
                    patent_soldiers[id] =  soldier

                elif random_patent == 4:
                    soldier["soldiers"]["patent"] = "Major"
                    print(soldier["soldiers"]["name"], " é reconhecido(a) como: ", soldier["soldiers"]["patent"])
                    patent_soldiers[id] =  soldier

            recognized_soldiers.pop(id)

            yield env.timeout(PATENT_TIME)
        else: 
            yield env.timeout(PATENT_TIME)


def select_armor(env):
    while True:
        global patent_soldiers
        global armor_storage
        global equipped_soldiers
        
        if len(patent_soldiers):
            print("Verificando a disponibilidade de Traje de Batalha em: ", env.now)
            for id, soldier in list(patent_soldiers.items()):
                
                if not soldier["soldiers"]["equipped"]:
                    
                    soldier_name = soldier["soldiers"]["name"]
                    patent = soldier["soldiers"]["patent"]

                    if patent == 'Recruit':
                        if armor_storage['Bronze Armor'] > 0:
                            print(soldier_name, " equipado(a) com Traje de Batalha do tipo Bronze em: ", env.now)
                            soldier["soldiers"]["armor"] = "Bronze Armor"
                            soldier["soldiers"]["equipped"] = True
                            equipped_soldiers[id] = soldier
                            armor_storage['Bronze Armor'] -= 1
                        else: 
                            print("Trajes de Batalhas disponíveis para essa patente esgotados. O soldado será equipado com um traje comum.")
                            print(soldier_name, " equipado(a) com Traje de Batalha do tipo Comum em: ", env.now)
                            soldier["soldiers"]["armor"] = "Commum Armor"
                            soldier["soldiers"]["equipped"] = True
                            equipped_soldiers[id] = soldier

                    elif patent == 'Solid':
                        if armor_storage['Steel Armor'] > 0:
                            print(soldier_name, " equipado(a) com Traje de Batalha do tipo Steel em: ", env.now)
                            soldier["soldiers"]["armor"] = "Steel Armor"
                            soldier["soldiers"]["equipped"] = True
                            equipped_soldiers[id] = soldier
                            armor_storage['Steel Armor'] -= 1
                        else: 
                            print("Trajes de Batalhas disponíveis para essa patente esgotados. O soldado será equipado com um traje comum.")
                            print(soldier_name, " equipado(a) com Traje de Batalha do tipo Comum em: ", env.now)
                            soldier["soldiers"]["armor"] = "Commum Armor"
                            soldier["soldiers"]["equipped"] = True
                            equipped_soldiers[id] = soldier

                    elif patent == 'General':
                        if armor_storage['Platinum Armor'] > 0:
                            print(soldier_name, " equipado(a) com Traje de Batalha do tipo Platinum em: ", env.now)
                            soldier["soldiers"]["armor"] = "Platinum Armor"
                            soldier["soldiers"]["equipped"] = True
                            equipped_soldiers[id] = soldier
                            armor_storage['Platinum Armor'] -= 1
                        else: 
                            print("Trajes de Batalhas disponíveis para essa patente esgotados. O soldado será equipado com um traje comum.")
                            print(soldier_name, " equipado(a) com Traje de Batalha do tipo Comum em: ", env.now)
                            soldier["soldiers"]["armor"] = "Commum Armor"
                            soldier["soldiers"]["equipped"] = True
                            equipped_soldiers[id] = soldier       

                    elif patent == 'Major':
                        if armor_storage['Diamond Scale Armor'] > 0:
                            print(soldier_name, " equipado(a) com Traje de Batalha do tipo Diamond Scale em: ", env.now)
                            soldier["soldiers"]["armor"] = "Diamond Scale Armor"
                            soldier["soldiers"]["equipped"] = True
                            equipped_soldiers[id] = soldier
                            armor_storage['Diamond Scale Armor'] -= 1
                        else: 
                            print("Trajes de Batalhas disponíveis para essa patente esgotados. O soldado será equipado com um traje comum.")
                            print(soldier_name, " equipado(a) com Traje de Batalha do tipo Comum em: ", env.now)
                            soldier["soldiers"]["armor"] = "Commum Armor"
                            soldier["soldiers"]["equipped"] = True
                            equipped_soldiers[id] = soldier
                        
                else:
                    print("Patente não reconhecida.")

                patent_soldiers.pop(id)
        yield env.timeout(EQUIP_TIME)

def provide_armor(env):
    while True:
        global equipped_soldiers
        
        if len(equipped_soldiers):
            print("Equipando e enviando Soldado para missão em: ", env.now)

            for id, soldier in list(equipped_soldiers.items()):
                
                if not soldier["soldiers"]["inMission"]:
                    soldier["soldiers"]["inMission"] = True
                    print("Missão de nível", random.randint(0,5), " selecionada. Enviando", soldier["soldiers"]["patent"], soldier["soldiers"]["name"], "em missão.")
                    print("O traje", soldier["soldiers"]["armor"], "está equipado com tecnologia de ponta. Vefique a bateria e munição antes de sair. Boa Sorte!")
                    equipped_soldiers.pop(id)
                    print("\n==================================================================================================================\n")

        yield env.timeout(TIME_TO_GO_WAR)

if __name__ == '__main__':

    start()

    env = simpy.Environment()

    env.process(recognitize_person(env))
    env.process(indentify_patent(env))
    env.process(select_armor(env))
    env.process(provide_armor(env))

    env.run(until = 1800)
    
