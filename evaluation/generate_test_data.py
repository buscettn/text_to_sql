import pandas as pd
import os

os.makedirs('evaluation', exist_ok=True)
data = {
    'query': [
        'get all users',
        'find invoices from today',
        'invalid query row',
        'missing sql row'
    ],
    'sql': [
        'SELECT * FROM users',
        'SELECT * FROM invoices WHERE date = today()',
        'SELECT * FROM users',  # This one will fail accuracy if model outputs something else
        None
    ]
}

df = pd.DataFrame(data)
df.to_excel('evaluation/ground_truth.xlsx', index=False)
print("Dummy ground truth created.")
