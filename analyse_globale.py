"""
Script d'analyse globale des drawdowns NQ
Regroupe tous les rapports du dossier Rapports et génère des statistiques globales
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import glob

class GlobalDrawdownAnalyzer:
    """
    Analyse tous les rapports de drawdown pour des statistiques globales
    """
    
    def __init__(self, reports_dir='Rapports'):
        """
        Initialise l'analyseur avec le dossier des rapports
        
        Args:
            reports_dir (str): Chemin vers le dossier contenant les rapports CSV
        """
        self.reports_dir = reports_dir
        self.all_trades = None
        
    def load_all_reports(self):
        """
        Charge tous les rapports CSV du dossier Rapports
        """
        print("="*60)
        print("📊 ANALYSE GLOBALE DES DRAWDOWNS")
        print("="*60 + "\n")
        
        print(f"📂 Recherche des rapports dans {self.reports_dir}/...")
        
        # Vérifier que le dossier existe
        if not os.path.exists(self.reports_dir):
            print(f"❌ ERREUR: Le dossier {self.reports_dir} n'existe pas!")
            print("   Exécutez d'abord le calculateur pour générer des rapports.")
            return None
        
        # Trouver tous les fichiers CSV dans le dossier
        csv_files = glob.glob(os.path.join(self.reports_dir, '*.csv'))
        
        if len(csv_files) == 0:
            print(f"❌ Aucun rapport trouvé dans {self.reports_dir}/")
            print("   Exécutez d'abord le calculateur pour générer des rapports.")
            return None
        
        print(f"✅ {len(csv_files)} rapport(s) trouvé(s)\n")
        
        # Charger tous les CSV
        all_dataframes = []
        for csv_file in csv_files:
            print(f"   📄 Chargement: {os.path.basename(csv_file)}")
            df = pd.read_csv(csv_file)
            
            # Ajouter le nom du fichier comme colonne pour traçabilité
            df['source_file'] = os.path.basename(csv_file)
            
            all_dataframes.append(df)
        
        # Fusionner tous les DataFrames
        self.all_trades = pd.concat(all_dataframes, ignore_index=True)
        
        # Convertir les timestamps en datetime
        self.all_trades['entry_time'] = pd.to_datetime(self.all_trades['entry_time'])
        self.all_trades['exit_time'] = pd.to_datetime(self.all_trades['exit_time'])
        self.all_trades['lowest_price_time'] = pd.to_datetime(self.all_trades['lowest_price_time'])
        
        # Filtrer les trades avec drawdown calculé
        self.all_trades = self.all_trades[self.all_trades['max_drawdown_points'].notna()]
        
        print(f"\n✅ Total : {len(self.all_trades)} trades chargés avec succès")
        
        return self.all_trades
    
    def generate_global_statistics(self):
        """
        Génère des statistiques globales sur tous les trades
        """
        if self.all_trades is None or len(self.all_trades) == 0:
            print("⚠️  Aucune donnée à analyser")
            return
        
        print("\n" + "="*60)
        print("📈 STATISTIQUES GLOBALES")
        print("="*60 + "\n")
        
        # Informations générales
        print(f"📅 Période couverte:")
        print(f"   Du {self.all_trades['entry_time'].min().strftime('%d/%m/%Y')}", end="")
        print(f" au {self.all_trades['entry_time'].max().strftime('%d/%m/%Y')}")
        print(f"\n📊 Nombre total de trades: {len(self.all_trades)}")
        
        # Répartition Long/Short
        direction_counts = self.all_trades['direction'].value_counts()
        print(f"\n🎯 Répartition:")
        for direction, count in direction_counts.items():
            percentage = (count / len(self.all_trades)) * 100
            print(f"   {direction}: {count} trades ({percentage:.1f}%)")
        
        # Statistiques Drawdown
        print(f"\n⬇️  DRAWDOWN EN POINTS:")
        print(f"   Moyen: {self.all_trades['max_drawdown_points'].mean():.2f} points")
        print(f"   Médian: {self.all_trades['max_drawdown_points'].median():.2f} points")
        print(f"   Maximum: {self.all_trades['max_drawdown_points'].max():.2f} points")
        print(f"   Minimum: {self.all_trades['max_drawdown_points'].min():.2f} points")
        print(f"   Écart-type: {self.all_trades['max_drawdown_points'].std():.2f} points")
        
        print(f"\n💰 DRAWDOWN EN DOLLARS:")
        print(f"   Moyen: ${self.all_trades['max_drawdown_dollars'].mean():.2f}")
        print(f"   Médian: ${self.all_trades['max_drawdown_dollars'].median():.2f}")
        print(f"   Maximum: ${self.all_trades['max_drawdown_dollars'].max():.2f}")
        print(f"   Minimum: ${self.all_trades['max_drawdown_dollars'].min():.2f}")
        
        print(f"\n📊 DRAWDOWN EN POURCENTAGE:")
        print(f"   Moyen: {self.all_trades['max_drawdown_percent'].mean():.3f}%")
        print(f"   Médian: {self.all_trades['max_drawdown_percent'].median():.3f}%")
        print(f"   Maximum: {self.all_trades['max_drawdown_percent'].max():.3f}%")
        print(f"   Minimum: {self.all_trades['max_drawdown_percent'].min():.3f}%")
        
        # Statistiques P&L
        print(f"\n💵 PROFIT & LOSS:")
        print(f"   P&L Total: {self.all_trades['profit_loss'].sum():.2f} points")
        print(f"   P&L Moyen par trade: {self.all_trades['profit_loss'].mean():.2f} points")
        trades_gagnants = len(self.all_trades[self.all_trades['profit_loss'] > 0])
        win_rate = (trades_gagnants / len(self.all_trades)) * 100
        print(f"   Win Rate: {win_rate:.1f}% ({trades_gagnants}/{len(self.all_trades)})")
        
    def analyze_by_direction(self):
        """
        Analyse séparée pour LONG et SHORT
        """
        if self.all_trades is None or len(self.all_trades) == 0:
            return
        
        print("\n" + "="*60)
        print("🔍 ANALYSE PAR DIRECTION")
        print("="*60)
        
        for direction in ['LONG', 'SHORT']:
            trades_dir = self.all_trades[self.all_trades['direction'] == direction]
            
            if len(trades_dir) == 0:
                continue
            
            print(f"\n📈 {direction} ({len(trades_dir)} trades):")
            print(f"   DD Moyen: {trades_dir['max_drawdown_points'].mean():.2f} points")
            print(f"   DD Médian: {trades_dir['max_drawdown_points'].median():.2f} points")
            print(f"   DD Maximum: {trades_dir['max_drawdown_points'].max():.2f} points")
            print(f"   P&L Moyen: {trades_dir['profit_loss'].mean():.2f} points")
    
    def analyze_by_date(self):
        """
        Analyse par jour de trading
        """
        if self.all_trades is None or len(self.all_trades) == 0:
            return
        
        print("\n" + "="*60)
        print("📅 ANALYSE PAR JOUR DE TRADING")
        print("="*60 + "\n")
        
        # Extraire la date (sans heure)
        self.all_trades['date'] = self.all_trades['entry_time'].dt.date
        
        # Grouper par date
        for date, group in self.all_trades.groupby('date'):
            print(f"📆 {date.strftime('%d/%m/%Y')} ({len(group)} trades):")
            print(f"   DD Moyen: {group['max_drawdown_points'].mean():.2f} points")
            print(f"   P&L Total: {group['profit_loss'].sum():.2f} points")
            print()
    
    def find_worst_trades(self, n=5):
        """
        Trouve les N pires trades (plus gros drawdowns)
        
        Args:
            n (int): Nombre de trades à afficher
        """
        if self.all_trades is None or len(self.all_trades) == 0:
            return
        
        print("\n" + "="*60)
        print(f"⚠️  TOP {n} DES PLUS GROS DRAWDOWNS")
        print("="*60 + "\n")
        
        worst_trades = self.all_trades.nlargest(n, 'max_drawdown_points')
        
        for idx, trade in worst_trades.iterrows():
            print(f"🔴 Trade {int(trade['trade_number'])} - {trade['direction']}")
            print(f"   Date: {trade['entry_time'].strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"   Drawdown: {trade['max_drawdown_points']:.2f} points (${trade['max_drawdown_dollars']:.2f})")
            print(f"   P&L: {trade['profit_loss']:.2f} points")
            print(f"   Fichier: {trade['source_file']}")
            print()
    
    def find_best_trades(self, n=5):
        """
        Trouve les N meilleurs trades (plus petits drawdowns)
        
        Args:
            n (int): Nombre de trades à afficher
        """
        if self.all_trades is None or len(self.all_trades) == 0:
            return
        
        print("\n" + "="*60)
        print(f"✅ TOP {n} DES PLUS PETITS DRAWDOWNS")
        print("="*60 + "\n")
        
        best_trades = self.all_trades.nsmallest(n, 'max_drawdown_points')
        
        for idx, trade in best_trades.iterrows():
            print(f"🟢 Trade {int(trade['trade_number'])} - {trade['direction']}")
            print(f"   Date: {trade['entry_time'].strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"   Drawdown: {trade['max_drawdown_points']:.2f} points (${trade['max_drawdown_dollars']:.2f})")
            print(f"   P&L: {trade['profit_loss']:.2f} points")
            print(f"   Fichier: {trade['source_file']}")
            print()
    
    def export_consolidated_report(self, output_file='rapport_consolide.csv'):
        """
        Exporte un rapport consolidé de tous les trades
        
        Args:
            output_file (str): Nom du fichier de sortie
        """
        if self.all_trades is None or len(self.all_trades) == 0:
            return
        
        output_path = os.path.join(self.reports_dir, output_file)
        
        print(f"\n💾 Export du rapport consolidé...")
        self.all_trades.to_csv(output_path, index=False)
        print(f"✅ Rapport consolidé sauvegardé: {output_path}")


def main():
    """
    Fonction principale
    """
    print("\n")
    
    # Créer l'analyseur
    analyzer = GlobalDrawdownAnalyzer()
    
    # Charger tous les rapports
    data = analyzer.load_all_reports()
    
    if data is None:
        return
    
    # Générer les analyses
    analyzer.generate_global_statistics()
    analyzer.analyze_by_direction()
    analyzer.analyze_by_date()
    analyzer.find_worst_trades(5)
    analyzer.find_best_trades(5)
    
    # Exporter le rapport consolidé
    analyzer.export_consolidated_report()
    
    print("\n" + "="*60)
    print("🎉 ANALYSE TERMINÉE")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
