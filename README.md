# NQ-Drawdown-Calculator
Objectif calculer ton drawdown moyen ! 
# 📊 NQ Drawdown Calculator

**Calculateur automatique de Drawdown Maximum pour traders NQ**

> Outil développé pour analyser vos trades Nasdaq (NQ) et calculer le drawdown maximum de chaque position. Idéal pour optimiser vos stops et améliorer votre gestion du risque.

---

## 🎯 Qu'est-ce que ce script fait ?

Ce script Python vous permet de :
- ✅ **Calculer automatiquement** le drawdown maximum de chaque trade
- ✅ **Analyser vos performances** sur plusieurs jours/semaines/mois
- ✅ **Optimiser vos stops** en connaissant vos DD moyens
- ✅ **Identifier vos meilleurs setups** (Long vs Short)
- ✅ **Suivre votre progression** dans le temps

**Résultat :** Améliorez votre win rate et réduisez vos pertes inutiles ! 🚀

---

## 📹 Tutoriel Vidéo

**[Voir la vidéo sur YouTube]** _(Ajoutez votre lien)_

---

## 🛠️ Installation (5 minutes)

### Étape 1 : Installer Python

**Windows :**
1. Téléchargez Python : https://www.python.org/downloads/
2. ⚠️ **IMPORTANT** : Cochez "Add Python to PATH" pendant l'installation
3. Cliquez sur "Install Now"

**Mac :**
```bash
brew install python3
```

**Linux :**
```bash
sudo apt-get install python3 python3-pip
```

### Étape 2 : Télécharger le script

**Option A : Téléchargement direct**
1. Cliquez sur le bouton vert "Code"
2. Sélectionnez "Download ZIP"
3. Décompressez le fichier

**Option B : Git (si vous l'avez)**
```bash
git clone https://github.com/VOTRE-NOM/NQ-Drawdown-Calculator.git
cd NQ-Drawdown-Calculator
```

### Étape 3 : Installer les dépendances

Ouvrez un terminal (CMD sur Windows) dans le dossier du script et tapez :

```bash
pip install -r requirements.txt
```

Ou manuellement :
```bash
pip install pandas numpy
```

**C'est tout ! Vous êtes prêt ! 🎉**

---

## 🚀 Utilisation Quotidienne

### 1️⃣ Après votre session de trading

**A. Exportez vos données depuis Rithmic :**
- Export des ordres exécutés → CSV
- Export du chart NQ (1 seconde) → CSV

**B. Lancez le calculateur :**
- Windows : Double-clic sur `lancer_calculateur.bat`
- Mac/Linux : Double-clic sur `lancer_calculateur.sh`

**C. Drag & Drop :**
- Glissez votre fichier d'ordres dans le terminal
- Glissez votre fichier de market data dans le terminal
- Appuyez sur Entrée

**D. Résultat :**
Un rapport est automatiquement créé dans `/Rapports/`

**Temps total : 2 minutes chrono !** ⏱️

---

### 2️⃣ Analyse hebdomadaire

Pour voir vos statistiques sur plusieurs jours :
- Double-clic sur `lancer_analyse_globale.bat` (Windows)
- Double-clic sur `lancer_analyse_globale.sh` (Mac/Linux)

Le script regroupe automatiquement tous vos rapports et affiche :
- Drawdown moyen
- Statistiques Long vs Short
- Top 5 meilleurs/pires trades
- Évolution dans le temps

---

## 📁 Structure des Fichiers

```
NQ-Drawdown-Calculator/
│
├── 📄 nq_drawdown_calculator.py      Script principal
├── 📄 analyse_globale.py              Analyse multi-jours
├── 📄 requirements.txt                Dépendances Python
│
├── 🚀 lancer_calculateur.bat          Lanceur Windows
├── 🚀 lancer_calculateur.sh           Lanceur Mac/Linux
├── 🚀 lancer_analyse_globale.bat      Lanceur analyse Windows
├── 🚀 lancer_analyse_globale.sh       Lanceur analyse Mac/Linux
│
├── 📖 README.md                       Ce fichier
├── 📖 GUIDE_UTILISATION.md            Guide détaillé
├── 📖 GUIDE_DRAG_DROP.md              Guide drag & drop
├── 📖 GUIDE_ANALYSE_GLOBALE.md        Guide analyse
│
└── 📁 Rapports/                       Rapports générés automatiquement
    ├── rapport_drawdown_2026-01-12.csv
    ├── rapport_drawdown_2026-01-13.csv
    └── rapport_consolide.csv
```

---

## 💡 Exemple de Résultat

```
============================================================
📊 RÉSUMÉ STATISTIQUE DES DRAWDOWNS
============================================================

📌 Nombre total de trades analysés: 15

🎯 DRAWDOWN EN POINTS:
   Moyen: 8.5 points
   Médian: 7.2 points
   Maximum: 15.3 points
   Minimum: 2.1 points

💰 DRAWDOWN EN DOLLARS:
   Moyen: $680
   Médian: $576

📊 Win Rate: 73% (11/15)
```

**Conclusion :** Avec un DD moyen de 8.5 points, vous devriez placer vos stops à minimum 10-12 points !

---

## ❓ FAQ (Foire Aux Questions)

### Le script fonctionne avec quel broker ?
✅ Tout broker qui utilise **Rithmic** (la plupart des prop firms US)  
✅ Export CSV depuis R Trader Pro  
✅ Export CSV depuis MotiveWave

### Quel format de fichier est nécessaire ?
Le script détecte automatiquement :
- Format tick-by-tick (Trade History)
- Format OHLC/bougies 1 seconde (Chart export)

### Ça fonctionne sur Mac ?
✅ Oui ! Python fonctionne sur Windows, Mac et Linux

### C'est gratuit ?
✅ Oui, 100% gratuit et open source

### Puis-je modifier le script ?
✅ Oui ! Le code est open source, modifiez-le comme vous voulez

### Combien de trades puis-je analyser ?
✅ Illimité ! Le script peut analyser des milliers de trades

### Les données sont-elles sécurisées ?
✅ Oui ! Tout reste sur VOTRE ordinateur. Aucune donnée n'est envoyée en ligne.

---

## 🐛 Problèmes Courants

### "Python n'est pas reconnu"
➡️ Réinstallez Python en cochant **"Add Python to PATH"**

### "Module pandas not found"
➡️ Installez les dépendances : `pip install pandas numpy`

### "Aucune donnée trouvée"
➡️ Vérifiez que les dates de vos fichiers correspondent (ordres + market data de la même journée)

### Le drag & drop ne marche pas
➡️ Copiez-collez le chemin du fichier à la place

---

## 🤝 Support & Communauté

- 💬 **Discord** : (https://discord.gg/SHuwUJpcMr)
- 📹 **YouTube** : (https://www.youtube.com/@LapivetteTrade)
- 🐛 **Bugs** : Ouvrez une "Issue" sur GitHub
- ⭐ **N'oubliez pas de mettre une étoile !** ⭐

---

## 🙏 Crédits

Créé par [Lapivette / LapivetteTrade]  
Développé pour la communauté des traders NQ

**Si ce script vous aide, pensez à :**
- ⭐ Mettre une étoile sur GitHub
- 👍 Liker la vidéo YouTube
- 💬 Partager avec d'autres traders

**Suggestions ? Ouvrez une Issue !**

---

**Bon trading et gestion du risque intelligente ! 📊💪**
