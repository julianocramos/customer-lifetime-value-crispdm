from pathlib import Path
p = Path(__file__).with_name('build_portfolio_assets.py')
s = p.read_text(encoding='utf-8')
replacements = {
    'params[2][5]="Intercept"; params[2][6]=PARAMS["intercept"]': 'params.cell(2,6,"Intercept"); params.cell(2,7,PARAMS["intercept"])',
    'params[3][5]="Mean - first_purchase_value"; params[3][6]=PARAMS["mean_first_purchase"]': 'params.cell(3,6,"Mean - first_purchase_value"); params.cell(3,7,PARAMS["mean_first_purchase"])',
    'params[4][5]="Scale - first_purchase_value"; params[4][6]=PARAMS["scale_first_purchase"]': 'params.cell(4,6,"Scale - first_purchase_value"); params.cell(4,7,PARAMS["scale_first_purchase"])',
    'params[5][5]="Coefficient - first_purchase_value"; params[5][6]=PARAMS["coef_first_purchase"]': 'params.cell(5,6,"Coefficient - first_purchase_value"); params.cell(5,7,PARAMS["coef_first_purchase"])',
    'params[6][5]="Coefficient - recurring_first_purchase"; params[6][6]=PARAMS["coef_recurring"]': 'params.cell(6,6,"Coefficient - recurring_first_purchase"); params.cell(6,7,PARAMS["coef_recurring"])',
}
for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f'Expected source pattern not found: {old}')
    s = s.replace(old, new)
p.write_text(s, encoding='utf-8')
print('Asset generator patched successfully')
