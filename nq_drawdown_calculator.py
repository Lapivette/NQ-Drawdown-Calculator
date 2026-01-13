"""
Script de calcul du Drawdown Maximum pour les trades NQ
Auteur: Automatisation trading
Date: 2026-01-12
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

class NQDrawdownCalculator:
    """
    Classe pour calculer le drawdown maximum de chaque trade NQ
    """
    
    def __init__(self, orders_file, market_data_file):
        """
        Initialise le calculateur avec les fichiers CSV
        
        Args:
            orders_file (str): Chemin vers le fichier CSV des ordres
            market_data_file (str): Chemin vers le fichier CSV des données de marché
        """
        self.orders_file = orders_file
        self.market_data_file = market_data_file
        self.trades = []
        self.results = []
        
    def load_orders(self):
        """
        Charge et parse le fichier des ordres exécutés
        """
        print("📂 Chargement du fichier des ordres...")
        
        # Lire le fichier CSV
        # Le fichier a une structure spéciale avec "Completed Orders" comme en-tête
        df = pd.read_csv(self.orders_file, skiprows=5)  # Skip les premières lignes jusqu'aux ordres complétés
        
        # Nettoyer les données vides
        df = df.dropna(subset=['Account'])
        
        # Convertir les colonnes de date en datetime
        df['Create Time'] = pd.to_datetime(df['Create Time (RST)'])
        df['Update Time'] = pd.to_datetime(df['Update Time (RST)'])
        
        # Convertir les prix en float
        df['Avg Fill Price'] = df['Avg Fill Price'].astype(float)
        df['Qty To Fill'] = df['Qty To Fill'].astype(int)
        
        # Trier par date de création
        df = df.sort_values('Create Time').reset_index(drop=True)
        
        print(f"✅ {len(df)} ordres chargés")
        
        return df
    
    def identify_trades(self, orders_df):
        """
        Identifie les paires d'ordres qui forment un trade complet (entrée + sortie)
        Hypothèse: 1 trade à la fois, ordre chronologique, full in/out
        
        Args:
            orders_df (DataFrame): DataFrame des ordres
            
        Returns:
            list: Liste de dictionnaires contenant les informations de chaque trade
        """
        print("🔍 Identification des trades complets...")
        
        trades = []
        i = 0
        
        while i < len(orders_df) - 1:
            current_order = orders_df.iloc[i]
            next_order = orders_df.iloc[i + 1]
            
            # Déterminer quel ordre est venu en premier chronologiquement
            # On utilise Create Time pour l'ordre réel d'exécution
            if current_order['Create Time'] < next_order['Create Time']:
                first_order = current_order
                second_order = next_order
            else:
                first_order = next_order
                second_order = current_order
            
            # Vérifier si c'est une paire Buy/Sell (trade long)
            if first_order['Buy/Sell'] == 'B' and second_order['Buy/Sell'] == 'S':
                trade = {
                    'trade_number': len(trades) + 1,
                    'direction': 'LONG',
                    'entry_time': first_order['Create Time'],
                    'entry_price': first_order['Avg Fill Price'],
                    'exit_time': second_order['Update Time'],
                    'exit_price': second_order['Avg Fill Price'],
                    'quantity': first_order['Qty To Fill'],
                    'profit_loss': (second_order['Avg Fill Price'] - first_order['Avg Fill Price']) * first_order['Qty To Fill']
                }
                trades.append(trade)
                i += 2  # Passer à la paire suivante
                
            # Vérifier si c'est une paire Sell/Buy (trade short)
            elif first_order['Buy/Sell'] == 'S' and second_order['Buy/Sell'] == 'B':
                trade = {
                    'trade_number': len(trades) + 1,
                    'direction': 'SHORT',
                    'entry_time': first_order['Create Time'],
                    'entry_price': first_order['Avg Fill Price'],
                    'exit_time': second_order['Update Time'],
                    'exit_price': second_order['Avg Fill Price'],
                    'quantity': first_order['Qty To Fill'],
                    'profit_loss': (first_order['Avg Fill Price'] - second_order['Avg Fill Price']) * first_order['Qty To Fill']
                }
                trades.append(trade)
                i += 2  # Passer à la paire suivante
            else:
                i += 1
        
        print(f"✅ {len(trades)} trades identifiés")
        
        return trades
    
    def load_market_data(self):
        """
        Charge les données de marché (tick-by-tick OU bougies OHLC)
        Détecte automatiquement le format du fichier
        """
        print("📊 Chargement des données de marché NQ...")
        
        # Lire le fichier CSV
        df = pd.read_csv(self.market_data_file)
        
        # Détecter le format du fichier
        columns = df.columns.tolist()
        
        # Format 1 : Bougies OHLC (nouveau format depuis Chart export)
        if 'Bar Ending Time' in columns or 'Series.Low' in columns:
            print("   Format détecté : Bougies OHLC (1 seconde)")
            
            # Renommer les colonnes si nécessaire
            if 'Bar Ending Time' in columns:
                df.rename(columns={'Bar Ending Time': 'Timestamp'}, inplace=True)
            
            # Convertir le timestamp
            # Essayer d'abord le format européen DD/MM/YYYY (Rithmic en Europe)
            # puis le format américain MM/DD/YYYY en fallback
            try:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d/%m/%Y %H:%M:%S')
                print("   Format de date : DD/MM/YYYY (européen)")
            except:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%m/%d/%Y %H:%M:%S')
                print("   Format de date : MM/DD/YYYY (américain)")
            
            # On garde la colonne Low pour les trades LONG et High pour les SHORT
            df['Low'] = df['Series.Low'].astype(float)
            df['High'] = df['Series.High'].astype(float)
            
            # Trier par timestamp
            df = df.sort_values('Timestamp').reset_index(drop=True)
            
            print(f"✅ {len(df)} bougies chargées (de {df['Timestamp'].min()} à {df['Timestamp'].max()})")
            
            return df, 'ohlc'
        
        # Format 2 : Tick-by-tick (ancien format depuis Trade History)
        elif 'Rithmic Date/Time (RST)' in columns or 'Trade Price' in columns:
            print("   Format détecté : Tick-by-tick")
            
            # Convertir le timestamp (format ISO)
            df['Timestamp'] = pd.to_datetime(df['Rithmic Date/Time (RST)'])
            
            # Convertir le prix
            df['Trade Price'] = df['Trade Price'].astype(float)
            
            # Trier par timestamp
            df = df.sort_values('Timestamp').reset_index(drop=True)
            
            print(f"✅ {len(df)} ticks chargés (de {df['Timestamp'].min()} à {df['Timestamp'].max()})")
            
            return df, 'tick'
        
        else:
            print(f"❌ ERREUR : Format de fichier non reconnu!")
            print(f"   Colonnes détectées : {columns[:5]}...")
            raise ValueError("Format de données de marché non supporté")
    
    def calculate_drawdown(self, trade, market_data_df, data_format):
        """
        Calcule le drawdown maximum pour un trade donné
        
        Args:
            trade (dict): Informations du trade
            market_data_df (DataFrame): Données de marché
            data_format (str): 'tick' ou 'ohlc'
            
        Returns:
            dict: Statistiques du drawdown
        """
        # Filtrer les données de marché pour la période du trade
        mask = (market_data_df['Timestamp'] >= trade['entry_time']) & \
               (market_data_df['Timestamp'] <= trade['exit_time'])
        
        trade_data = market_data_df[mask].copy()
        
        if len(trade_data) == 0:
            print(f"⚠️  Aucune donnée de marché trouvée pour le trade {trade['trade_number']}")
            return {
                'max_drawdown_points': None,
                'max_drawdown_dollars': None,
                'max_drawdown_percent': None,
                'lowest_price': None,
                'lowest_price_time': None
            }
        
        # Calculer le drawdown selon le format et la direction du trade
        if trade['direction'] == 'LONG':
            # Pour un trade long, le drawdown est la différence entre le prix d'entrée et le plus bas
            
            if data_format == 'ohlc':
                # Format OHLC : on prend le Low de toutes les bougies
                lowest_price = trade_data['Low'].min()
                lowest_price_time = trade_data[trade_data['Low'] == lowest_price]['Timestamp'].iloc[0]
            else:
                # Format tick : on prend le prix le plus bas
                lowest_price = trade_data['Trade Price'].min()
                lowest_price_time = trade_data[trade_data['Trade Price'] == lowest_price]['Timestamp'].iloc[0]
            
            # Drawdown en points
            drawdown_points = trade['entry_price'] - lowest_price
            
        else:  # SHORT
            # Pour un trade short, le drawdown est la différence entre le plus haut et le prix d'entrée
            
            if data_format == 'ohlc':
                # Format OHLC : on prend le High de toutes les bougies
                highest_price = trade_data['High'].max()
                lowest_price_time = trade_data[trade_data['High'] == highest_price]['Timestamp'].iloc[0]
                lowest_price = highest_price
            else:
                # Format tick : on prend le prix le plus haut
                highest_price = trade_data['Trade Price'].max()
                lowest_price_time = trade_data[trade_data['Trade Price'] == highest_price]['Timestamp'].iloc[0]
                lowest_price = highest_price
            
            # Drawdown en points (négatif car c'est un short)
            drawdown_points = highest_price - trade['entry_price']
        
        # Calculer le drawdown en dollars (1 point NQ = $20)
        drawdown_dollars = drawdown_points * 20 * trade['quantity']
        
        # Calculer le drawdown en pourcentage du prix d'entrée
        drawdown_percent = (drawdown_points / trade['entry_price']) * 100
        
        return {
            'max_drawdown_points': drawdown_points,
            'max_drawdown_dollars': drawdown_dollars,
            'max_drawdown_percent': drawdown_percent,
            'lowest_price': lowest_price,
            'lowest_price_time': lowest_price_time
        }
    
    def process_all_trades(self):
        """
        Traite tous les trades et calcule les drawdowns
        """
        print("\n" + "="*60)
        print("🚀 DÉBUT DU CALCUL DES DRAWDOWNS")
        print("="*60 + "\n")
        
        # Charger les ordres
        orders_df = self.load_orders()
        
        # Identifier les trades
        self.trades = self.identify_trades(orders_df)
        
        # Charger les données de marché
        market_data_df, data_format = self.load_market_data()
        
        # Calculer le drawdown pour chaque trade
        print(f"\n💹 Calcul des drawdowns pour {len(self.trades)} trades...")
        
        for i, trade in enumerate(self.trades, 1):
            print(f"\n📈 Trade {i}/{len(self.trades)}:")
            print(f"   Direction: {trade['direction']}")
            print(f"   Entrée: {trade['entry_price']} @ {trade['entry_time']}")
            print(f"   Sortie: {trade['exit_price']} @ {trade['exit_time']}")
            print(f"   P&L: {trade['profit_loss']:.2f} points")
            
            # Calculer le drawdown
            dd_stats = self.calculate_drawdown(trade, market_data_df, data_format)
            
            # Ajouter les stats au trade
            trade.update(dd_stats)
            
            if dd_stats['max_drawdown_points'] is not None:
                print(f"   ⬇️  Drawdown Max: {dd_stats['max_drawdown_points']:.2f} points")
                print(f"   💰 Drawdown $: ${dd_stats['max_drawdown_dollars']:.2f}")
                print(f"   📊 Drawdown %: {dd_stats['max_drawdown_percent']:.3f}%")
                print(f"   🎯 Prix extrême: {dd_stats['lowest_price']} @ {dd_stats['lowest_price_time']}")
            
            self.results.append(trade)
        
        print("\n" + "="*60)
        print("✅ CALCUL TERMINÉ")
        print("="*60 + "\n")
    
    def save_results(self, output_file=None):
        """
        Sauvegarde les résultats dans un fichier CSV dans le dossier Rapports
        Le fichier est automatiquement nommé avec la date si non spécifié
        
        Args:
            output_file (str): Nom du fichier de sortie (optionnel)
        """
        # Créer le dossier Rapports s'il n'existe pas
        reports_dir = 'Rapports'
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            print(f"📁 Dossier '{reports_dir}' créé")
        
        # Si pas de nom de fichier spécifié, utiliser la date des trades
        if output_file is None and len(self.results) > 0:
            # Prendre la date du premier trade
            first_trade_date = self.results[0]['entry_time'].strftime('%Y-%m-%d')
            output_file = f"rapport_drawdown_{first_trade_date}.csv"
        elif output_file is None:
            # Fallback : date du jour
            from datetime import datetime
            output_file = f"rapport_drawdown_{datetime.now().strftime('%Y-%m-%d')}.csv"
        
        # Construire le chemin complet
        output_path = os.path.join(reports_dir, output_file)
        
        print(f"💾 Sauvegarde des résultats dans {output_path}...")
        
        # Convertir les résultats en DataFrame
        results_df = pd.DataFrame(self.results)
        
        # Sauvegarder en CSV
        results_df.to_csv(output_path, index=False)
        
        print(f"✅ Résultats sauvegardés avec succès!")
        print(f"📂 Emplacement : {os.path.abspath(output_path)}")
        
        return results_df
    
    def generate_summary(self):
        """
        Génère un résumé statistique des drawdowns
        """
        if not self.results:
            print("⚠️  Aucun résultat à analyser")
            return
        
        # Filtrer les trades avec drawdown calculé
        valid_trades = [t for t in self.results if t['max_drawdown_points'] is not None]
        
        if not valid_trades:
            print("⚠️  Aucun drawdown calculé")
            return
        
        # Calculer les statistiques
        dd_points = [t['max_drawdown_points'] for t in valid_trades]
        dd_dollars = [t['max_drawdown_dollars'] for t in valid_trades]
        dd_percent = [t['max_drawdown_percent'] for t in valid_trades]
        
        print("\n" + "="*60)
        print("📊 RÉSUMÉ STATISTIQUE DES DRAWDOWNS")
        print("="*60)
        print(f"\n📌 Nombre total de trades analysés: {len(valid_trades)}")
        print(f"\n🎯 DRAWDOWN EN POINTS:")
        print(f"   Moyen: {np.mean(dd_points):.2f} points")
        print(f"   Médian: {np.median(dd_points):.2f} points")
        print(f"   Maximum: {np.max(dd_points):.2f} points")
        print(f"   Minimum: {np.min(dd_points):.2f} points")
        print(f"   Écart-type: {np.std(dd_points):.2f} points")
        
        print(f"\n💰 DRAWDOWN EN DOLLARS:")
        print(f"   Moyen: ${np.mean(dd_dollars):.2f}")
        print(f"   Médian: ${np.median(dd_dollars):.2f}")
        print(f"   Maximum: ${np.max(dd_dollars):.2f}")
        print(f"   Minimum: ${np.min(dd_dollars):.2f}")
        
        print(f"\n📊 DRAWDOWN EN POURCENTAGE:")
        print(f"   Moyen: {np.mean(dd_percent):.3f}%")
        print(f"   Médian: {np.median(dd_percent):.3f}%")
        print(f"   Maximum: {np.max(dd_percent):.3f}%")
        print(f"   Minimum: {np.min(dd_percent):.3f}%")
        
        print("\n" + "="*60 + "\n")


def main():
    """
    Fonction principale
    """
    print("="*60)
    print("   CALCULATEUR DE DRAWDOWN NQ")
    print("   Propfirm Trading Analysis Tool")
    print("="*60 + "\n")
    
    print("💡 ASTUCE: Vous pouvez faire un drag & drop depuis votre explorateur de fichiers")
    print("   vers le terminal pour obtenir automatiquement le chemin du fichier.\n")
    
    # Demander le fichier des ordres
    print("📋 ÉTAPE 1/2 - Fichier des ordres exécutés")
    print("-" * 60)
    while True:
        orders_file = input("Entrez le chemin du fichier des ordres (ou drag & drop) : ").strip()
        
        # Nettoyer le chemin (enlever les guillemets si présents)
        orders_file = orders_file.strip('"').strip("'")
        
        # Vérifier que le fichier existe
        if os.path.exists(orders_file):
            print(f"✅ Fichier trouvé: {os.path.basename(orders_file)}\n")
            break
        else:
            print(f"❌ ERREUR: Le fichier '{orders_file}' n'existe pas!")
            print("   Vérifiez le chemin et réessayez.\n")
    
    # Demander le fichier des données de marché
    print("📊 ÉTAPE 2/2 - Fichier des données de marché NQ")
    print("-" * 60)
    while True:
        market_data_file = input("Entrez le chemin du fichier des données NQ (ou drag & drop) : ").strip()
        
        # Nettoyer le chemin (enlever les guillemets si présents)
        market_data_file = market_data_file.strip('"').strip("'")
        
        # Vérifier que le fichier existe
        if os.path.exists(market_data_file):
            print(f"✅ Fichier trouvé: {os.path.basename(market_data_file)}\n")
            break
        else:
            print(f"❌ ERREUR: Le fichier '{market_data_file}' n'existe pas!")
            print("   Vérifiez le chemin et réessayez.\n")
    
    # Demander le nom du fichier de sortie (optionnel)
    print("💾 Nom du fichier de sortie")
    print("-" * 60)
    print("ℹ️  Par défaut : rapport_drawdown_YYYY-MM-DD.csv")
    output_file = input("Nom personnalisé (Entrée pour automatique) : ").strip()
    if not output_file:
        output_file = None  # Utilisera le nom automatique avec la date
    else:
        # Ajouter l'extension .csv si oubliée
        if not output_file.endswith('.csv'):
            output_file += '.csv'
        print(f"✅ Fichier de sortie personnalisé: {output_file}\n")
    
    print("="*60)
    print("🚀 Lancement de l'analyse...")
    print("="*60 + "\n")
    
    # Créer le calculateur
    calculator = NQDrawdownCalculator(orders_file, market_data_file)
    
    # Traiter tous les trades
    calculator.process_all_trades()
    
    # Sauvegarder les résultats
    calculator.save_results(output_file)
    
    # Générer le résumé
    calculator.generate_summary()
    
    print("🎉 Processus terminé avec succès!")
    print(f"📁 Les résultats sont disponibles dans: {output_file}")
    print("\n💡 Vous pouvez ouvrir ce fichier dans Excel pour une analyse détaillée.")


if __name__ == "__main__":
    main()