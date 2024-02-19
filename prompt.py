import os
import util


herb = 'ginger'
problem = 'bloating'

rows = util.csv_get_rows('database/remedies/remedies.csv')
rows = [row for row in rows if row[0].strip().lower() == problem]

herbal_mix = f'{rows[0][2].strip()} Tea, {rows[1][2].strip()} Tea, and {rows[1][2].strip()} Tea'


print(f'''

Write a 60-word paragraph explaining why {herb} tea helps with {problem}.

-------------------------------------------------

''')

print(f'''

Write a 60-word paragraph answering this question: 

What is the best herbal tea mix for acid reflux? 

Tell in the answer that the best herbal tea mix for acid reflux is {herbal_mix}. 
Then explain why it is the best herbal tea mix for acid reflux.
Start the answer with these words: The best herbal tea mix for acid reflux is 

-------------------------------------------------

''')


