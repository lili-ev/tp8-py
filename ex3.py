
import csv
from datetime import datetime


class BatchProcessor:

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.fichier_csv = None
        self.fichier_journal = None

    def __enter__(self):
        try:
            self.fichier_csv = open(
                self.csv_file,
                "r",
                newline="",
                encoding="cp1252"
            )

            self.fichier_journal = open(
                "journal.log",
                "a",
                encoding="utf-8"
            )

            self.journaliser("Début du traitement")
            return self

        except OSError as e:
            if self.fichier_csv and not self.fichier_csv.closed:
                self.fichier_csv.close()

            if self.fichier_journal and not self.fichier_journal.closed:
                self.fichier_journal.close()

            raise e

    def journaliser(self, message):
        try:
            self.fichier_journal.write(
                f"[{datetime.now()}] {message}\n"
            )
            self.fichier_journal.flush()

        except OSError as e:
            print("Erreur d'écriture du journal :", e)
            raise

    def traiter(self):
        try:
            lecteur = csv.reader(self.fichier_csv)

            for ligne in lecteur:
                if ligne:
                    operation = ligne[0]
                    print(f"Traitement de l'opération : {operation}")

        except (OSError, csv.Error, UnicodeDecodeError) as e:
            print("Erreur de lecture du CSV :", e)
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type:
                self.journaliser(
                    f"Erreur durant le traitement : {exc_value}"
                )
            else:
                self.journaliser("Fin du traitement")

        finally:
            if self.fichier_csv and not self.fichier_csv.closed:
                self.fichier_csv.close()

            if self.fichier_journal and not self.fichier_journal.closed:
                self.fichier_journal.close()

        return False


# Exemple d'utilisation

with BatchProcessor("operations.csv") as processor:
    processor.traiter()
