<!--
╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║   Copyright (c) 2020 https://prrvchr.github.io                                     ║
║                                                                                    ║
║   Permission is hereby granted, free of charge, to any person obtaining            ║
║   a copy of this software and associated documentation files (the "Software"),     ║
║   to deal in the Software without restriction, including without limitation        ║
║   the rights to use, copy, modify, merge, publish, distribute, sublicense,         ║
║   and/or sell copies of the Software, and to permit persons to whom the Software   ║
║   is furnished to do so, subject to the following conditions:                      ║
║                                                                                    ║
║   The above copyright notice and this permission notice shall be included in       ║
║   all copies or substantial portions of the Software.                              ║
║                                                                                    ║
║   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,                  ║
║   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES                  ║
║   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.        ║
║   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY             ║
║   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,             ║
║   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE       ║
║   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                    ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝
-->
# [![H2dbOOo logo][1]][2] Documentation

**This [document][3] in English.**

**L'utilisation de ce logiciel vous soumet à nos [Conditions d'utilisation][4].**

# version [1.1.2][5]

## Introduction:

**H2dbOOo** fait partie d'une [Suite][6] d'extensions [LibreOffice][7] ~~et/ou [OpenOffice][8]~~ permettant de vous offrir des services inovants dans ces suites bureautique.  

Cette extension vous permet d'utiliser la base de données [H2 Database][9] en mode intégré, rendant la base de donnée portable (un seul fichier odb).  
Elle permet de profiter des propriétés [ACID][10] de la base de données [H2 Database][11] sous jancente.

Etant un logiciel libre je vous encourage:
- A dupliquer son [code source][12].
- A apporter des modifications, des corrections, des améliorations.
- D'ouvrir un [dysfonctionnement][13] si nécessaire.

Bref, à participer au developpement de cette extension.  
Car c'est ensemble que nous pouvons rendre le Logiciel Libre plus intelligent.

___

## Prérequis:

