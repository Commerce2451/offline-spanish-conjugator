#!/usr/bin/env python3
from flask import Flask, request
import warnings
import mlconjug3

warnings.filterwarnings("ignore")

app = Flask(__name__)
conjugator = mlconjug3.Conjugator(language="es")

VERB_DEFINITIONS = {
    "hablar": {
        "english": "to speak; to talk",
        "notes": "Use hablar for speaking, talking, or having a conversation.",
        "example": "Me gusta hablar español.",
        "tags": ["communication", "regular -ar"],
    },
    "tomar": {
        "english": "to take; to drink",
        "notes": "Tomar can mean to take something, to drink something, or to take transportation.",
        "example": "Voy a tomar café por la mañana.",
        "tags": ["daily life", "regular -ar"],
    },
    "comer": {
        "english": "to eat",
        "notes": "Use comer for eating food or having a meal.",
        "example": "Vamos a comer juntos.",
        "tags": ["food", "regular -er"],
    },
    "vivir": {
        "english": "to live",
        "notes": "Use vivir for where someone lives or how someone experiences life.",
        "example": "Quiero vivir cerca del parque.",
        "tags": ["life", "regular -ir"],
    },
    "estudiar": {
        "english": "to study",
        "notes": "Use estudiar for school, practice, review, or learning a subject.",
        "example": "Necesito estudiar para el examen.",
        "tags": ["education", "regular -ar"],
    },
    "trabajar": {
        "english": "to work",
        "notes": "Use trabajar for jobs, labor, projects, and work activities.",
        "example": "Trabajo en equipo todos los días.",
        "tags": ["work", "regular -ar"],
    },
    "caminar": {
        "english": "to walk",
        "notes": "Use caminar for walking, either as transportation or exercise.",
        "example": "Me gusta caminar por el parque.",
        "tags": ["movement", "regular -ar"],
    },
    "beber": {
        "english": "to drink",
        "notes": "Use beber specifically for drinking liquids.",
        "example": "Debo beber más agua.",
        "tags": ["food", "regular -er"],
    },
    "leer": {
        "english": "to read",
        "notes": "Use leer for reading books, signs, messages, instructions, and articles.",
        "example": "Me gusta leer libros en español.",
        "tags": ["education", "regular -er"],
    },
    "escribir": {
        "english": "to write",
        "notes": "Use escribir for writing messages, letters, notes, and documents.",
        "example": "Voy a escribir un correo electrónico.",
        "tags": ["communication", "regular -ir"],
    },
    "aprender": {
        "english": "to learn",
        "notes": "Use aprender for gaining knowledge or skills.",
        "example": "Quiero aprender palabras nuevas.",
        "tags": ["education", "regular -er"],
    },
    "correr": {
        "english": "to run",
        "notes": "Use correr for running, racing, or moving quickly on foot.",
        "example": "Voy a correr por la mañana.",
        "tags": ["movement", "regular -er"],
    },
    "abrir": {
        "english": "to open",
        "notes": "Use abrir for opening doors, windows, books, stores, files, or apps.",
        "example": "Voy a abrir la puerta.",
        "tags": ["daily life", "regular -ir"],
    },
    "recibir": {
        "english": "to receive",
        "notes": "Use recibir for receiving messages, calls, packages, help, or news.",
        "example": "Espero recibir buenas noticias.",
        "tags": ["communication", "regular -ir"],
    },
    "subir": {
        "english": "to go up; to upload",
        "notes": "Use subir for going up, climbing, getting on a bus, or uploading files.",
        "example": "Voy a subir los archivos.",
        "tags": ["movement", "technology", "regular -ir"],
    },
    "ser": {
        "english": "to be",
        "notes": "Use ser for identity, origin, profession, time, and lasting characteristics.",
        "example": "Soy estudiante de español.",
        "tags": ["core verb", "irregular"],
    },
    "estar": {
        "english": "to be",
        "notes": "Use estar for location, condition, emotions, and temporary states.",
        "example": "Estoy en casa.",
        "tags": ["core verb", "irregular"],
    },
    "ir": {
        "english": "to go",
        "notes": "Use ir for going somewhere or for near-future plans with ir a + infinitive.",
        "example": "Voy a estudiar esta noche.",
        "tags": ["core verb", "movement", "irregular"],
    },
    "tener": {
        "english": "to have",
        "notes": "Use tener for possession, age, obligations, and common expressions like tener que.",
        "example": "Tengo que trabajar mañana.",
        "tags": ["core verb", "irregular"],
    },
    "hacer": {
        "english": "to do; to make",
        "notes": "Use hacer for doing tasks, making things, weather expressions, and time expressions.",
        "example": "Voy a hacer la tarea.",
        "tags": ["core verb", "irregular"],
    },
    "poder": {
        "english": "to be able to; can",
        "notes": "Use poder for ability, possibility, and permission.",
        "example": "Puedo ayudarte hoy.",
        "tags": ["modal verb", "irregular"],
    },
    "querer": {
        "english": "to want; to love",
        "notes": "Use querer for wanting something or loving someone.",
        "example": "Quiero aprender más español.",
        "tags": ["emotion", "modal verb", "irregular"],
    },
    "decir": {
        "english": "to say; to tell",
        "notes": "Use decir for saying words, telling information, or reporting what someone says.",
        "example": "Quiero decir la verdad.",
        "tags": ["communication", "irregular"],
    },
    "venir": {
        "english": "to come",
        "notes": "Use venir for coming toward a place, speaker, event, or situation.",
        "example": "Voy a venir a la reunión.",
        "tags": ["movement", "irregular"],
    },
    "poner": {
        "english": "to put; to place",
        "notes": "Use poner for putting, placing, setting, or turning something on.",
        "example": "Voy a poner el libro en la mesa.",
        "tags": ["daily life", "irregular"],
    },
    "salir": {
        "english": "to leave; to go out",
        "notes": "Use salir for leaving a place, going out, or departing.",
        "example": "Voy a salir después del trabajo.",
        "tags": ["movement", "irregular"],
    },
    "dar": {
        "english": "to give",
        "notes": "Use dar for giving something, offering help, or handing something to someone.",
        "example": "Voy a dar un regalo a mi amigo.",
        "tags": ["daily life", "irregular"],
    },
    "ver": {
        "english": "to see",
        "notes": "Use ver for seeing, watching, or looking at something.",
        "example": "Quiero ver una película.",
        "tags": ["perception", "irregular"],
    },
    "saber": {
        "english": "to know",
        "notes": "Use saber for knowing facts, information, or how to do something.",
        "example": "Sé hablar un poco de español.",
        "tags": ["knowledge", "irregular"],
    },
    "traer": {
        "english": "to bring",
        "notes": "Use traer for bringing something or someone toward the speaker or location.",
        "example": "Voy a traer comida a la fiesta.",
        "tags": ["movement", "irregular"],
    },
    "oír": {
        "english": "to hear",
        "notes": "Use oír for physically hearing sounds or voices.",
        "example": "Puedo oír la música.",
        "tags": ["perception", "irregular"],
    },
    "conocer": {
        "english": "to know; to meet; to be familiar with",
        "notes": "Use conocer for knowing people, places, or being familiar with something.",
        "example": "Quiero conocer la ciudad.",
        "tags": ["knowledge", "irregular"],
    },
}

