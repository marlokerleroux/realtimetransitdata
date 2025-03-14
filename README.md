# Realtime Transit Data

Conception d'un afficheur LED permettant la visualisation en temps réel des données de réseaux de transports en commun de 4 communes : Brest, Caen, Nantes, Rennes.
Projet réalisé en équipe dans le cadre d'un projet d'études à l'ISEN Brest.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://web.isen-ouest.fr/gitlab/mkerl222/projet-python/-/graphs/master/charts/contributors
[photo-exemple]: https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Brighton_Old_Steine_bus_stop_stand_T_real_time_information_display_in_October_2013.jpeg/320px-Brighton_Old_Steine_bus_stop_stand_T_real_time_information_display_in_October_2013.jpeg

<!-- ABOUT THE PROJECT -->
## À propos du projet

[![Brighton Old Steine bus stop stand][photo-exemple]](https://commons.wikimedia.org/wiki/File:Brighton_Old_Steine_bus_stop_stand_T_real_time_information_display_in_October_2013.jpeg)

Dans le cadre de leur démarche d'**ouverture des données**, de plus en plus de collectivités locales mettent à la
disposition du public **des informations et des jeux de données** liés à leurs périmètres de compétences. Une
concrétisation fréquente de cette démarche passe par la **mise en place d'API** (interfaces de programmation
applicatives) interrogeables par le grand public.

Dans ce projet, nous nous interessons aux **données temps réel** générées par les sociétés en charge
des transports en commun pour les ensembles urbains dans lesquels les sites d'**Yncréa Ouest** sont implantés (à
savoir : *Brest*, *Caen*, *Nantes* et *Rennes*). Le but du projet est de créer une solution permettant de récupérer des
données, de les traiter, puis de procéder à une phase d'affichage. 

### Technologies et matériels utilisés

Pour mener à bien notre projet, nous avons utilisé les **technologies** et **équipements** suivants :

* [Python 3](https://www.python.org) - Communication API et traitement des données
* [Raspberry Pi 3 Model B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/) - Support du projet
* [Adafruit RGB Matrix HAT + RTC for Raspberry Pi](https://www.adafruit.com/product/2345) - Interface pour la commande de la matrice LED
* [64x32 RGB LED Matrix - 6mm pitch](https://www.adafruit.com/product/2276) - Afficheur LED

### API utilisés

La solution couvre les réseaux de transports des villes où les campus **ISEN-Ouest** sont présents, à savoir : les données en temps réel relatives aux moyens de transports en commun à **Brest** (réseau *Bibus*), **Caen** (réseau *Twisto*), **Nantes** (réseau
*TAN*) et **Rennes** (réseau *STAR*). 

Les liens suivants renvoient vers des pages de description des API :

* Brest : https://geo.pays-de-brest.fr/donnees/Pages/TempsReel.aspx
* Caen : https://data.twisto.fr/explore/dataset/horaires-tr/information
* Nantes : https://data.nantesmetropole.fr/explore/dataset/244400404_api-temps-reel-tan/
* Rennes : https://data.explore.star.fr/explore/dataset/tco-bus-circulation-passages-tr/api/

<!-- GETTING STARTED -->
## Pour débuter

### Prérequis

[urllib](https://docs.python.org/fr/3/library/urllib.html) est un paquet qui collecte plusieurs modules travaillant avec les URLs.
* urllib
  ```sh
  pip install urllib
  ```
[pytz](https://pypi.org/project/pytz/) est un paquet qui permet des calculs de fuseau horaire précis et multiplateformes.
* pytz
  ```sh
  pip install pytz
  ```
  
### Installation

ETAPES NECESSAIRES POUR EXECUTER LE PROJET

1. Cloner le projet
2. Installer les librairies python nécéssaires 
   ```sh
   pip install urllib
   ```
   ```sh
   pip install pytz
   ```
3. Suivre les instructions sur RASPBERRY.md et ECRAN.md