L'extension H2dbOOo utilise l'extension jdbcDriverOOo pour fonctionner.  
Elle doit donc répondre aux [prérequis de l'extension jdbcDriverOOo][14].

**Depuis la version 1.1.0, seul LibreOffice 24.2.x ou supérieur est pris en charge.**  
S'il ne vous est pas possible d'utiliser une telle version, utilisez la version précédente de H2dbOOo. Mais dans ce cas, cette extension ne peut pas être installée avec l'extension [HyperSQLOOo][15], voir [bug #156471][16].  
De plus, il vous sera difficile de migrer les fichiers odb créés sous des versions inférieures de H2dbOOo. Je vous recommande d'utiliser LibreOffice 24.2.x minimum avec H2dbOOo 1.1.0 ou supérieur.

**Sous Linux et macOS les paquets Python** utilisés par l'extension, peuvent s'il sont déja installé provenir du système et donc, **peuvent ne pas être à jour**.  
Afin de s'assurer que vos paquets Python sont à jour il est recommandé d'utiliser l'option **Info système** dans les Options de l'extension accessible par:  
**Outils -> Options -> Pilotes Base -> Pilote SQLite intégré -> Voir journal -> Info système**  
Si des paquets obsolètes apparaissent, vous pouvez les mettre à jour avec la commande:  
`pip install --upgrade <package-name>`

___

## Installation:

Il semble important que le fichier n'ait pas été renommé lors de son téléchargement.  
Si nécessaire, renommez-le avant de l'installer.

- [![jdbcDriverOOo logo][17]][18] Installer l'extension **[jdbcDriverOOo.oxt][19]** [![Version][20]][19]

    Cette extension est nécessaire pour utiliser H2 Database avec toutes ses fonctionnalités.

- ![H2dbOOo logo][21] Installer l'extension **[H2dbOOo.oxt][22]** [![Version][23]][22]

Redémarrez LibreOffice après l'installation.  
**Attention, redémarrer LibreOffice peut ne pas suffire.**
- **Sous Windows** pour vous assurer que LibreOffice redémarre correctement, utilisez le Gestionnaire de tâche de Windows pour vérifier qu'aucun service LibreOffice n'est visible après l'arrêt de LibreOffice (et tuez-le si ç'est le cas).
- **Sous Linux ou macOS** vous pouvez également vous assurer que LibreOffice redémarre correctement, en le lançant depuis un terminal avec la commande `soffice` et en utilisant la combinaison de touches `Ctrl + C` si après l'arrêt de LibreOffice, le terminal n'est pas actif (pas d'invité de commande).

___

## Utilisation:

### Comment créer une nouvelle base de données:

Dans LibreOffice / OpenOffice aller à: Fichier -> Nouveau -> Base de données...:

![H2dbOOo screenshot 1][24]

A l'étape: Sélectionner une base de données:
- selectionner: Créer une nouvelle base de données
- Dans: Base de données intégrée: choisir: **Pilote H2 intégré**
- cliquer sur le bouton: Suivant

![H2dbOOo screenshot 2][25]

A l'étape: Enregistrer et continuer:
- ajuster les paramètres selon vos besoins...
- cliquer sur le bouton: Terminer

![H2dbOOo screenshot 3][26]

Maintenant à vous d'en profiter...

___

## Comment ça marche:

H2dbOOo est un service [com.sun.star.sdbc.Driver][27] UNO écrit en Python.  
Il s'agit d'une surcouche à l'extension [jdbcDriverOOo][18] permettant de stocker la base de données H2 dans un fichier odb (qui est, en fait, un fichier compressé).

Son fonctionnement est assez basique, à savoir:

- Lors d'une demande de connexion, plusieurs choses sont faites:
  - S'il n'existe pas déjà, un **sous-répertoire** avec le nom: `.` + `nom_du_fichier_odb` + `.lck` est créé à l'emplacement du fichier odb dans lequel tous les fichiers H2 sont extraits du répertoire **database** du fichier odb (décompression).
  - L'extension [jdbcDriverOOo][18] est utilisée pour obtenir l'interface [com.sun.star.sdbc.XConnection][28] à partir du chemin du **sous-répertoire** + `/H2`.
  - Si la connexion réussi, un [DocumentHandler][29] est ajouté en tant que [com.sun.star.util.XCloseListener][30] et [com.sun.star.document.XStorageChangeListener][31] au fichier odb.
  - Si la connexion échoue et que les fichiers ont été extraits lors de la phase 1, le **sous-répertoire** est supprimé.
- Lors de la fermeture ou du changement de nom (Enregistrer sous) du fichier odb, si la connexion a réussi, le [DocumentHandler][29] copie tous les fichiers présents dans le **sous-répertoire** dans le (nouveau) répertoire **database** du fichier odb (zip), puis supprime le **sous-répertoire**.

Le but principal de ce mode de fonctionnement est de profiter des caractéristiques ACID de la base de données sous-jacente en cas de fermeture anormale de LibreOffice.
En contre partie, la fonction: **fichier -> Sauvegarder** n'a **aucun effet sur la base de données sous jacente**. Seul la fermeture du fichier odb ou son enregistrement sous un nom different (Fichier -> Enregistrer sous) effectura la sauvegarde de la base de donnée dans le fichier odb.

___

## A été testé avec:

* LibreOffice 24.2.1.2 (x86_64)- Windows 10

* LibreOffice 24.2.1.2 - Lubuntu 22.04

* LibreOffice 24.8.0.3 (X86_64) - Windows 10(x64) - Python version 3.9.19 (sous Lubuntu 22.04 / VirtualBox 6.1.38)

Je vous encourage en cas de problème :confused:  
de créer un [dysfonctionnement][13]  
J'essaierai de le résoudre :smile:

___

## Historique:

### Ce qui a été fait pour la version 1.0.0:

- Implémentation d'un nouveau format dans les fichiers odb permettant de prendre en compte le nom du catalogue de la base de données sous-jacente.

### Ce qui a été fait pour la version 1.1.0:

- Cette version est basée sur la [correction #154989][32] disponible depuis LibreOffice 24.2.x. Elle peut donc fonctionner avec les autres extensions proposant des services de bases de données intégrées.
- Désormais, H2dbOOo nécessite LibreOffice 24.2.x minimum et se chargera pour l'url: `sdbc:embedded:h2`.

### Ce qui a été fait pour la version 1.1.1:

- Mise à jour du paquet [Python packaging][33] vers la version 24.1.
- Mise à jour du paquet [Python setuptools][34] vers la version 72.1.0.
- L'extension vous demandera d'installer l'extensions jdbcDriverOOo en version 1.4.2 minimum.

### Ce qui a été fait pour la version 1.1.2:

- Correction du [problème n°2][35] qui semble être une régression liée à la sortie de JaybirdOOo. Merci à TeddyBoomer de l'avoir signalé.
- Mise à jour du paquet [Python setuptools][34] vers la version 73.0.1.
- La journalisation accessible dans les options de l’extension s’affiche désormais correctement sous Windows.
- Les options de l'extension sont désormais accessibles via: **Outils -> Options... -> LibreOffice Base -> Pilote H2 intégré**
- Les modifications apportées aux options d'extension, qui nécessitent un redémarrage de LibreOffice, entraîneront l'affichage d'un message.
- Support de LibreOffice version 24.8.x.

### Que reste-t-il à faire pour la version 1.1.2:

- Ajouter de nouvelles langue pour l'internationalisation...

- Tout ce qui est bienvenu...

[1]: </img/h2db.svg#collapse>
[2]: <https://prrvchr.github.io/H2dbOOo/>
[3]: <https://prrvchr.github.io/H2dbOOo/>
[4]: <https://prrvchr.github.io/H2dbOOo/source/H2dbOOo/registration/TermsOfUse_fr>
[5]: <https://prrvchr.github.io/H2dbOOo/README_fr#historique>
[6]: <https://prrvchr.github.io/README_fr>
[7]: <https://fr.libreoffice.org/download/telecharger-libreoffice/>
[8]: <https://www.openoffice.org/fr/Telecharger/>
[9]: <https://github.com/h2database/h2database>
[10]: <https://en.wikipedia.org/wiki/ACID>
[11]: <https://www.h2database.com/html/features.html#logging_recovery>
[12]: <https://github.com/prrvchr/H2dbOOo/>
[13]: <https://github.com/prrvchr/H2dbOOo/issues/new>
[14]: <https://prrvchr.github.io/jdbcDriverOOo/README_fr#pr%C3%A9requis>
[15]: <https://prrvchr.github.io/HyperSQLOOo/README_fr#pr%C3%A9requis>
[16]: <https://bugs.documentfoundation.org/show_bug.cgi?id=156471>
[17]: <https://prrvchr.github.io/jdbcDriverOOo/img/jdbcDriverOOo.svg#middle>
[18]: <https://prrvchr.github.io/jdbcDriverOOo/README_fr>
[19]: <https://github.com/prrvchr/jdbcDriverOOo/releases/latest/download/jdbcDriverOOo.oxt>
[20]: <https://img.shields.io/github/v/tag/prrvchr/jdbcDriverOOo?label=latest#right>
[21]: <img/H2dbOOo.svg#middle>
[22]: <https://github.com/prrvchr/H2dbOOo/releases/latest/download/H2dbOOo.oxt>
[23]: <https://img.shields.io/github/downloads/prrvchr/H2dbOOo/latest/total?label=v1.1.2#right>
[24]: <img/H2dbOOo-1_fr.png>
[25]: <img/H2dbOOo-2_fr.png>
[26]: <img/H2dbOOo-3_fr.png>
[27]: <https://www.openoffice.org/api/docs/common/ref/com/sun/star/sdbc/Driver.html>
[28]: <https://www.openoffice.org/api/docs/common/ref/com/sun/star/sdbc/XConnection.html>
[29]: <https://github.com/prrvchr/H2dbOOo/blob/main/uno/lib/uno/embedded/documenthandler.py>
[30]: <https://www.openoffice.org/api/docs/common/ref/com/sun/star/util/XCloseListener.html>
[31]: <http://www.openoffice.org/api/docs/common/ref/com/sun/star/document/XStorageChangeListener.html>
[32]: <https://gerrit.libreoffice.org/c/core/+/154989>
[33]: <https://pypi.org/project/packaging/>
[34]: <https://pypi.org/project/setuptools/>
[35]: <https://github.com/prrvchr/HyperSQLOOo/issues/2>