PERSONS = {
    "1s": "yo",
    "2s": "tú",
    "3s": "él / ella / usted",
    "1p": "nosotros",
    "2p": "vosotros",
    "3p": "ellos / ellas / ustedes",
}

PRONUNCIATIONS = {
    "hablar": {"ipa": "/aˈβlaɾ/", "hint": "ah-BLAR"},
    "tomar": {"ipa": "/toˈmaɾ/", "hint": "toh-MAR"},
    "comer": {"ipa": "/koˈmeɾ/", "hint": "koh-MER"},
    "vivir": {"ipa": "/biˈβiɾ/", "hint": "bee-BEER"},
    "estudiar": {"ipa": "/estuˈðjaɾ/", "hint": "es-too-DYAR"},
    "trabajar": {"ipa": "/tɾaβaˈxaɾ/", "hint": "trah-bah-HAR"},
    "caminar": {"ipa": "/kamiˈnaɾ/", "hint": "kah-mee-NAR"},
    "beber": {"ipa": "/beˈβeɾ/", "hint": "beh-BER"},
    "leer": {"ipa": "/leˈeɾ/", "hint": "leh-ER"},
    "escribir": {"ipa": "/eskɾiˈβiɾ/", "hint": "es-kree-BEER"},
    "aprender": {"ipa": "/apɾenˈdeɾ/", "hint": "ah-pren-DER"},
    "correr": {"ipa": "/koˈreɾ/", "hint": "koh-RER"},
    "abrir": {"ipa": "/aˈβɾiɾ/", "hint": "ah-BREER"},
    "recibir": {"ipa": "/resiˈβiɾ/", "hint": "reh-see-BEER"},
    "subir": {"ipa": "/suˈβiɾ/", "hint": "soo-BEER"},
    "ser": {"ipa": "/seɾ/", "hint": "ser"},
    "estar": {"ipa": "/esˈtaɾ/", "hint": "es-TAR"},
    "ir": {"ipa": "/iɾ/", "hint": "eer"},
    "tener": {"ipa": "/teˈneɾ/", "hint": "teh-NER"},
    "hacer": {"ipa": "/aˈseɾ/", "hint": "ah-SER"},
    "poder": {"ipa": "/poˈðeɾ/", "hint": "poh-DER"},
    "querer": {"ipa": "/keˈɾeɾ/", "hint": "keh-RER"},
    "decir": {"ipa": "/deˈsiɾ/", "hint": "deh-SEER"},
    "venir": {"ipa": "/beˈniɾ/", "hint": "beh-NEER"},
    "poner": {"ipa": "/poˈneɾ/", "hint": "poh-NER"},
    "salir": {"ipa": "/saˈliɾ/", "hint": "sah-LEER"},
    "dar": {"ipa": "/daɾ/", "hint": "dar"},
    "ver": {"ipa": "/beɾ/", "hint": "ber"},
    "saber": {"ipa": "/saˈβeɾ/", "hint": "sah-BER"},
    "traer": {"ipa": "/tɾaˈeɾ/", "hint": "trah-ER"},
    "oír": {"ipa": "/oˈiɾ/", "hint": "oh-EER"},
    "conocer": {"ipa": "/konoˈseɾ/", "hint": "koh-noh-SER"},
}


