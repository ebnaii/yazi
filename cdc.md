## CAHIER DES CHARGES

### A/ Contexte et définition du projet

L'objectif du projet est de créer une distribution Linux orientée pentest. Le but est de fournir lors du téléchargement une machine prête à être utilisée sans besoin de configuration particulière, mais qui peut aussi être modulable si besoin.

Ce projet est divisible en 4 parties, elles-mêmes divisibles en sous-parties :

1. **Gestion de projet** : Cette partie est essentielle et nous permettra d’avancer au mieux pendant toute la durée du projet. Elle comporte un grand nombre d’axes possibles, chacun pouvant s’entremêler, ce qui permettra de délimiter des périmètres propres à chacun et de contrôler l’avancement.

2. **Recompilation du noyau** : Cette étape va permettre de garder uniquement le nécessaire afin d’avoir une machine qui puisse fonctionner avec le minimum de RAM/CPU, assurant ainsi de meilleures performances sur les outils. De plus, étant donné que tous les pentesters n'ont pas les mêmes besoins, certains "sets" d’outils pourront être installés ou non lors de l'installation pour garantir des performances maximales.

3. **Mise en place de conteneurs** : Cette étape va apporter un boost de performances, mais surtout un ordre dans la distribution. Chaque conteneur aura un but spécifique, par exemple un conteneur pourra être orienté sur les tests d’attaques WEB, un autre sur la cryptographie, etc. Il y aura un travail majeur de recherche afin de trouver les outils les plus performants et surtout une utilité dans un cadre propre à chacun.

4. **Développement d’outils** : Bien que le développement d'outils soit un objectif secondaire, il est possible que certains de nos besoins ne soient pas représentés par les outils existants. Dans ce cas, la création ou la reprise d’outils remplissant ces besoins sera nécessaire.

Comme la recompilation du noyau n’est pas suffisante pour permettre une grande accessibilité et visibilité à cette distribution, il va donc falloir créer un ISO afin de permettre l’installation de celle-ci. C’est encore ici un grand point de recherche en amont, afin de déterminer les spécifications nécessaires, qui peuvent dépendre de l’architecture des processeurs disponibles.


### B/ Cahier des charges

#### 1) Contraintes technique de la solution

##### Tableau des fonctionnalités :

| Fonctionnalité                  | Description                                                                                              |
|---------------------------------|----------------------------------------------------------------------------------------------------------|
| Recompilation du noyau          | Garder uniquement les composants essentiels pour optimiser les ressources matérielle                    |
| Utilisation de conteneurs       | Organiser les outils de pentest dans des environnements isolés pour une gestion plus efficace            |
| Recherche et sélection d’outils | Identifier et intégrer les outils de pentest les plus performants et pertinents                         |
| Développement d’outils supplémentaires | Créer ou adapter des outils spécifique pour répondre à des besoins non couverts                 |
| Création d’une image ISO       | Produire une image d’installation facilitant le déploiement de la distribution                            |
| Hardening                       | Renforcer significativement la sécurité et réduire les chances de subir des incidents de sécurité graves |
| Documentation                   | Fournir une documentation complète et accessible pour faciliter l’utilisation et la maintenance        |

##### Tableau des contraintes :

| Contrainte      | Description                                              |
|-----------------|----------------------------------------------------------|
| Performance     | Optimisation des performances pour garantir une utilisation fluide des outils de pentest                    |
| Sécurité        | Assurer la sécurité de la distribution et des outils intégrés contre les attaques potentielles              |
| Modularité      | Permettre une gestion flexible et modulaire de la distribution pour répondre à divers besoins               |
| Compatibilité matérielle | Assurer la compatibilité avec un large éventail de configurations matérielles                      |

#### 2) Technologies utilisées

##### 2.1) Base
Il y a deux possibilités quant à la base de la machine : 

>- **Alpine**
Connu pour sa légèreté et sa sécurité, Alpine Linux offre une base idéale pour une distribution pentest rapide et efficace. Cependant, en raison de sa conception minimaliste, il peut présenter des limitations en termes de disponibilité des logiciels et de compatibilité matérielle. Certaines fonctionnalités avancées ou spécifiques peuvent nécessiter des configurations supplémentaires ou ne pas être disponibles du tout, ce qui pourrait limiter les possibilités de personnalisation et de déploiement pour certains cas d'utilisation.

>- **Debian**
Debian est une distribution Linux stable et largement utilisée, offrant une vaste sélection de logiciels et une communauté active de support et de développement. Bien qu'il soit plus lourd qu'Alpine, Debian offre une compatibilité matérielle plus large et une disponibilité étendue de logiciels, ce qui en fait une solution de secours fiable en cas de besoins spécifiques ou de limitations rencontrées avec Alpine.

##### 2.2) Outils
La majeure partie des outils seront des outils existants, il faudra cependant faire un grand tri sur les outils afin de savoir lequel convient le mieux dans quel environnement et dans quel but.

