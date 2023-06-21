### Libs ####


from fpdf import FPDF
import json


##### Envs #####


## Methods :

def getMyListFromFilePath (filePath, splitting) :
    file = open(filePath)
    stringV =  file.read()
    file.close()
    return stringV.split(splitting)

# traitement des champs a compler, et concatenation des strings
def TreatForPersonAndType(personne, dtype, TAB, example_list, fileName):
    resultStr = ""
    #on itere sur le tableau des champs a remplir
    for i in range (0, len(TAB)):
        resultStr = resultStr + example_list[i]
        if(TAB[i] == "dtype"):
            resultStr = resultStr + dtype
        elif(TAB[i]=="url"):
            resultStr = resultStr + fileName
        else: # dans le cas ou c est une info propre a la personne
            resultStr = resultStr + personne[TAB[i]]
    resultStr = resultStr + example_list[len(example_list)-1]
    return resultStr
    

# genere un referentiel pour une liste de champs et un repertoire defini
def GenerateReferential(fields, link):
    # liste des elements du fichier d'exemple
    referential_list = getMyListFromFilePath("referentiel_example.json", "_$VAR_")
    fields_string = json.dumps(fields)
    print( str(len(fields)) + " champs trouves pour le referentiel de " + link)

    result_string = referential_list[0] + fields_string + referential_list[1]
    referential_body = open(link + "/__files/referentiel.json", 'w')
    referential_body.write(result_string)
    referential_body.close()

##################### LISTE DES IDS ###################

resList = []
# envoie l element dans la bonne fonction
def goNext(elt, previous=''):
    if (type(elt) == type ({}) ):
        #traitement pour un dictionnaire
        return getAllFieldsFromDictionnary(elt, previous)
    elif (type(elt) == type ([])):
        #traitement pour un tableau
        return getAllFieldsFromList(elt, previous)
    else:
        #on renvoie l'historique + le nom de l element (passur dutout, ptet return previous, meme suremnt)
        return previous #+ '_' + elt

# traitement pour une liste
def getAllFieldsFromList(list, previous=''):
    # si iterable, on avance dans l arborescence
    if(type(list[0]) == type([]) or type(list[0]) == type({})):
        return goNext(list[0], previous)
    else:
        #sinon on a termine le parcours
        return previous

# traitement pour un dictionnaire
def getAllFieldsFromDictionnary(dictionnary, previous=''):
    
    #On itere sur les clefs du dico, et on ajoute a la liste des elements ceux trouves
    for key in dictionnary.keys():
        resList.append(goNext(dictionnary[key], previous + '_' +key))
    return previous


def getIdList ():
    # ouvrir le fichier en tant que JSon
    with open('api-rh-fields-list.json') as sample_file:
        sample = json.load(sample_file)
    return getAllFieldsFromDictionnary(sample)

##################### FIN LISTE DES IDS ###################

## define lists

P1 = {"nom":"Hallyday", "prenom":"Johnny", "nid":"001", "dateDeNaissance":"15/06/1943", "role": "Intermitant du spectacle", "grade": "Chanteur", "pnomConjoint": "Laeticia", "pnomEnfant":"plusieurs","adresse":"cimetiere"}
P2 = {"nom":"Bond", "prenom":"James", "nid":"007", "dateDeNaissance":"07/07/007", "role":"AgentSecret", "grade":"Spy", "pnomConjoint":"Toutes les femmes", "pnomEnfant": "", "adresse":""}
P3 = {"nom":"Deloin", "prenom":"Alain", "nid":"002", "dateDeNaissance":"Mathusalem", "role":"Meilleur Acteur", "grade":"Cesare", "pnomConjoint":"", "pnomEnfant": "", "adresse":"Cimetierre"}

TAB_MAPPING = ["nid", "dtype", "url"]
TAB_BODY = ["url", "dtype", "prenom", "nid", "nom"]
TAB_BODY_RH = ["role","grade","nid","nom", "prenom", "nom", "pnomConjoint", "nom", "pnomEnfant", "adresse"]
TAB_MAPPING_RH = ["nid", "nid"]

personnes = [P1, P2, P3]
doc_types = getMyListFromFilePath("types_documents.txt", "\n\n")


## read and split examples


body_list_ex = getMyListFromFilePath("body_example.json", "_$VAR_")
mapping_list_ex = getMyListFromFilePath("mappings_example.json", "_$VAR_")

#rh_body_list_ex = getMyListFromFilePath("rhpi_body_example.json", "_$VAR_")
#rh_mapping_list_ex = getMyListFromFilePath("rhpi_mappings_example.json", "_$VAR_")

print("Sources interpretees")
print("===========================================================================")

## write results => 888 / personne

#if(len(body_list_ex) != len(TAB_BODY) or len(mapping_list_ex) != len(TAB_MAPPING)):
#     exit("tailles differentes :: " + str(len(body_list_ex)) +'!='+ str(len(TAB_BODY)) +' '+ str(len(mapping_list_ex)) +'!='+ str(len(TAB_MAPPING)))

# generation des fichiers
for personne in personnes :
    #####################################
    # generation pour Sdemat
    #####################################
    for dtype in doc_types:
        ## Nom du fichier defini "par convention"
        filename = personne["nom"] + "_" + personne["prenom"] + "_" + dtype

        ## recuperation des chaines de caracteres equivalente aux fichiers a generer 
        res_body = TreatForPersonAndType(personne, dtype, TAB_BODY, body_list_ex,  filename)
        res_mapping = TreatForPersonAndType(personne, dtype, TAB_MAPPING, mapping_list_ex, filename)

        ## Le body de la reponse
        f_body = open("wiremock_standalone_SDemat-MOCK/__files/documents_"+filename+".json", 'w')
        f_body.write(res_body)
        f_body.close()

        ## Le pattern pour le mapping de wiremock
        f_mapping = open("wiremock_standalone_SDemat-MOCK/mappings/documents_"+filename+".json", 'w')
        f_mapping.write(res_mapping)
        f_mapping.close()

        ## Creation des PJ en PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=dtype + " de " + personne["prenom"] + " " + personne["nom"], ln=1, align="C")
        pdf.output("PJ/" + filename + ".pdf")

    ####################################
    # generation API-RH
    ####################################

    #filename = personne["nid"]
    #res_body = TreatForPersonAndType(personne, None, TAB_BODY_RH, rh_body_list_ex,  filename)
    #res_mapping = TreatForPersonAndType(personne, None, TAB_MAPPING_RH, rh_mapping_list_ex, filename)

    #f_body = open("wiremock_standalone_api-RH-MOCK/__files/api_"+filename+".json", 'w')
    #f_body.write(res_body)
    #f_body.close()

    #f_mapping = open("wiremock_standalone_api-RH-MOCK/mappings/api_"+filename+".json", 'w')
    #f_mapping.write(res_mapping)
    #f_mapping.close()


## Les referentiels

GenerateReferential(doc_types, "wiremock_standalone_SDemat-MOCK")
#getIdList()
#GenerateReferential(resList, "wiremock_standalone_api-RH-MOCK")

print("generation terminee")