IRREGULAR_OVERRIDES = {
    "ser": {
        "Present": {
            "1s": "soy", "2s": "eres", "3s": "es",
            "1p": "somos", "2p": "sois", "3p": "son",
        },
        "Imperfect": {
            "1s": "era", "2s": "eras", "3s": "era",
            "1p": "éramos", "2p": "erais", "3p": "eran",
        },
        "Preterite": {
            "1s": "fui", "2s": "fuiste", "3s": "fue",
            "1p": "fuimos", "2p": "fuisteis", "3p": "fueron",
        },
        "Future": {
            "1s": "seré", "2s": "serás", "3s": "será",
            "1p": "seremos", "2p": "seréis", "3p": "serán",
        },
        "Conditional": {
            "1s": "sería", "2s": "serías", "3s": "sería",
            "1p": "seríamos", "2p": "seríais", "3p": "serían",
        },
        "Subjunctive Present": {
            "1s": "sea", "2s": "seas", "3s": "sea",
            "1p": "seamos", "2p": "seáis", "3p": "sean",
        },
    },

    "estar": {
        "Present": {
            "1s": "estoy", "2s": "estás", "3s": "está",
            "1p": "estamos", "2p": "estáis", "3p": "están",
        },
        "Imperfect": {
            "1s": "estaba", "2s": "estabas", "3s": "estaba",
            "1p": "estábamos", "2p": "estabais", "3p": "estaban",
        },
        "Preterite": {
            "1s": "estuve", "2s": "estuviste", "3s": "estuvo",
            "1p": "estuvimos", "2p": "estuvisteis", "3p": "estuvieron",
        },
        "Future": {
            "1s": "estaré", "2s": "estarás", "3s": "estará",
            "1p": "estaremos", "2p": "estaréis", "3p": "estarán",
        },
        "Conditional": {
            "1s": "estaría", "2s": "estarías", "3s": "estaría",
            "1p": "estaríamos", "2p": "estaríais", "3p": "estarían",
        },
        "Subjunctive Present": {
            "1s": "esté", "2s": "estés", "3s": "esté",
            "1p": "estemos", "2p": "estéis", "3p": "estén",
        },
    },

    "ir": {
        "Present": {
            "1s": "voy", "2s": "vas", "3s": "va",
            "1p": "vamos", "2p": "vais", "3p": "van",
        },
        "Imperfect": {
            "1s": "iba", "2s": "ibas", "3s": "iba",
            "1p": "íbamos", "2p": "ibais", "3p": "iban",
        },
        "Preterite": {
            "1s": "fui", "2s": "fuiste", "3s": "fue",
            "1p": "fuimos", "2p": "fuisteis", "3p": "fueron",
        },
        "Future": {
            "1s": "iré", "2s": "irás", "3s": "irá",
            "1p": "iremos", "2p": "iréis", "3p": "irán",
        },
        "Conditional": {
            "1s": "iría", "2s": "irías", "3s": "iría",
            "1p": "iríamos", "2p": "iríais", "3p": "irían",
        },
        "Subjunctive Present": {
            "1s": "vaya", "2s": "vayas", "3s": "vaya",
            "1p": "vayamos", "2p": "vayáis", "3p": "vayan",
        },
    },

    "tener": {
        "Present": {
            "1s": "tengo", "2s": "tienes", "3s": "tiene",
            "1p": "tenemos", "2p": "tenéis", "3p": "tienen",
        },
        "Preterite": {
            "1s": "tuve", "2s": "tuviste", "3s": "tuvo",
            "1p": "tuvimos", "2p": "tuvisteis", "3p": "tuvieron",
        },
        "Future": {
            "1s": "tendré", "2s": "tendrás", "3s": "tendrá",
            "1p": "tendremos", "2p": "tendréis", "3p": "tendrán",
        },
        "Conditional": {
            "1s": "tendría", "2s": "tendrías", "3s": "tendría",
            "1p": "tendríamos", "2p": "tendríais", "3p": "tendrían",
        },
        "Subjunctive Present": {
            "1s": "tenga", "2s": "tengas", "3s": "tenga",
            "1p": "tengamos", "2p": "tengáis", "3p": "tengan",
        },
    },

    "hacer": {
        "Present": {
            "1s": "hago", "2s": "haces", "3s": "hace",
            "1p": "hacemos", "2p": "hacéis", "3p": "hacen",
        },
        "Preterite": {
            "1s": "hice", "2s": "hiciste", "3s": "hizo",
            "1p": "hicimos", "2p": "hicisteis", "3p": "hicieron",
        },
        "Future": {
            "1s": "haré", "2s": "harás", "3s": "hará",
            "1p": "haremos", "2p": "haréis", "3p": "harán",
        },
        "Conditional": {
            "1s": "haría", "2s": "harías", "3s": "haría",
            "1p": "haríamos", "2p": "haríais", "3p": "harían",
        },
        "Subjunctive Present": {
            "1s": "haga", "2s": "hagas", "3s": "haga",
            "1p": "hagamos", "2p": "hagáis", "3p": "hagan",
        },
    },

    "poder": {
        "Present": {
            "1s": "puedo", "2s": "puedes", "3s": "puede",
            "1p": "podemos", "2p": "podéis", "3p": "pueden",
        },
        "Preterite": {
            "1s": "pude", "2s": "pudiste", "3s": "pudo",
            "1p": "pudimos", "2p": "pudisteis", "3p": "pudieron",
        },
        "Future": {
            "1s": "podré", "2s": "podrás", "3s": "podrá",
            "1p": "podremos", "2p": "podréis", "3p": "podrán",
        },
        "Conditional": {
            "1s": "podría", "2s": "podrías", "3s": "podría",
            "1p": "podríamos", "2p": "podríais", "3p": "podrían",
        },
        "Subjunctive Present": {
            "1s": "pueda", "2s": "puedas", "3s": "pueda",
            "1p": "podamos", "2p": "podáis", "3p": "puedan",
        },
    },

    "querer": {
        "Present": {
            "1s": "quiero", "2s": "quieres", "3s": "quiere",
            "1p": "queremos", "2p": "queréis", "3p": "quieren",
        },
        "Preterite": {
            "1s": "quise", "2s": "quisiste", "3s": "quiso",
            "1p": "quisimos", "2p": "quisisteis", "3p": "quisieron",
        },
        "Future": {
            "1s": "querré", "2s": "querrás", "3s": "querrá",
            "1p": "querremos", "2p": "querréis", "3p": "querrán",
        },
        "Conditional": {
            "1s": "querría", "2s": "querrías", "3s": "querría",
            "1p": "querríamos", "2p": "querríais", "3p": "querrían",
        },
        "Subjunctive Present": {
            "1s": "quiera", "2s": "quieras", "3s": "quiera",
            "1p": "queramos", "2p": "queráis", "3p": "quieran",
        },
    },

    "decir": {
        "Present": {
            "1s": "digo", "2s": "dices", "3s": "dice",
            "1p": "decimos", "2p": "decís", "3p": "dicen",
        },
        "Imperfect": {
            "1s": "decía", "2s": "decías", "3s": "decía",
            "1p": "decíamos", "2p": "decíais", "3p": "decían",
        },
        "Preterite": {
            "1s": "dije", "2s": "dijiste", "3s": "dijo",
            "1p": "dijimos", "2p": "dijisteis", "3p": "dijeron",
        },
        "Future": {
            "1s": "diré", "2s": "dirás", "3s": "dirá",
            "1p": "diremos", "2p": "diréis", "3p": "dirán",
        },
        "Conditional": {
            "1s": "diría", "2s": "dirías", "3s": "diría",
            "1p": "diríamos", "2p": "diríais", "3p": "dirían",
        },
        "Subjunctive Present": {
            "1s": "diga", "2s": "digas", "3s": "diga",
            "1p": "digamos", "2p": "digáis", "3p": "digan",
        },
    },

    "venir": {
        "Present": {
            "1s": "vengo", "2s": "vienes", "3s": "viene",
            "1p": "venimos", "2p": "venís", "3p": "vienen",
        },
        "Imperfect": {
            "1s": "venía", "2s": "venías", "3s": "venía",
            "1p": "veníamos", "2p": "veníais", "3p": "venían",
        },
        "Preterite": {
            "1s": "vine", "2s": "viniste", "3s": "vino",
            "1p": "vinimos", "2p": "vinisteis", "3p": "vinieron",
        },
        "Future": {
            "1s": "vendré", "2s": "vendrás", "3s": "vendrá",
            "1p": "vendremos", "2p": "vendréis", "3p": "vendrán",
        },
        "Conditional": {
            "1s": "vendría", "2s": "vendrías", "3s": "vendría",
            "1p": "vendríamos", "2p": "vendríais", "3p": "vendrían",
        },
        "Subjunctive Present": {
            "1s": "venga", "2s": "vengas", "3s": "venga",
            "1p": "vengamos", "2p": "vengáis", "3p": "vengan",
        },
    },

    "poner": {
        "Present": {
            "1s": "pongo", "2s": "pones", "3s": "pone",
            "1p": "ponemos", "2p": "ponéis", "3p": "ponen",
        },
        "Imperfect": {
            "1s": "ponía", "2s": "ponías", "3s": "ponía",
            "1p": "poníamos", "2p": "poníais", "3p": "ponían",
        },
        "Preterite": {
            "1s": "puse", "2s": "pusiste", "3s": "puso",
            "1p": "pusimos", "2p": "pusisteis", "3p": "pusieron",
        },
        "Future": {
            "1s": "pondré", "2s": "pondrás", "3s": "pondrá",
            "1p": "pondremos", "2p": "pondréis", "3p": "pondrán",
        },
        "Conditional": {
            "1s": "pondría", "2s": "pondrías", "3s": "pondría",
            "1p": "pondríamos", "2p": "pondríais", "3p": "pondrían",
        },
        "Subjunctive Present": {
            "1s": "ponga", "2s": "pongas", "3s": "ponga",
            "1p": "pongamos", "2p": "pongáis", "3p": "pongan",
        },
    },

    "salir": {
        "Present": {
            "1s": "salgo", "2s": "sales", "3s": "sale",
            "1p": "salimos", "2p": "salís", "3p": "salen",
        },
        "Imperfect": {
            "1s": "salía", "2s": "salías", "3s": "salía",
            "1p": "salíamos", "2p": "salíais", "3p": "salían",
        },
        "Preterite": {
            "1s": "salí", "2s": "saliste", "3s": "salió",
            "1p": "salimos", "2p": "salisteis", "3p": "salieron",
        },
        "Future": {
            "1s": "saldré", "2s": "saldrás", "3s": "saldrá",
            "1p": "saldremos", "2p": "saldréis", "3p": "saldrán",
        },
        "Conditional": {
            "1s": "saldría", "2s": "saldrías", "3s": "saldría",
            "1p": "saldríamos", "2p": "saldríais", "3p": "saldrían",
        },
        "Subjunctive Present": {
            "1s": "salga", "2s": "salgas", "3s": "salga",
            "1p": "salgamos", "2p": "salgáis", "3p": "salgan",
        },
    },

    "dar": {
        "Present": {
            "1s": "doy", "2s": "das", "3s": "da",
            "1p": "damos", "2p": "dais", "3p": "dan",
        },
        "Imperfect": {
            "1s": "daba", "2s": "dabas", "3s": "daba",
            "1p": "dábamos", "2p": "dabais", "3p": "daban",
        },
        "Preterite": {
            "1s": "di", "2s": "diste", "3s": "dio",
            "1p": "dimos", "2p": "disteis", "3p": "dieron",
        },
        "Future": {
            "1s": "daré", "2s": "darás", "3s": "dará",
            "1p": "daremos", "2p": "daréis", "3p": "darán",
        },
        "Conditional": {
            "1s": "daría", "2s": "darías", "3s": "daría",
            "1p": "daríamos", "2p": "daríais", "3p": "darían",
        },
        "Subjunctive Present": {
            "1s": "dé", "2s": "des", "3s": "dé",
            "1p": "demos", "2p": "deis", "3p": "den",
        },
    },

    "ver": {
        "Present": {
            "1s": "veo", "2s": "ves", "3s": "ve",
            "1p": "vemos", "2p": "veis", "3p": "ven",
        },
        "Imperfect": {
            "1s": "veía", "2s": "veías", "3s": "veía",
            "1p": "veíamos", "2p": "veíais", "3p": "veían",
        },
        "Preterite": {
            "1s": "vi", "2s": "viste", "3s": "vio",
            "1p": "vimos", "2p": "visteis", "3p": "vieron",
        },
        "Future": {
            "1s": "veré", "2s": "verás", "3s": "verá",
            "1p": "veremos", "2p": "veréis", "3p": "verán",
        },
        "Conditional": {
            "1s": "vería", "2s": "verías", "3s": "vería",
            "1p": "veríamos", "2p": "veríais", "3p": "verían",
        },
        "Subjunctive Present": {
            "1s": "vea", "2s": "veas", "3s": "vea",
            "1p": "veamos", "2p": "veáis", "3p": "vean",
        },
    },

    "saber": {
        "Present": {
            "1s": "sé", "2s": "sabes", "3s": "sabe",
            "1p": "sabemos", "2p": "sabéis", "3p": "saben",
        },
        "Imperfect": {
            "1s": "sabía", "2s": "sabías", "3s": "sabía",
            "1p": "sabíamos", "2p": "sabíais", "3p": "sabían",
        },
        "Preterite": {
            "1s": "supe", "2s": "supiste", "3s": "supo",
            "1p": "supimos", "2p": "supisteis", "3p": "supieron",
        },
        "Future": {
            "1s": "sabré", "2s": "sabrás", "3s": "sabrá",
            "1p": "sabremos", "2p": "sabréis", "3p": "sabrán",
        },
        "Conditional": {
            "1s": "sabría", "2s": "sabrías", "3s": "sabría",
            "1p": "sabríamos", "2p": "sabríais", "3p": "sabrían",
        },
        "Subjunctive Present": {
            "1s": "sepa", "2s": "sepas", "3s": "sepa",
            "1p": "sepamos", "2p": "sepáis", "3p": "sepan",
        },
    },

    "traer": {
        "Present": {
            "1s": "traigo", "2s": "traes", "3s": "trae",
            "1p": "traemos", "2p": "traéis", "3p": "traen",
        },
        "Imperfect": {
            "1s": "traía", "2s": "traías", "3s": "traía",
            "1p": "traíamos", "2p": "traíais", "3p": "traían",
        },
        "Preterite": {
            "1s": "traje", "2s": "trajiste", "3s": "trajo",
            "1p": "trajimos", "2p": "trajisteis", "3p": "trajeron",
        },
        "Future": {
            "1s": "traeré", "2s": "traerás", "3s": "traerá",
            "1p": "traeremos", "2p": "traeréis", "3p": "traerán",
        },
        "Conditional": {
            "1s": "traería", "2s": "traerías", "3s": "traería",
            "1p": "traeríamos", "2p": "traeríais", "3p": "traerían",
        },
        "Subjunctive Present": {
            "1s": "traiga", "2s": "traigas", "3s": "traiga",
            "1p": "traigamos", "2p": "traigáis", "3p": "traigan",
        },
    },

    "oír": {
        "Present": {
            "1s": "oigo", "2s": "oyes", "3s": "oye",
            "1p": "oímos", "2p": "oís", "3p": "oyen",
        },
        "Imperfect": {
            "1s": "oía", "2s": "oías", "3s": "oía",
            "1p": "oíamos", "2p": "oíais", "3p": "oían",
        },
        "Preterite": {
            "1s": "oí", "2s": "oíste", "3s": "oyó",
            "1p": "oímos", "2p": "oísteis", "3p": "oyeron",
        },
        "Future": {
            "1s": "oiré", "2s": "oirás", "3s": "oirá",
            "1p": "oiremos", "2p": "oiréis", "3p": "oirán",
        },
        "Conditional": {
            "1s": "oiría", "2s": "oirías", "3s": "oiría",
            "1p": "oiríamos", "2p": "oiríais", "3p": "oirían",
        },
        "Subjunctive Present": {
            "1s": "oiga", "2s": "oigas", "3s": "oiga",
            "1p": "oigamos", "2p": "oigáis", "3p": "oigan",
        },
    },

    "conocer": {
        "Present": {
            "1s": "conozco", "2s": "conoces", "3s": "conoce",
            "1p": "conocemos", "2p": "conocéis", "3p": "conocen",
        },
        "Imperfect": {
            "1s": "conocía", "2s": "conocías", "3s": "conocía",
            "1p": "conocíamos", "2p": "conocíais", "3p": "conocían",
        },
        "Preterite": {
            "1s": "conocí", "2s": "conociste", "3s": "conoció",
            "1p": "conocimos", "2p": "conocisteis", "3p": "conocieron",
        },
        "Future": {
            "1s": "conoceré", "2s": "conocerás", "3s": "conocerá",
            "1p": "conoceremos", "2p": "conoceréis", "3p": "conocerán",
        },
        "Conditional": {
            "1s": "conocería", "2s": "conocerías", "3s": "conocería",
            "1p": "conoceríamos", "2p": "conoceríais", "3p": "conocerían",
        },
        "Subjunctive Present": {
            "1s": "conozca", "2s": "conozcas", "3s": "conozca",
            "1p": "conozcamos", "2p": "conozcáis", "3p": "conozcan",
        },
    },
}

