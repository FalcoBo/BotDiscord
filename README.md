# BotDiscord

**fonctionnalitées du bot**
-   Il peut gérer la modération d'un serveur seulement pour les nouveaux membres. Dès leur arrivé ils peuvent seulement voir un channel textuel "rôles" où ils répondent à un message par un émojis qui leurs permette d'obtenir le rôles "Nouveau" et ainsi pouvoir accéder aux autres salons.

-   Il permet de jouer une vidéo seulement si la personne qui utilise la commande est dans un channel vocal.

-   Un système d'historique des commandes est géré par le bot. Si le bot est dans plusieurs serveurs différents il stockera les historiques par serveurs et par membres, l'historique des commandes ne sera pas le même d'un serveur à un autre. Toutes les données sont stockées dans un fichier data.json. Il y a aussi plusieurs commandes pour gérer les historiques.

-   Certaines fonctionnalitées seront disponibles seulement pour certains rôles par exemple l'effacement de tout les messages dans un channel qui est utilisables seulement par les admins etc ..

**Commandes**

Si un utilisateur tente de rentrer une commande qui n'existe pas alors un message d'erreur s'affichera et proposera d'utiliser la commande ci-dessous. 

-   !commands : permet d'afficher toutes les commandes utilisables par les Nouveaux utilisateurs ou si elle est utilisée par un admin elle affichera les commandes pour les admins et pour tout les autres rôles.

-   !txt et !hello : sont deux commandes de test pour l'historique qui affichent "Hello Wordl !" et "Hello".

-   !clear_channel : Une commande utilisable seulement par les Admin du serveur (actuellemnt le rôle définis est "Master") qui permet d'effacer maximum les 1500 des messages d'un channel.

-   !history :Permet d'afficher l'historique des commandes par utilisateurs par serveur (ne s'enregistre pas elle même dans l'hisorique).

-   !first : Montre la première commande utilisé.

-   !last : Montrre la dernière commande utilisé.

-   !clear_history : Efface l'entièreté de l'historique de l'utilisateur dans le serveru où elle a été utilisée.

-   !play : Permet de jouer l'audio d'une vidéo youtube si l'utilisateur est dans un channel vocal.

-   !stop : Déconnect le bot musique du channel vocal.

-   !ban : Peux être utilisée seulement par les membres détenant le rôle "Master" et permet de bannir un utilisateur. (non fonctionnel).

**fonctionnalitées commencées mais pas finis**

-   Le chatbot

-   Le hash de l'historique des commandes