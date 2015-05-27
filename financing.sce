clc
clear
// close 

nMonth_per_year = 12
// Caracteristiques Achat
logement_eur = 180000

notaire_eur = 14000
notaire_percent = notaire_eur/logement_eur


// Caracteristiques Financement
frais_garantie_eur = 2000
frais_bancaire_eur = 2000
frais_courtier_eur = 2000
frais_eur = 2000

apport_eur = 16000

// Pret Principal
pret_period_yr = 20
pret_period_month = pret_period_yr * nMonth_per_year;

taux_emprunt_percent = 0.034;
taux_emprunt_per_month_percent = taux_emprunt_percent / nMonth_per_year;
taux_assurance_percent = 0.002
taux_assurance_per_month_percent = taux_assurance_percent / nMonth_per_year

pret_eur = logement_eur + notaire_eur + frais_eur - apport_eur


// Aide

// PTZ+
ptz_eur = 0
ptz_period_yr = 16
ptz_period_month = ptz_period_yr * nMonth_per_year

// Pret 1% 
pret_1percent_eur = 25000
pret_1percent_percent = 0.0153

// pret_1percent_period_yr = pret_period_yr
// pret_1percent_per_month_eur = pret_1percent_eur / nMonth_per_year
// pret_1percent_per_month_eur = pret_1percent_per_month_eur * 

// taux_assurance_percent = 0.002
// taux_assurance_per_month_percent = taux_assurance_percent / nMonth_per_year



// Financing
financing_eur = logement_eur + notaire_eur + frais_eur - apport_eur
financing_1percent_eur = financing_eur - pret_1percent_eur
financing_Ptz_1percent_eur = financing_1percent_eur - ptz_eur