EXAMPLE_SUBJECTS = {
    "1s": "Yo",
    "2s": "Tú",
    "3s": "Él",
    "1p": "Nosotros",
    "2p": "Vosotros",
    "3p": "Ellos",
}

DEFINITIONS = {
    "Indicative": "Used for facts, real actions, habits, and statements.",
    "Subjunctive": "Used for wishes, doubt, emotion, uncertainty, recommendations, and non-factual situations.",
    "Conditional": "Used for would/could situations, polite requests, and hypotheticals.",
    "Imperative": "Used to give commands or instructions.",
    "Non-finite Forms": "Verb forms that do not change by person.",
    "Present": "Used for actions happening now, habits, and general truths.",
    "Imperfect": "Used for ongoing, repeated, or background actions in the past.",
    "Preterite": "Used for completed actions in the past.",
    "Future": "Used for actions that will happen in the future.",
    "Present Perfect": "Used for actions that have happened and are relevant to the present.",
    "Pluperfect": "Used for actions that had happened before another past action.",
    "Future Perfect": "Used for actions that will have been completed before a future point.",
    "Imperfect Subjunctive (-ra)": "Used for hypothetical, doubtful, or uncertain situations in the past.",
    "Imperfect Subjunctive (-se)": "An alternate form of the imperfect subjunctive.",
    "Conditional Perfect": "Used for actions that would have happened under certain conditions.",
    "Affirmative": "Positive commands.",
    "Negative": "Negative commands.",
}

