import os

import g
import util

conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
conditions_cols = util.csv_get_cols(conditions_rows)
conditions_rows = conditions_rows[1:]


def tea_redirects():
    for condition_row in conditions_rows:
        condition_id = condition_row[conditions_cols['condition_id']].strip().lower()
        condition_slug = condition_row[conditions_cols['condition_slug']].strip().lower()
        condition_slugs_prev = condition_row[conditions_cols['condition_slugs_prev']].strip().lower()
        to_process = condition_row[conditions_cols['to_process']].strip().lower()

        if condition_id == '': continue
        if condition_slug == '': continue
        if to_process == '': continue

        # print(condition_id, condition_slug)

        # REDIRECTS
        condition_slugs_prev_list = condition_slugs_prev.split(',')
        for condition_slug_prev in condition_slugs_prev_list:
            print(condition_slug_prev)
            if condition_slug_prev == condition_slug: continue
            
            html_filepath_web = f'https://terrawhisper.com/herbalism/tea/{condition_slug}.html'
            html_filepath_out = f'website/herbalism/tea/{condition_slug_prev}.html'
            if os.path.exists(html_filepath_out):
                html = util.file_read(html_filepath_out)
                if f'<meta http-equiv="refresh" content="0; url={html_filepath_web}">' not in html:
                    html = html.replace(
                        '<head>',
                        f'<head>\n<meta http-equiv="refresh" content="0; url={html_filepath_web}">'
                    )
                util.file_write(html_filepath_out, html)

tea_redirects()



'''
gut-health
bad-breath
dry-mouth
mouth-ulcers
oral-thrush
periodontal-disease
esophagus-health
throat-pain
heartburn
acid-reflux
gerd
digestion
indigestion
stomach-pain
stomach-cramps
hyperacidity
gastric-problem
gastritis
mucus-stomach
peptic-ulcers
gastroenteritis
gastroparesis
hiatus-hernia
queasy-stomach
upset-stomach
nausea
vomiting
gas
gas-stomach
bloating
overeating
food-poisoning
hangover
jaundice
chronic-hepatitis
viral-hepatitis
cirrhosis
gallstones
cholecystitis
abdominal-pain
gas-pain
bowel-movement
quick-digestion
inflammatory-bowel-disease
constipation
diarrhea
flatulence
irritable-bowel-syndrome
ulcerative-colitis
diverticulitis
colon-cleanse
hemorrhoids
hay-fever
blocked-nose
runny-nose
post-nasal-drip
sinus-headache
sinusitis
sore-throat
dry-throat
snoring
laryngitis
hoarse-voice
lost-voice
tonsillitis
cough
flu
chest-congestion
bronchitis
asthma
phlegm
acute-bronchitis
chronic-bronchitis
pertussis
emphysema
hiccups
colds
mucus
nasal-congestion
high-blood-pressure
low-blood-pressure
heart-pain
high-cholesterol
jaundice
nose-bleeding
palpitation
swollen-feet
arteriosclerosis
congestive-heart-failure
peripheral-arterial-occlusive-disease
varicose-veins
circulation
cholesterol
heart-health
hypertension
muscle-pain
osteoporosis
arthritis
joint-pain
joint-stiffness
osteoarthritis
rheumatoid-arthritis
bursitis
tendinitis
gout
back-pain
lower-back-pain
stiff-neck
neck-pain
frozen-shoulder
jammed-finger
leg-cramps
leg-pain
restless-leg-syndrome
knee-pain
knee-swelling
foot-pain
plantar-fasciitis
chapped-lips
jaw-pain
jaw-lock
jaw-clenching
eye-twitching
bone-health
cramps
itchy-skin
acne
bee-sting
boils
chickenpox
dry-skin
excessive-sweating
fungal-infection
glowing-skin
insect-bites
ingrown-hair
jellyfish-sting
open-pores
open-wounds
pimples
pigmentation
ringworm
rashes
sunburn
eczema
psoriasis
dermatitis
nail-fungus
dry-hair
frizzy-hair
grey-hair
hair-fall
oily-hair
quick-hair-growth
dandruff
dry-scalp
itchy-scalp
lice
swollen-gums
oily-skin
clear-skin
eye-health
eyesight
hair-growth
headache
alertness
brain-fog
fatigue
sleep
ear-infection
earache
eye-floaters
focus
concentration
grief
allergies
fever
infection
bladder-pain
dehydration
fluid-retention
hydration
endometriosis-pain
fertility
breastfeeding
female-libido
female-fertility
female-hormone-balance
belly-fat
weight-loss
anti-aging
appetite-suppression
diet
energy-boost
flat-tummy
fasting
fat-loss
good-health
enlarged-spleen
aging
altitude-sickness
alzheimer-disease
angina
akylosing-spondylitis
baldness
bladder-infection
body-odor
breast-enlargement
bruises
bunion
burns
wheezing
breath-shortness
chills
appetite-loss
difficulty-swallowing
inflamed-gums
white-tongue
bad-taste
taste-changes
dental-plaque
tooth-decay
dry-nose
inflamed-mouth
difficulty-chewing
speech-difficulty
lymph-node-swelling
month-white-patches
taste-loss
mouth-reddened-corners
difficulty-eating
painful-swallowing
mouth-bleeding-spots
dry-cough
throat-congestion
difficult-speaking
feverish-feeling
tickling-throat
throat-redness
throat-irritation
mouth-sour-taste
mouth-bitter-taste
burping
regurgitation
stomach-discomfort
coughing-fits
stomach-growling
upper-abdominal-pain
food-intolerance
'''