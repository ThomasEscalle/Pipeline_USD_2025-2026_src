from datetime import datetime

aniversaires = [
    { "nom" : "Zoé" ,              "aniversaire" : "29/12/2004" },
    { "nom" : "Seelen" ,           "aniversaire" : "01/10/2003" },
    { "nom" : "Fleur" ,            "aniversaire" : "15/06/2002" },
    { "nom" : "Eliott" ,           "aniversaire" : "09/09/2003" },
    { "nom" : "Robin" ,            "aniversaire" : "21/01/2000" },
    { "nom" : "Anouk" ,            "aniversaire" : "03/05/2002" },
    { "nom" : "Lilian" ,           "aniversaire" : "09/11/2001" },
    { "nom" : "Nicholas" ,         "aniversaire" : "24/07/2003" },
    { "nom" : "Yannis" ,           "aniversaire" : "31/05/2003" },
    { "nom" : "Noah" ,             "aniversaire" : "11/10/2003" },
    { "nom" : "Louis" ,            "aniversaire" : "16/03/2004" },
    { "nom" : "Mathieu" ,          "aniversaire" : "25/04/2003" },
    { "nom" : "Nora" ,             "aniversaire" : "08/11/2004" },
    { "nom" : "Flavie" ,           "aniversaire" : "22/11/2003" },
    { "nom" : "Andy" ,             "aniversaire" : "10/03/2001" },
    { "nom" : "Alix" ,             "aniversaire" : "28/04/2003" },
    { "nom" : "Emma" ,             "aniversaire" : "11/02/2000" },
    { "nom" : "Constance" ,        "aniversaire" : "21/02/2003" },
    { "nom" : "Eva" ,              "aniversaire" : "30/04/2003" },
    { "nom" : "Arnaud" ,           "aniversaire" : "01/08/2004" },
    { "nom" : "Samuel" ,           "aniversaire" : "25/01/2003" },
    { "nom" : "Thomas Duponchez" , "aniversaire" : "18/12/1996" },
    { "nom" : "Thomas Escalle" ,   "aniversaire" : "28/05/2000" },
    { "nom" : "Eric" ,             "aniversaire" : "19/12/2003" },
    { "nom" : "Clara" ,            "aniversaire" : "01/11/2003" },
    { "nom" : "Jolan" ,            "aniversaire" : "06/08/2001" },
    { "nom" : "Céline" ,           "aniversaire" : "21/03/2003" },
    { "nom" : "Agnès" ,            "aniversaire" : "05/12/2002" },
    { "nom" : "Manon" ,            "aniversaire" : "02/04/2003" },
    { "nom" : "Ethan" ,            "aniversaire" : "07/02/2003" },
    { "nom" : "Tilia" ,            "aniversaire" : "13/03/2002" },
    { "nom" : "Yesmin" ,           "aniversaire" : "30/10/2003" },
    { "nom" : "Gaïa" ,             "aniversaire" : "17/05/1999" },
    { "nom" : "Corentin" ,         "aniversaire" : "07/07/2002" },
    { "nom" : "Joffrey" ,          "aniversaire" : "02/03/2003" },
    { "nom" : "Lucie" ,            "aniversaire" : "25/03/2002" },
    { "nom" : "Chelsea" ,          "aniversaire" : "21/03/2004" },
    { "nom" : "Mathilde" ,         "aniversaire" : "10/10/2002" },
    { "nom" : "Michel" ,           "aniversaire" : "20/04/2003" },
    { "nom" : "Altay" ,            "aniversaire" : "12/10/2003" },
    { "nom" : "Marie-Lou" ,        "aniversaire" : "13/07/2004" },
    { "nom" : "Julien Lauze" ,     "aniversaire" : "04/09/2003" },
    { "nom" : "Maëlle" ,           "aniversaire" : "30/05/2002" },
    { "nom" : "Emeric" ,           "aniversaire" : "03/01/2002" },
    { "nom" : "Diana" ,            "aniversaire" : "21/09/2003" },
    { "nom" : "Nathan" ,           "aniversaire" : "19/03/2003" },
    { "nom" : "Odilie" ,           "aniversaire" : "07/03/2003" },
    { "nom" : "Sinane" ,           "aniversaire" : "15/06/2003" },
    { "nom" : "Lucas Maurin" ,     "aniversaire" : "27/02/2000" },
    { "nom" : "Lina" ,             "aniversaire" : "14/05/2003" },
    { "nom" : "Chloé " ,           "aniversaire" : "20/07/2003" },
    { "nom" : "Estelle" ,          "aniversaire" : "12/03/2003" },
    { "nom" : "Pénélope" ,         "aniversaire" : "30/03/2003" },
    { "nom" : "Laurine" ,          "aniversaire" : "15/01/2003" },
    { "nom" : "Pierrick" ,         "aniversaire" : "07/03/2003" },
    { "nom" : "Amélie" ,           "aniversaire" : "05/02/2002" },
    { "nom" : "Lucas Pomarede" ,   "aniversaire" : "06/09/2003" },
    { "nom" : "Marine Poty" ,      "aniversaire" : "21/09/2003" },
    { "nom" : "Marine Rixte" ,     "aniversaire" : "26/03/1998" },
    { "nom" : "Iakov" ,            "aniversaire" : "16/07/2003" },
    { "nom" : "Océane" ,           "aniversaire" : "08/03/2003" },
    { "nom" : "Mélissa" ,          "aniversaire" : "23/02/2002" },
    { "nom" : "Indigo" ,           "aniversaire" : "25/08/2004" },
    { "nom" : "Yelena" ,           "aniversaire" : "04/08/2003" },
    { "nom" : "Julien Salame" ,    "aniversaire" : "25/07/2003" },
    { "nom" : "Romain" ,           "aniversaire" : "07/08/2003" },
    { "nom" : "Ombeline" ,         "aniversaire" : "21/10/2002" },
    { "nom" : "Maxime" ,           "aniversaire" : "07/12/2003" },
    { "nom" : "Arthur" ,           "aniversaire" : "27/03/2003" },
    { "nom" : "Olga" ,             "aniversaire" : "07/01/2001" },
    { "nom" : "Lucile" ,           "aniversaire" : "20/07/2004" },
    { "nom" : "Mylène " ,          "aniversaire" : "18/10/2003" },
    { "nom" : "Inès" ,             "aniversaire" : "28/07/2004" },
    { "nom" : "Alexis" ,           "aniversaire" : "09/08/2003" },
    { "nom" : "Solène" ,           "aniversaire" : "05/05/2003" },
    { "nom" : "Joo-Hyuk " ,        "aniversaire" : "08/08/1999" }
]

def get_anniversaires_aujourd_hui():
    """
    Retourne la liste des personnes dont l'anniversaire est aujourd'hui.
    
    Returns:
        list: Liste des dictionnaires contenant les informations des personnes 
              dont c'est l'anniversaire aujourd'hui
    """
    aujourd_hui = datetime.now()
    jour_actuel = aujourd_hui.day
    mois_actuel = aujourd_hui.month
    
    anniversaires_aujourd_hui = []
    
    for personne in aniversaires:
        # Parser la date d'anniversaire (format: "dd/mm/yyyy")
        date_anniversaire = datetime.strptime(personne["aniversaire"], "%d/%m/%Y")
        
        # Vérifier si le jour et le mois correspondent à aujourd'hui
        if date_anniversaire.day == jour_actuel and date_anniversaire.month == mois_actuel:
            anniversaires_aujourd_hui.append(personne)
    
    return anniversaires_aujourd_hui