HABER = {
    "present_perfect": {
        "1s": "he", "2s": "has", "3s": "ha",
        "1p": "hemos", "2p": "habéis", "3p": "han",
    },
    "pluperfect": {
        "1s": "había", "2s": "habías", "3s": "había",
        "1p": "habíamos", "2p": "habíais", "3p": "habían",
    },
    "future_perfect": {
        "1s": "habré", "2s": "habrás", "3s": "habrá",
        "1p": "habremos", "2p": "habréis", "3p": "habrán",
    },
    "conditional_perfect": {
        "1s": "habría", "2s": "habrías", "3s": "habría",
        "1p": "habríamos", "2p": "habríais", "3p": "habrían",
    },
}


IRREGULAR_PAST_PARTICIPLES = {
    "decir": "dicho",
    "hacer": "hecho",
    "poner": "puesto",
    "ver": "visto",
    "traer": "traído",
    "oír": "oído",
}

IRREGULAR_GERUNDS = {
    "decir": "diciendo",
    "venir": "viniendo",
    "poder": "pudiendo",
    "traer": "trayendo",
    "oír": "oyendo",
}

VERB_CONTEXTS = {
    "hablar": {
        "1s": "con mi amigo por teléfono",
        "2s": "español en clase",
        "3s": "con su familia",
        "1p": "sobre el trabajo",
        "2p": "muy rápido",
        "3p": "con el profesor",
    },
    "tomar": {
        "1s": "café por la mañana",
        "2s": "agua después de correr",
        "3s": "el autobús al trabajo",
        "1p": "notas en clase",
        "2p": "fotos durante el viaje",
        "3p": "decisiones importantes",
    },
    "comer": {
        "1s": "fruta en el desayuno",
        "2s": "arroz con pollo",
        "3s": "en un restaurante",
        "1p": "juntos los domingos",
        "2p": "verduras frescas",
        "3p": "pizza los viernes",
    },
    "vivir": {
        "1s": "en una casa pequeña",
        "2s": "cerca del parque",
        "3s": "en la ciudad",
        "1p": "en un apartamento",
        "2p": "lejos del centro",
        "3p": "con sus padres",
    },
    "estudiar": {
        "1s": "español por la noche",
        "2s": "para el examen",
        "3s": "en la biblioteca",
        "1p": "juntos después del trabajo",
        "2p": "mucho en la universidad",
        "3p": "matemáticas todos los días",
    },
    "trabajar": {
        "1s": "en una fábrica",
        "2s": "los fines de semana",
        "3s": "en una oficina",
        "1p": "en equipo",
        "2p": "muchas horas",
        "3p": "en el taller",
    },
    "caminar": {
        "1s": "por el parque",
        "2s": "hasta la tienda",
        "3s": "con su perro",
        "1p": "por la playa",
        "2p": "por la ciudad",
        "3p": "después de cenar",
    },
    "beber": {
        "1s": "agua fría",
        "2s": "café por la tarde",
        "3s": "té caliente",
        "1p": "jugo en el desayuno",
        "2p": "agua durante el viaje",
        "3p": "leche con la cena",
    },
    "leer": {
        "1s": "un libro interesante",
        "2s": "el periódico",
        "3s": "una carta",
        "1p": "historias en español",
        "2p": "las instrucciones",
        "3p": "muchos artículos",
    },
    "escribir": {
        "1s": "un correo electrónico",
        "2s": "una carta",
        "3s": "en su cuaderno",
        "1p": "mensajes en español",
        "2p": "notas importantes",
        "3p": "historias cortas",
    },
    "aprender": {
        "1s": "palabras nuevas",
        "2s": "la gramática",
        "3s": "muy rápido",
        "1p": "juntos en clase",
        "2p": "con práctica",
        "3p": "algo nuevo cada día",
    },
    "correr": {
        "1s": "por la mañana",
        "2s": "en el parque",
        "3s": "muy rápido",
        "1p": "después del trabajo",
        "2p": "en la pista",
        "3p": "todos los días",
    },
    "abrir": {
        "1s": "la puerta",
        "2s": "la ventana",
        "3s": "el libro",
        "1p": "la tienda temprano",
        "2p": "los regalos",
        "3p": "sus mochilas",
    },
    "recibir": {
        "1s": "un mensaje",
        "2s": "una llamada",
        "3s": "una carta",
        "1p": "buenas noticias",
        "2p": "ayuda del profesor",
        "3p": "paquetes en casa",
    },
    "subir": {
        "1s": "las escaleras",
        "2s": "una foto a internet",
        "3s": "al segundo piso",
        "1p": "a la montaña",
        "2p": "los archivos",
        "3p": "al autobús",
    },
    "venir": {
        "1s": "a casa después del trabajo",
        "2s": "a clase temprano",
        "3s": "con sus amigos",
        "1p": "a la reunión",
        "2p": "al parque",
        "3p": "mañana por la tarde",
    },
    "poner": {
        "1s": "el libro sobre la mesa",
        "2s": "la llave en la puerta",
        "3s": "la mochila en el suelo",
        "1p": "la comida en la mesa",
        "2p": "los papeles en orden",
        "3p": "sus cosas en la habitación",
    },
    "salir": {
        "1s": "de casa temprano",
        "2s": "del trabajo tarde",
        "3s": "con sus amigos",
        "1p": "a caminar",
        "2p": "de la escuela",
        "3p": "por la noche",
    },
    "dar": {
        "1s": "una respuesta clara",
        "2s": "un regalo a tu amigo",
        "3s": "clases de español",
        "1p": "gracias por la ayuda",
        "2p": "buenos consejos",
        "3p": "comida a los niños",
    },
    "ver": {
        "1s": "una película en casa",
        "2s": "las noticias por la mañana",
        "3s": "a su familia los domingos",
        "1p": "el partido juntos",
        "2p": "muchas fotos",
        "3p": "la televisión por la noche",
    },
    "saber": {
        "1s": "la respuesta correcta",
        "2s": "mucho de tecnología",
        "3s": "la verdad",
        "1p": "cómo resolver el problema",
        "2p": "la dirección",
        "3p": "qué hacer",
    },
    "traer": {
        "1s": "comida para la cena",
        "2s": "tu mochila a clase",
        "3s": "flores para su madre",
        "1p": "herramientas al taller",
        "2p": "los documentos necesarios",
        "3p": "buenas noticias",
    },
    "oír": {
        "1s": "música en la radio",
        "2s": "ruidos en la calle",
        "3s": "la voz del profesor",
        "1p": "el anuncio claramente",
        "2p": "la conversación",
        "3p": "el teléfono sonar",
    },
    "conocer": {
        "1s": "a muchas personas nuevas",
        "2s": "bien la ciudad",
        "3s": "a mi hermano",
        "1p": "ese restaurante",
        "2p": "la historia del lugar",
        "3p": "a los vecinos",
    },
}

