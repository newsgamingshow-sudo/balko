"""Génère le Pack Pro micro-entrepreneur (xlsx) dans produit/dist/."""
import pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
OUT = pathlib.Path(__file__).parent / "dist"; OUT.mkdir(exist_ok=True)
H = PatternFill("solid", fgColor="1F6F5C"); HF = Font(bold=True, color="FFFFFF"); B = Font(bold=True)
thin = Side(style="thin", color="CCCCCC"); BOX = Border(top=thin, bottom=thin, left=thin, right=thin)
EUR = '#,##0.00 "€"'; MOIS = ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
def header(ws, row, cols, widths=None):
    for i, c in enumerate(cols, 1):
        x = ws.cell(row=row, column=i, value=c); x.fill = H; x.font = HF; x.alignment = Alignment(wrap_text=True, vertical="center")
    if widths:
        for i, w in enumerate(widths, 1): ws.column_dimensions[chr(64 + i)].width = w
wb = Workbook()
# --- Paramètres
p = wb.active; p.title = "Paramètres"
p["A1"] = "Paramètres — à vérifier et adapter chaque année (autoentrepreneur.urssaf.fr)"; p["A1"].font = Font(bold=True, size=13)
rows = [("Année", 2026), ("Taux de cotisations sociales (% du CA)", 0.212), ("Versement libératoire de l'impôt (% du CA, 0 si non opté)", 0.017),
        ("Contribution à la formation professionnelle (% du CA)", 0.002), ("Plafond de CA du régime micro (€)", 77700), ("Délai de paiement par défaut (jours)", 30)]
for i, (k, v) in enumerate(rows, 3):
    p.cell(row=i, column=1, value=k); c = p.cell(row=i, column=2, value=v); c.fill = PatternFill("solid", fgColor="FFF4D6"); c.border = BOX
p["B4"].number_format = p["B5"].number_format = p["B6"].number_format = "0.0%"; p["B7"].number_format = EUR
p["A10"] = "Cellules jaunes = à remplir. Les autres onglets se calculent automatiquement."
p["A11"] = "Les valeurs par défaut sont indicatives : vérifiez les taux et le plafond correspondant à votre activité."
p.column_dimensions["A"].width = 62; p.column_dimensions["B"].width = 16
# --- Livre des recettes
r = wb.create_sheet("Livre des recettes")
header(r, 1, ["Date d'encaissement", "N° facture", "Client", "Nature de la prestation / vente", "Montant encaissé (€)", "Mode de règlement", "Mois (auto)"], [18, 14, 26, 38, 18, 18, 12])
dv = DataValidation(type="list", formula1='"Virement,Carte,Chèque,Espèces,PayPal,Autre"', allow_blank=True); r.add_data_validation(dv)
for i in range(2, 502):
    r.cell(row=i, column=1).number_format = "DD/MM/YYYY"; r.cell(row=i, column=5).number_format = EUR; dv.add(f"F{i}")
    r.cell(row=i, column=7, value=f'=IF(A{i}="","",MONTH(A{i}))')
r.freeze_panes = "A2"
# --- Suivi des factures
f = wb.create_sheet("Suivi des factures")
header(f, 1, ["N° facture", "Client", "Date d'émission", "Montant (€)", "Échéance (auto)", "Date de paiement", "Statut (auto)", "Jours de retard (auto)"], [14, 26, 16, 14, 16, 16, 14, 16])
for i in range(2, 302):
    for col in (3, 5, 6): f.cell(row=i, column=col).number_format = "DD/MM/YYYY"
    f.cell(row=i, column=4).number_format = EUR
    f.cell(row=i, column=5, value=f'=IF(C{i}="","",C{i}+Paramètres!$B$8)')
    f.cell(row=i, column=7, value=f'=IF(A{i}="","",IF(F{i}<>"","Payée",IF(TODAY()>E{i},"En retard","En attente")))')
    f.cell(row=i, column=8, value=f'=IF(G{i}="En retard",TODAY()-E{i},"")')
