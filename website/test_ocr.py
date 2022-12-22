import os
import json
import requests
from pathlib import Path

# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver

from .ocr import import_source_content_dependency


def test_import_dependency(monkeypatch):

    test_case_lst = [
        # https://openclassrooms.com/fr/courses/4670706-adoptez-une-architecture-mvc-en-
        {
            "url": "https://openclassrooms.com/fr/courses/4525266-decrivez-et-nettoyez-votre-jeu-de-donnees",
            "dependency_id_lst": [],
            "dependency_label_lst": [],
            "objective_lst": [
                "Quand vous faites vos courses, à quelle vitesse consommez-vous vos produits ?",
                "Combien faites-vous de stock ?",
                "Consommez-vous plus en début ou en fin de mois ? les week-ends ?",
                "Êtes-vous plus dépensier lorsque vous avez beaucoup d'argent sur votre compte ?",
                "etc",
                "Nettoyer un jeu de données",
                "Représenter les variables",
                "Réaliser une analyse univariée",
                "Réaliser une analyse bivariée",
            ],
        },
        {
            "url": "https://openclassrooms.com/fr/courses/4425076-decouvrez-le-framework-django",
            "dependency_id_lst": [
                "1603881",
                "4262331",
                "4302126",
                "4425111",
            ],
            "dependency_label_lst": [
                "apprenez-a-creer-votre-site-web-avec-html5-et-css3",
                "demarrez-votre-projet-avec-python",
                "decouvrez-la-programmation-orientee-objet-avec-python",
                "perfectionnez-vous-en-python",
            ],
            "objective_lst": [
                "Utiliser Django pour créer une application professionnelle",
                "Organiser un projet Django en suivant de bonnes pratiques",
                "Utiliser l'ORM de Django pour interagir avec la base de données",
                "Créer des gabarits",
                "Tester un projet Django avec des tests unitaires",
                "Mettre en ligne une application Django sur Heroku",
            ],
        },
        {
            "url": "https://openclassrooms.com/fr/courses/3306901-creez-des-pages-web-interactives-avec-javascript",
            "dependency_id_lst": [
                "1603881",
                # "2984401",
                "6175841",
            ],
            "dependency_label_lst": [
                "apprenez-a-creer-votre-site-web-avec-html5-et-css3",
                # "apprenez-a-coder-avec-javascript",
                "apprenez-a-programmer-avec-javascript",
            ],
            "objective_lst": ["un éditeur de code", "Mozilla Firefox ou Chrome"],
        },
        {
            "url": "https://openclassrooms.com/fr/courses/4664381-realisez-une-application-web-avec-react-js",
            "dependency_id_lst": [
                # "2984401",
                "6175841",
                "5641796",
            ],
            "dependency_label_lst": [
                # "apprenez-a-coder-avec-javascript",
                "apprenez-a-programmer-avec-javascript",
                "adoptez-visual-studio-comme-environnement-de-developpement",
            ],
            "objective_lst": [
                "Être en mesure d'expliquer les concepts fondamentaux de React, et ce qui le différencie d'autres frameworks",
                "Mettre en place un projet avec Create React App (CRA)",
                "Créer des composants React complets avec la syntaxe JavaScript ES2015 et l'extension JSX",
                "Gérer des formulaires avec ou sans contrôle de saisie",
                "Tester ses composants React",
            ],
        },
        {
            "url": "https://openclassrooms.com/fr/courses/4525361-realisez-un-dashboard-avec-vos-donnees",
            "dependency_id_lst": [
                "4425066",
                "1603881",
                "6175841",
            ],
            "dependency_label_lst": [
                "concevez-un-site-avec-flask",
                "apprenez-a-creer-votre-site-web-avec-html5-et-css3",
                "apprenez-a-programmer-avec-javascript",
            ],
            "objective_lst": [
                "Identifier les étapes de création d’un dashboard",
                "Réaliser un dashboard avec Tableau",
                "Réaliser un dashboard avec les langages de la programmation web",
            ],
        },
        {
            "url": "https://openclassrooms.com/fr/courses/1603881-apprenez-a-creer-votre-site-web-avec-html5-et-css3",
            "dependency_id_lst": [],
            "dependency_label_lst": [],
            "objective_lst": [
                "utiliser du code HTML",
                "structurer une page web en HTML",
                "utiliser du code CSS",
                "mettre en forme une page web en CSS",
                "organiser les éléments d’une page web grâce au CSS",
                "modifier l'agencement d'une page HTML avec CSS",
                "intégrer des formules dans une page web",
                "adapter une page pour les petites résolutions en CSS",
            ],
        },
        {
            "url": "https://openclassrooms.com/fr/courses/6175841-apprenez-a-programmer-avec-javascript",
            "dependency_id_lst": [
                "4366701",
            ],
            "dependency_label_lst": [
                "decouvrez-le-fonctionnement-des-algorithmes",
            ],
            "objective_lst": [
                "Utiliser les données et les types de données dans JavaScript",
                "Gérer la logique d'un programme en JavaScript (conditions, boucles et erreurs)",
                "Écrire du code propre et facile à maintenir à l'aide de méthodes en JavaScript",
            ],
        },
        {
            "url": "https://openclassrooms.com/fr/courses/4366701-decouvrez-le-fonctionnement-des-algorithmes",
            "dependency_id_lst": [],
            "dependency_label_lst": [],
            "objective_lst": [
                "Mettre en œuvre un algorithme simple",
                "Sélectionner les bonnes méthodes pour résoudre un problème",
                "Utiliser les notions basiques en programmation : variables, fonctions, boucles et structures conditionnelles",
                "Manipuler les structures de données essentielles : tableaux, listes chaînées, tables de hachage",
                "Créer des fonctions récursives",
                "Calculer la complexité d’un algorithme",
            ],
        },
    ]

    with WebDriver() as driver:

        for idx, test_case_dct in enumerate(test_case_lst):

            dependency_dct = import_source_content_dependency(
                driver, test_case_dct["url"]
            )

            objective_lst = dependency_dct["objective_lst"]
            if objective_lst:
                for objective_idx, objective in enumerate(
                    dependency_dct["objective_lst"]
                ):
                    assert objective == test_case_dct["objective_lst"][objective_idx]
            else:
                assert not test_case_dct["objective_lst"]

            dependency_lst = dependency_dct["dependency_lst"]
            print(dependency_lst)
            if dependency_lst:
                for idx, dependency in enumerate(dependency_dct["dependency_lst"]):
                    assert dependency[0] == test_case_dct["dependency_id_lst"][idx]
                    assert dependency[1] == test_case_dct["dependency_label_lst"][idx]
            else:
                assert not test_case_dct["dependency_id_lst"]
                assert not test_case_dct["dependency_label_lst"]


# [TODO] Skip
def test_deprecated():

    test_case = [
        "https://openclassrooms.com/fr/courses/2984401-apprenez-a-coder-avec-javascript"
    ]