def heading(level, title):
    definition = DEFINITIONS.get(title, "")
    if definition:
        return f"<h{level}>{title}</h{level}><p class='definition'>{definition}</p>"
    return f"<h{level}>{title}</h{level}>"

def ending_type(verb):
    if verb.endswith("ar"):
        return "ar"
    if verb.endswith("er"):
        return "er"
    if verb.endswith("ir"):
        return "ir"
    return ""

def stem(verb):
    return verb[:-2]

def past_participle(verb):
    if verb in IRREGULAR_PAST_PARTICIPLES:
        return IRREGULAR_PAST_PARTICIPLES[verb]

    kind = ending_type(verb)
    if kind == "ar":
        return stem(verb) + "ado"
    if kind in ["er", "ir"]:
        return stem(verb) + "ido"
    return verb

def gerund(verb):
    if verb in IRREGULAR_GERUNDS:
        return IRREGULAR_GERUNDS[verb]

    kind = ending_type(verb)
    if kind == "ar":
        return stem(verb) + "ando"
    if kind in ["er", "ir"]:
        return stem(verb) + "iendo"
    return verb

def verb_type_label(verb):
    kind = ending_type(verb)
    if kind:
        return f"-{kind.upper()} verb"
    return "Verb"

def regularity_label(verb):
    if verb in IRREGULAR_OVERRIDES or verb in IRREGULAR_PAST_PARTICIPLES or verb in IRREGULAR_GERUNDS:
        return "Irregular / manually verified"
    return "Regular"

def difficulty_label(verb):
    if verb in ["hablar", "tomar", "comer", "vivir", "estudiar", "trabajar"]:
        return "Beginner"
    if verb in IRREGULAR_OVERRIDES:
        return "Intermediate"
    return "Beginner / intermediate"

def pronunciation_block(verb):
    pronunciation = PRONUNCIATIONS.get(verb, {})
    ipa = pronunciation.get("ipa", "")
    hint = pronunciation.get("hint", "")

    if not ipa and not hint:
        return ""

    hint_html = f"<p><strong>Sound hint:</strong> {hint}</p>" if hint else ""
    ipa_html = f"<p><strong>IPA:</strong> <code>{ipa}</code></p>" if ipa else ""

    return f"""
    <div class="pronunciation-card">
        <h3>Pronunciation</h3>
        {ipa_html}
        {hint_html}
        <p class="small-note">Pronunciation hints are approximate learning aids. IPA is included when available.</p>
    </div>
    """