f.conditional_formatting.add("G2:G301", FormulaRule(formula=['G2="En retard"'], fill=PatternFill("solid", fgColor="F8D0D0")))
f.conditional_formatting.add("G2:G301", FormulaRule(formula=['G2="Payée"'], fill=PatternFill("solid", fgColor="D3EFE5")))
f["J1"] = "Total impayé"; f["J1"].font = B; f["K1"] = '=SUMIF(G2:G301,"<>Payée",D2:D301)'; f["K1"].number_format = EUR
f["J2"] = "Dont en retard"; f["K2"] = '=SUMIF(G2:G301,"En retard",D2:D301)'; f["K2"].number_format = EUR
f.column_dimensions["J"].width = 16; f.column_dimensions["K"].width = 14; f.freeze_panes = "A2"
# --- Tableau de bord
d = wb.create_sheet("Tableau de bord", 0)
d["A1"] = "Tableau de bord annuel"; d["A1"].font = Font(bold=True, size=15)
header(d, 3, ["Mois", "CA encaissé", "Cotisations", "Impôt (VL)", "CFP", "Net après prélèvements", "CA cumulé"], [14, 15, 14, 13, 11, 22, 15])
for m in range(12):
    i = 4 + m; d.cell(row=i, column=1, value=MOIS[m])
    d.cell(row=i, column=2, value=f"=SUMIF('Livre des recettes'!G:G,{m+1},'Livre des recettes'!E:E)")
    d.cell(row=i, column=3, value=f"=B{i}*Paramètres!$B$4"); d.cell(row=i, column=4, value=f"=B{i}*Paramètres!$B$5")
    d.cell(row=i, column=5, value=f"=B{i}*Paramètres!$B$6"); d.cell(row=i, column=6, value=f"=B{i}-C{i}-D{i}-E{i}")
    d.cell(row=i, column=7, value=f"=SUM($B$4:B{i})")
    for c in range(2, 8): d.cell(row=i, column=c).number_format = EUR
d["A16"] = "TOTAL"; d["A16"].font = B
for c in "BCDEF": d[f"{c}16"] = f"=SUM({c}4:{c}15)"; d[f"{c}16"].font = B; d[f"{c}16"].number_format = EUR
d["A18"] = "Plafond micro restant"; d["B18"] = "=Paramètres!B7-B16"; d["B18"].number_format = EUR; d["A18"].font = B
d["A19"] = "Plafond utilisé"; d["B19"] = "=IFERROR(B16/Paramètres!B7,0)"; d["B19"].number_format = "0%"
d["A20"] = "Factures impayées"; d["B20"] = "='Suivi des factures'!K1"; d["B20"].number_format = EUR
d["A22"] = "Saisissez vos encaissements dans « Livre des recettes » : ce tableau se remplit tout seul."
wb.save(OUT / "Balko-Pack-Pro-micro-entrepreneur.xlsx")
# --- Modèles de relance
(OUT / "Modeles-de-relance-impayes.txt").write_text("""MODÈLES DE RELANCE D'IMPAYÉS — Pack Pro Balko
Remplacez les éléments entre crochets.

1) RELANCE AMIABLE (quelques jours après l'échéance)
Objet : Facture [N°] — rappel de paiement
Bonjour [Prénom],
Sauf erreur de ma part, la facture [N°] du [date], d'un montant de [montant] €, arrivée à échéance le [date], n'a pas encore été réglée. Il s'agit peut-être d'un simple oubli : je vous la remets en pièce jointe.
Pourriez-vous me confirmer la date de règlement prévue ?
Bien cordialement,
[Nom]

2) RELANCE FERME (environ 15 jours après l'échéance)
Objet : Facture [N°] — deuxième relance
Bonjour [Prénom],
Malgré ma précédente relance du [date], la facture [N°] de [montant] € reste impayée à ce jour.
Je vous remercie de procéder au règlement sous 8 jours. Je vous rappelle que, conformément à mes conditions de vente, des pénalités de retard ainsi qu'une indemnité forfaitaire de 40 € pour frais de recouvrement sont exigibles en cas de retard de paiement entre professionnels.
Cordialement,
[Nom]

3) MISE EN DEMEURE (à envoyer en recommandé avec accusé de réception)
Objet : Mise en demeure de payer — facture [N°]
Madame, Monsieur,
Par la présente, je vous mets en demeure de me régler sous 8 jours à compter de la réception de ce courrier la somme de [montant] € correspondant à la facture [N°] du [date], restée impayée malgré mes relances des [dates].
À défaut de paiement dans ce délai, je me réserve le droit d'engager une procédure de recouvrement (injonction de payer), les frais restant à votre charge, en plus des pénalités de retard et de l'indemnité forfaitaire de 40 €.
Veuillez agréer, Madame, Monsieur, mes salutations distinguées.
[Nom, adresse, SIRET]
""", encoding="utf-8")
print("Pack généré dans", OUT)
