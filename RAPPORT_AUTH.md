# Rapport : Différence entre Authentification et Autorisation

Dans le cadre du Workshop Django (Partie Authentification & Protection des vues - TransConnect) :

### 1. Authentification (« Qui es-tu ? »)
- **Définition** : L'authentification vérifie et valide l'identité de l'utilisateur accédant au système (via ses identifiants : username/mot de passe).
- **Implémentation** : Elle est assurée par le système de session de Django (`django.contrib.auth`), les vues `LoginView`/`LogoutView`, et le mixin `LoginRequiredMixin` (ou décorateur `@login_required`).
- **Limitation constatée en Section VII** : `LoginRequiredMixin` vérifie uniquement si `request.user.is_authenticated` est vrai. Cependant, être connecté ne dit rien sur les droits d'accès à une ressource spécifique.

### 2. Autorisation (« À quoi as-tu le droit ? »)
- **Définition** : L'autorisation détermine si un utilisateur authentifié possède la permission d'exécuter une action donnée sur une ressource précise (consulter, modifier, supprimer).
- **Problème constaté en Section VII.1** : Sans contrôle d'autorisation au niveau de l'objet, un transporteur A connecté pouvait accéder directement à `/vehicules/7/modifier/` ou `/vehicules/7/supprimer/` et altérer le véhicule appartenant au transporteur B, car `UpdateView` et `DeleteView` chargeaient l'objet via `Vehicule.objects.all()`.
- **Solution mise en place (Section VII.2 & IX)** :
  1. **Contrôle par rôle / type d'acteur** : Les mixins `TransporteurRequisMixin` et `ChargeurRequisMixin` (`UserPassesTestMixin`) interdisent l'accès aux vues inappropriées (ex: un chargeur ne peut pas ajouter un véhicule ou proposer une offre).
  2. **Contrôle d'appartenance (Scoping)** : Le mixin `VehiculesDeMonEntrepriseMixin` (et `ExpeditionsDeMonEntrepriseMixin`) surcharge `get_queryset()` pour restreindre la sélection aux objets appartenant à `request.user.entreprise`. Si l'utilisateur tente d'accéder à l'objet d'un autre utilisateur, Django renvoie une erreur **HTTP 404** (ressource introuvable pour ce client), masquant ainsi l'existence même de la ressource.