def verb_definition_box(verb):
    entry = VERB_DEFINITIONS.get(verb)

    if not entry:
        return f"""
        <div class="verb-card">
            <h2>{verb}</h2>
            <p><strong>English meaning:</strong> No local definition found yet.</p>
            <p>Add this verb to <code>VERB_DEFINITIONS</code> in <code>app.py</code>.</p>
            {pronunciation_block(verb)}
        </div>
        """

    # Backward compatibility: allow older simple string definitions.
    if isinstance(entry, str):
        return f"""
        <div class="verb-card">
            <h2>{verb}</h2>
            <div class="metadata-row">
                <span class="badge">{verb_type_label(verb)}</span>
                <span class="badge">{regularity_label(verb)}</span>
                <span class="badge">{difficulty_label(verb)}</span>
            </div>
            <p><strong>English meaning:</strong> {entry}</p>
            {pronunciation_block(verb)}
        </div>
        """

    english = entry.get("english", "")
    notes = entry.get("notes", "")
    example = entry.get("example", "")
    tags = entry.get("tags", [])

    tags_html = ""
    if tags:
        tag_items = "".join(f"<span class='tag'>{tag}</span>" for tag in tags)
        tags_html = f"<div class='tag-row'><strong>Tags:</strong> {tag_items}</div>"

    return f"""
    <div class="verb-card">
        <h2>{verb}</h2>

        <div class="metadata-row">
            <span class="badge">{verb_type_label(verb)}</span>
            <span class="badge">{regularity_label(verb)}</span>
            <span class="badge">{difficulty_label(verb)}</span>
        </div>

        <p><strong>English meaning:</strong> {english}</p>
        <p><strong>Usage notes:</strong> {notes}</p>
        <p><strong>Example:</strong> <em>{example}</em></p>
        {tags_html}
        {pronunciation_block(verb)}
    </div>
    """

def context_for(verb, person):
    default_contexts = {
        "1s": "todos los días",
        "2s": "con frecuencia",
        "3s": "por la tarde",
        "1p": "juntos",
        "2p": "en clase",
        "3p": "en casa",
    }

    return VERB_CONTEXTS.get(verb, default_contexts).get(person, "")

def make_example(verb, person, form, title):
    subject = EXAMPLE_SUBJECTS.get(person, "")
    context = context_for(verb, person)

    if not subject:
        return ""

    lower_subject = subject.lower()

    if title == "Present":
        return f"{subject} {form} {context}."

    if title == "Imperfect":
        return f"Antes, {subject.lower()} {form} {context}."

    if title == "Preterite":
        return f"Ayer, {subject.lower()} {form} {context}."

    if title == "Future":
        return f"Mañana, {subject.lower()} {form} {context}."

    if title == "Present Perfect":
        return f"Hoy, {subject.lower()} {form} {context}."

    if title == "Pluperfect":
        return f"{subject} ya {form} {context} antes de salir."

    if title == "Future Perfect":
        return f"{subject} ya {form} {context} antes de mañana."

    if title == "Conditional":
        return f"{subject} {form} {context} si tuviera tiempo."

    if title == "Conditional Perfect":
        return f"{subject} {form} {context} si hubiera tenido tiempo."

    if title == "Subjunctive Present":
        return f"Espero que {lower_subject} {form} {context}."

    if title == "Imperfect Subjunctive (-ra)":
        return f"Quería que {lower_subject} {form} {context}."

    if title == "Imperfect Subjunctive (-se)":
        return f"Era importante que {lower_subject} {form} {context}."

    return f"{subject} {form} {context}."

def make_rows(forms, title, verb_text):
    html = ["<table>", "<tr><th>Person</th><th>Conjugation</th><th>Example Sentence</th></tr>"]

    for person, form in forms.items():
        example = make_example(verb_text, person, form, title)
        html.append(
            f"<tr><td>{PERSONS[person]}</td><td>{form}</td><td>{example}</td></tr>"
        )

    html.append("</table>")
    return "\n".join(html)

def get_simple_tense(verb_obj, mood, tense, verb_text=None, title=None):
    if (
        verb_text
        and title
        and verb_text in IRREGULAR_OVERRIDES
        and title in IRREGULAR_OVERRIDES[verb_text]
    ):
        return IRREGULAR_OVERRIDES[verb_text][title]

    return verb_obj.conjug_info.get(mood, {}).get(tense, {})

def make_compound_rows(participle, haber_key, title, verb_text):
    forms = {p: f"{aux} {participle}" for p, aux in HABER[haber_key].items()}
    return make_rows(forms, title, verb_text)

def make_imperative(verb_text):
    kind = ending_type(verb_text)
    s = stem(verb_text)

    if kind not in ["ar", "er", "ir"]:
        return ""

    context = VERB_CONTEXTS.get(verb_text, {}).get("2s", "por favor")

    html = [heading(2, "Imperative")]

    if kind == "ar":
        affirmative = {"tú": s+"a", "usted": s+"e", "nosotros": s+"emos", "vosotros": s+"ad", "ustedes": s+"en"}
        negative = {"tú": "no "+s+"es", "usted": "no "+s+"e", "nosotros": "no "+s+"emos", "vosotros": "no "+s+"éis", "ustedes": "no "+s+"en"}
    elif kind == "er":
        affirmative = {"tú": s+"e", "usted": s+"a", "nosotros": s+"amos", "vosotros": s+"ed", "ustedes": s+"an"}
        negative = {"tú": "no "+s+"as", "usted": "no "+s+"a", "nosotros": "no "+s+"amos", "vosotros": "no "+s+"áis", "ustedes": "no "+s+"an"}
    else:
        affirmative = {"tú": s+"e", "usted": s+"a", "nosotros": s+"amos", "vosotros": s+"id", "ustedes": s+"an"}
        negative = {"tú": "no "+s+"as", "usted": "no "+s+"a", "nosotros": "no "+s+"amos", "vosotros": "no "+s+"áis", "ustedes": "no "+s+"an"}

    for title, forms in [("Affirmative", affirmative), ("Negative", negative)]:
        html.append(heading(3, title))
        html.append("<table><tr><th>Person</th><th>Conjugation</th><th>Example Sentence</th></tr>")

        for person, form in forms.items():
            if title == "Affirmative":
                example = f"{form.capitalize()} {context}, por favor."
            else:
                example = f"{form.capitalize()} {context} ahora."

            html.append(f"<tr><td>{person}</td><td>{form}</td><td>{example}</td></tr>")

        html.append("</table>")

    return "\n".join(html)