Chaque "set" d'outil aura un but associé, on peut en imaginer un pour les attaques WEB, le cassage de mot de passes, l'analyse réseau...
Chacun de ces "set" à besoin d'outils différents, et même si certains ont un besoin qui peut être commun, il est possible qu'un outil soit plus approprié qu'un autre dans le contexte du set, que ce soit par des mécaniques avec d'autres outils, ou certaines fonctionnalitées plus avancées disponible uniquement sur certains outils.

Une liste des "sets" ainsi que leur contenu sera fourni dans la documentation.

##### 2.3) Hardening

Une partie hardening est aussi prévue afin de garantir la sécurité et l'intégrité de la machine.
La base de ce hardening se focalisera sur les recommendations de l'ANSSI sur les systèmes GNU/Linux. Cependant comme ce guide se concentre sur les bases du système, il est possible d'avoir quelques retouches à faire dépendamment de la nécessité de chaque outils.
On pourra aussi rajouter le chiffrement du disque par défaut lors de l'installation pour rajouter une couche sur la partie physique.


#### 3) Configuration matérielle minimale requise pour la solution

La détermination de la configuration matérielle minimale requise pour la distribution Linux dédiée aux tests de pénétration dépend en grande partie de la base choisie, que ce soit Alpine Linux ou Debian, ainsi que des outils de pentest inclus. À ce stade, il n'est pas encore possible de définir précisément les spécifications matérielles minimales, mais nous pouvons proposer quelques idées générales en tenant compte des caractéristiques de chaque base et des exigences des outils de pentest :

- **Alpine Linux** :
  Étant donné la légèreté et l'efficacité d'Alpine Linux, la configuration matérielle minimale pourrait être relativement modeste. Cependant, la présence d'outils de pentest peut nécessiter des ressources supplémentaires. Une configuration matérielle de base pourrait inclure :
  - Processeur : Processeur x86_64 (64 bits) ou ARM, avec une fréquence d'horloge minimale de 1 GHz.
  - Mémoire vive (RAM) : 1 Go de RAM pour une utilisation de base, 2 Go ou plus recommandé pour des performances optimales en tenant compte de l'exécution simultanée d'outils de pentest.
  - Espace de stockage : 10 Go d'espace disque disponible pour l'installation du système d'exploitation, des outils de pentest et pour le stockage des données et des rapports de test.

- **Debian** :
  Debian étant une distribution Linux plus complète, la configuration matérielle minimale pourrait être légèrement plus élevée que celle d'Alpine Linux, en particulier en tenant compte de la nécessité d'exécuter plusieurs outils de pentest. Une configuration matérielle de base pourrait inclure :
  - Processeur : Processeur x86_64 (64 bits) recommandé, avec une fréquence d'horloge minimale de 1,5 GHz.
  - Mémoire vive (RAM) : 2 Go de RAM pour une utilisation de base, 4 Go ou plus recommandé pour des performances optimales en tenant compte de l'exécution simultanée d'outils de pentest.
  - Espace de stockage : 20 Go d'espace disque disponible pour l'installation du système d'exploitation, des outils de pentest et pour le stockage des données et des rapports de test.

>**Ces spécifications sont fournies à titre indicatif** et peuvent être ajustées une fois que la base de la distribution Linux sera définitivement choisie et que des tests de performance supplémentaires auront été effectués.

#### 4) Conception et design

Pour l'interface utilisateur de la distribution Linux dédiée aux tests de pénétration, nous utiliserons XFCE comme base. XFCE est un environnement de bureau léger, rapide et personnalisable, ce qui le rend idéal pour les environnements de test où les performances et la flexibilité sont essentielles.

##### Rework de l'interface utilisateur :

Bien que nous utilisions XFCE comme base, nous prévoyons de procéder à une refonte complète de l'interface utilisateur pour répondre aux besoins spécifiques des professionnels de la sécurité informatique. Cette refonte incluera une nouvelle disposition des menus, une organisation optimisée des outils de pentest et une interface plus conviviale pour améliorer l'expérience utilisateur globale.


#### 5) Livrables attendus :

- Une distribution Linux entièrement configurée et prête à être déployée sur les systèmes cibles des professionnels de la sécurité informatique. La distribution sera pré-installée avec l'ensemble d'outils de pentest intégrés et configurés pour une utilisation immédiate. Elle sera disponible sous forme d'image ISO, prête à être gravée sur un support de stockage ou à être utilisée dans un environnement de machine virtuelle.

- Une documentation détaillée sera fournie pour guider les utilisateurs dans l'installation, la configuration et l'utilisation de la distribution Linux dédiée aux tests de pénétration. Cette documentation incluera :
  - Des instructions d'installation pas à pas, couvrant les différentes options de déploiement, y compris l'installation sur un système physique ou dans une machine virtuelle.
  - Des guides d'utilisation pour chaque outil de pentest inclus, décrivant leurs fonctionnalités, leurs options de configuration et leurs cas d'utilisation recommandés.
  - Des recommandations de bonnes pratiques en matière de tests de pénétration et de sécurité informatique, visant à aider les utilisateurs à maximiser l'efficacité de leurs évaluations de sécurité.
