from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from EntrepriseApp.models import Utilisateur, Entreprise
from VehiculesApp.models import Vehicule
from ExpeditionsApp.models import Expedition
from OffresApp.models import Offre


class Command(BaseCommand):
    help = "Peuple la base de données TransConnect avec des données de démonstration réalistes."

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Supprime les offres, expéditions, véhicules et entreprises existantes avant le peuplement',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING("Nettoyage des données existantes..."))
            Offre.objects.all().delete()
            Expedition.objects.all().delete()
            Vehicule.objects.all().delete()
            Entreprise.objects.all().delete()
            # On conserve les superutilisateurs et staff
            Utilisateur.objects.filter(is_superuser=False, is_staff=False).delete()
            self.stdout.write(self.style.SUCCESS("Données nettoyées avec succès."))

        self.stdout.write("Création des données de démonstration...")

        # --------------------------------------------------------------------
        # 1. UTILISATEURS (Gérants)
        # --------------------------------------------------------------------
        # Règles : email @gmail.com, telephone max 8 car., role dans ('chargeur', 'transporteur')
        users_data = [
            {
                'username': 'ahmed_chargeur',
                'email': 'ahmed.benali@gmail.com',
                'telephone': '21111111',
                'role': 'chargeur',
                'first_name': 'Ahmed',
                'last_name': 'Ben Ali',
            },
            {
                'username': 'karim_chargeur',
                'email': 'karim.charge@gmail.com',
                'telephone': '22222222',
                'role': 'chargeur',
                'first_name': 'Karim',
                'last_name': 'Trabelsi',
            },
            {
                'username': 'sami_transport',
                'email': 'sami.express@gmail.com',
                'telephone': '23333333',
                'role': 'transporteur',
                'first_name': 'Sami',
                'last_name': 'Mansour',
            },
            {
                'username': 'fethi_fret',
                'email': 'fethi.logistics@gmail.com',
                'telephone': '24444444',
                'role': 'transporteur',
                'first_name': 'Fethi',
                'last_name': 'Jlassi',
            },
        ]

        users = {}
        for u_data in users_data:
            user = Utilisateur.objects.filter(username=u_data['username']).first()
            if not user:
                user = Utilisateur(
                    username=u_data['username'],
                    email=u_data['email'],
                    telephone=u_data['telephone'],
                    role=u_data['role'],
                    first_name=u_data['first_name'],
                    last_name=u_data['last_name'],
                )
                user.set_password('pass1234')
                user.save()
                self.stdout.write(f"  + Utilisateur créé : {user.username} ({user.role})")
            users[u_data['username']] = user

        # --------------------------------------------------------------------
        # 2. ENTREPRISES
        # --------------------------------------------------------------------
        # Règles : matricule regex ^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$
        # Adresse >= 20 car., gérant OneToOne
        entreprises_data = [
            {
                'key': 'chargeur_1',
                'raison_social': 'Société Agro-Alimentaire Express',
                'matricule_fiscal': '1111111-A-A-M-001',
                'type_entreprise': 'chargeur',
                'adresse': 'Zone Industrielle Charguia II, 2035 Tunis, Tunisie',
                'gerant': users['ahmed_chargeur'],
            },
            {
                'key': 'chargeur_2',
                'raison_social': 'Textile & Industrie Méditerranée',
                'matricule_fiscal': '2222222-B-B-M-002',
                'type_entreprise': 'chargeur',
                'adresse': 'Route de Gabès Km 3.5, 3052 Sfax, Tunisie',
                'gerant': users['karim_chargeur'],
            },
            {
                'key': 'transporteur_1',
                'raison_social': 'Mansour Transport & Logistique',
                'matricule_fiscal': '3333333-C-A-M-003',
                'type_entreprise': 'transporteur',
                'adresse': 'Avenue Habib Bourguiba, 4000 Sousse, Tunisie',
                'gerant': users['sami_transport'],
            },
            {
                'key': 'transporteur_2',
                'raison_social': 'Trans-Tunisie Fret Rapide',
                'matricule_fiscal': '4444444-D-B-M-004',
                'type_entreprise': 'transporteur',
                'adresse': 'Zone Portuaire de Rades, 2040 Ben Arous, Tunisie',
                'gerant': users['fethi_fret'],
            },
        ]

        entreprises = {}
        for e_data in entreprises_data:
            ent = Entreprise.objects.filter(matricule_fiscal=e_data['matricule_fiscal']).first()
            if not ent:
                # Vérifier si le gérant n'a pas déjà une entreprise
                if hasattr(e_data['gerant'], 'entreprise'):
                    ent = e_data['gerant'].entreprise
                else:
                    ent = Entreprise.objects.create(
                        raison_social=e_data['raison_social'],
                        matricule_fiscal=e_data['matricule_fiscal'],
                        type_entreprise=e_data['type_entreprise'],
                        adresse=e_data['adresse'],
                        gerant=e_data['gerant'],
                    )
                    self.stdout.write(f"  + Entreprise créée : {ent.raison_social} ({ent.type_entreprise})")
            entreprises[e_data['key']] = ent

        # --------------------------------------------------------------------
        # 3. VÉHICULES
        # --------------------------------------------------------------------
        # Règles : immmatriculation max 8 car. unique, type_vehicule dans les choix,
        # entreprise doit être transporteur, capacite_kg >= 1
        vehicules_data = [
            {
                'immmatriculation': '201TN101',
                'type_vehicule': 'camionette',
                'capacite_kg': 1400,
                'disponible': True,
                'entreprise': entreprises['transporteur_1'],
            },
            {
                'immmatriculation': '202TN202',
                'type_vehicule': 'fourgon',
                'capacite_kg': 3200,
                'disponible': True,
                'entreprise': entreprises['transporteur_1'],
            },
            {
                'immmatriculation': '203TN303',
                'type_vehicule': 'camion',
                'capacite_kg': 16000,
                'disponible': True,
                'entreprise': entreprises['transporteur_1'],
            },
            {
                'immmatriculation': '204TN404',
                'type_vehicule': 'semi-remorque',
                'capacite_kg': 25000,
                'disponible': True,
                'entreprise': entreprises['transporteur_2'],
            },
            {
                'immmatriculation': '205TN505',
                'type_vehicule': 'fourgon',
                'capacite_kg': 3000,
                'disponible': True,
                'entreprise': entreprises['transporteur_2'],
            },
        ]

        vehicules = []
        for v_data in vehicules_data:
            veh = Vehicule.objects.filter(immmatriculation=v_data['immmatriculation']).first()
            if not veh:
                veh = Vehicule.objects.create(
                    immmatriculation=v_data['immmatriculation'],
                    type_vehicule=v_data['type_vehicule'],
                    capacite_kg=v_data['capacite_kg'],
                    disponible=v_data['disponible'],
                    entreprise=v_data['entreprise'],
                )
                self.stdout.write(f"  + Véhicule créé : {veh.immmatriculation} ({veh.type_vehicule})")
            vehicules.append(veh)

        # --------------------------------------------------------------------
        # 4. EXPÉDITIONS
        # --------------------------------------------------------------------
        # Règles : statut='publiee ', entreprise type='chargeur', poids_kg >= 1
        now = timezone.now()
        expeditions_data = [
            {
                'ville_depart': 'Tunis',
                'ville_arrivee': 'Sousse',
                'date_souhaite': now + timedelta(days=3),
                'poids_kg': 1200,
                'statut': 'publiee ',
                'entreprise': entreprises['chargeur_1'],
            },
            {
                'ville_depart': 'Sfax',
                'ville_arrivee': 'Bizerte',
                'date_souhaite': now + timedelta(days=5),
                'poids_kg': 2800,
                'statut': 'publiee ',
                'entreprise': entreprises['chargeur_2'],
            },
            {
                'ville_depart': 'Nabeul',
                'ville_arrivee': 'Gabès',
                'date_souhaite': now + timedelta(days=7),
                'poids_kg': 14000,
                'statut': 'publiee ',
                'entreprise': entreprises['chargeur_1'],
            },
            {
                'ville_depart': 'Monastir',
                'ville_arrivee': 'Tunis',
                'date_souhaite': now + timedelta(days=2),
                'poids_kg': 800,
                'statut': 'publiee ',
                'entreprise': entreprises['chargeur_2'],
            },
        ]

        expeditions = []
        for ex_data in expeditions_data:
            existing = Expedition.objects.filter(
                ville_depart=ex_data['ville_depart'],
                ville_arrivee=ex_data['ville_arrivee'],
                entreprise=ex_data['entreprise'],
            ).first()
            if not existing:
                ex = Expedition.objects.create(
                    ville_depart=ex_data['ville_depart'],
                    ville_arrivee=ex_data['ville_arrivee'],
                    date_souhaite=ex_data['date_souhaite'],
                    poids_kg=ex_data['poids_kg'],
                    statut=ex_data['statut'],
                    entreprise=ex_data['entreprise'],
                )
                self.stdout.write(f"  + Expédition créée : {ex.reference} ({ex.ville_depart} -> {ex.ville_arrivee})")
                expeditions.append(ex)
            else:
                expeditions.append(existing)

        # --------------------------------------------------------------------
        # 5. OFFRES
        # --------------------------------------------------------------------
        # Règles : transporteur type='transporteur', véhicule appartient au transporteur,
        # expédition au statut 'publiee', pas deux offres proposées de la même entreprise sur la même expédition.
        if len(expeditions) >= 3 and len(vehicules) >= 5:
            # Offre 1 : Transporteur 1 propose pour Expédition 1 (1200 kg, camionette 1400 kg)
            ex1 = expeditions[0]
            if ex1.statut.strip() == 'publiee' and not Offre.objects.filter(expedition=ex1, transporteur=entreprises['transporteur_1']).exists():
                o1 = Offre.objects.create(
                    prix=Decimal('450.000'),
                    delai_jours=2,
                    statut='proposee',
                    expedition=ex1,
                    transporteur=entreprises['transporteur_1'],
                    vehicule=vehicules[0],  # 201TN101 camionette
                )
                self.stdout.write(f"  + Offre créée : #{o1.id} ({o1.prix} DT) sur {ex1.reference}")

            # Offre 2 : Transporteur 2 propose pour Expédition 1 (fourgon 3000 kg)
            if ex1.statut.strip() == 'publiee' and not Offre.objects.filter(expedition=ex1, transporteur=entreprises['transporteur_2']).exists():
                o2 = Offre.objects.create(
                    prix=Decimal('420.500'),
                    delai_jours=1,
                    statut='proposee',
                    expedition=ex1,
                    transporteur=entreprises['transporteur_2'],
                    vehicule=vehicules[4],  # 205TN505 fourgon
                )
                self.stdout.write(f"  + Offre créée : #{o2.id} ({o2.prix} DT) sur {ex1.reference}")

            # Offre 3 : Transporteur 1 propose pour Expédition 2 (2800 kg, fourgon 3200 kg)
            ex2 = expeditions[1]
            if ex2.statut.strip() == 'publiee' and not Offre.objects.filter(expedition=ex2, transporteur=entreprises['transporteur_1']).exists():
                o3 = Offre.objects.create(
                    prix=Decimal('890.000'),
                    delai_jours=3,
                    statut='proposee',
                    expedition=ex2,
                    transporteur=entreprises['transporteur_1'],
                    vehicule=vehicules[1],  # 202TN202 fourgon
                )
                self.stdout.write(f"  + Offre créée : #{o3.id} ({o3.prix} DT) sur {ex2.reference}")

            # Offre 4 : Transporteur 1 propose pour Expédition 3 (14000 kg, camion 16000 kg)
            ex3 = expeditions[2]
            if ex3.statut.strip() == 'publiee' and not Offre.objects.filter(expedition=ex3, transporteur=entreprises['transporteur_1']).exists():
                o4 = Offre.objects.create(
                    prix=Decimal('2300.000'),
                    delai_jours=4,
                    statut='proposee',
                    expedition=ex3,
                    transporteur=entreprises['transporteur_1'],
                    vehicule=vehicules[2],  # 203TN303 camion
                )
                self.stdout.write(f"  + Offre créée : #{o4.id} ({o4.prix} DT) sur {ex3.reference}")

        self.stdout.write(self.style.SUCCESS("\n[SUCCESS] Base de données peuplée avec succès !"))