def make_table(verb_text, verb_obj):
    html = [verb_definition_box(verb_text)]
    pp = past_participle(verb_text)

    html.append(heading(2, "Indicative"))

    for title, mood, tense in [
        ("Present", "Indicativo", "Indicativo presente"),
        ("Imperfect", "Indicativo", "Indicativo pretérito imperfecto"),
        ("Preterite", "Indicativo", "Indicativo pretérito perfecto simple"),
        ("Future", "Indicativo", "Indicativo futuro"),
    ]:
        forms = get_simple_tense(verb_obj, mood, tense, verb_text, title)
        if forms:
            html.append(heading(3, title))
            html.append(make_rows(forms, title, verb_text))

    for title, key in [
        ("Present Perfect", "present_perfect"),
        ("Pluperfect", "pluperfect"),
        ("Future Perfect", "future_perfect"),
    ]:
        html.append(heading(3, title))
        html.append(make_compound_rows(pp, key, title, verb_text))

    html.append(heading(2, "Subjunctive"))

    for title, mood, tense in [
        ("Subjunctive Present", "Subjuntivo", "Subjuntivo presente"),
        ("Imperfect Subjunctive (-ra)", "Subjuntivo", "Subjuntivo pretérito imperfecto 1"),
        ("Imperfect Subjunctive (-se)", "Subjuntivo", "Subjuntivo pretérito imperfecto 2"),
        ("Future", "Subjuntivo", "Subjuntivo futuro"),
    ]:
        forms = get_simple_tense(verb_obj, mood, tense, verb_text, title)
        if forms:
            html.append(heading(3, title))
            html.append(make_rows(forms, title, verb_text))

    html.append(heading(2, "Conditional"))

    forms = get_simple_tense(
        verb_obj,
        "Condicional",
        "Condicional Condicional",
        verb_text,
        "Conditional"
    )
    if forms:
        html.append(heading(3, "Conditional"))
        html.append(make_rows(forms, "Conditional", verb_text))

    html.append(heading(3, "Conditional Perfect"))
    html.append(make_compound_rows(pp, "conditional_perfect", "Conditional Perfect", verb_text))

    html.append(make_imperative(verb_text))

    html.append(heading(2, "Non-finite Forms"))
    html.append(f"""
    <table>
        <tr><th>Form</th><th>Spanish</th><th>Example Sentence</th></tr>
        <tr><td>Infinitive</td><td>{verb_text}</td><td>Me gusta {verb_text}.</td></tr>
        <tr><td>Gerund</td><td>{gerund(verb_text)}</td><td>Estoy {gerund(verb_text)} ahora.</td></tr>
        <tr><td>Past Participle</td><td>{pp}</td><td>He {pp} hoy.</td></tr>
    </table>
    """)

    return "\n".join(html)

@app.route("/", methods=["GET", "POST"])
def home():
    output = ""

    if request.method == "POST":
        verb_text = request.form.get("verb", "").strip().lower()

        try:
            verb_obj = conjugator.conjugate(verb_text)
            output = make_table(verb_text, verb_obj)
        except Exception as e:
            output = f"<p>Error: {e}</p>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Offline Spanish Conjugator</title>
        <style>
            body {{
                font-family: system-ui, sans-serif;
                margin: 30px auto;
                max-width: 1200px;
                line-height: 1.4;
                background: #ffffff;
                color: #111111;
            }}

            body.dark-mode {{
                background: #121212;
                color: #eeeeee;
            }}

            .top-bar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 15px;
                margin-bottom: 25px;
            }}

            .verb-card {{
                border: 1px solid #ccc;
                padding: 15px;
                margin-top: 25px;
                margin-bottom: 25px;
                background: #f8f8f8;
            }}

            body.dark-mode .verb-card {{
                background: #222222;
                border-color: #555555;
            }}

            input[type=text] {{
                width: 260px;
                font-size: 18px;
                padding: 8px;
            }}

            input[type=submit],
            button {{
                font-size: 18px;
                padding: 8px 12px;
                cursor: pointer;
            }}

            table {{
                border-collapse: collapse;
                margin-bottom: 35px;
                width: 100%;
            }}

            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
                vertical-align: top;
            }}

            th {{
                background: #e5e5e5;
            }}

            tr:nth-child(even) {{
                background: #f8f8f8;
            }}

            body.dark-mode th {{
                background: #333333;
            }}

            body.dark-mode td,
            body.dark-mode th {{
                border-color: #555555;
            }}

            body.dark-mode tr:nth-child(even) {{
                background: #222222;
            }}

            body.dark-mode input,
            body.dark-mode button {{
                background: #222222;
                color: #eeeeee;
                border: 1px solid #555555;
            }}

            h2 {{
                margin-top: 35px;
                border-bottom: 2px solid #333;
            }}

            body.dark-mode h2 {{
                border-bottom: 2px solid #eeeeee;
            }}

            .definition {{
                margin-top: -8px;
                margin-bottom: 15px;
                color: #666666;
                font-style: italic;
            }}

            body.dark-mode .definition {{
                color: #bbbbbb;
            }}
        </style>
    </head>

    <body>
        <div class="top-bar">
            <h1>Offline Spanish Conjugator</h1>
            <button onclick="toggleDarkMode()" id="darkButton">🌙 Dark Mode</button>
        </div>

        <form method="post">
            <input type="text" name="verb" placeholder="comer, vivir, hablar" autofocus>
            <input type="submit" value="Conjugate">
        </form>

        {output}

        <script>
            function setButtonText() {{
                const button = document.getElementById("darkButton");
                button.textContent = document.body.classList.contains("dark-mode")
                    ? "☀️ Light Mode"
                    : "🌙 Dark Mode";
            }}

            function toggleDarkMode() {{
                document.body.classList.toggle("dark-mode");
                localStorage.setItem(
                    "theme",
                    document.body.classList.contains("dark-mode") ? "dark" : "light"
                );
                setButtonText();
            }}

            if (localStorage.getItem("theme") === "dark") {{
                document.body.classList.add("dark-mode");
            }}

            setButtonText();
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import threading
    import webbrowser

    def open_browser():
        webbrowser.open("http://127.0.0.1:5000")

    threading.Timer(1.5, open_browser).start()

    app.run(port=5000, debug=True)