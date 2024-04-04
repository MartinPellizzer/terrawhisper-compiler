import utils_ai
import time

# https://pubmed.ncbi.nlm.nih.gov/?term=chamomile+sleep 
# TODO: scrape studies and automate the summary generation

abstracts = [
'Sleep is considered as one of the most important aspects for maintaining a healthy life. For a person to function normally, at least 6-8 hours of sleep daily is necessary. Sleep not only affects our mood, but also regulates the efficiency of work done. Many complications arise due to inadequacy of sleep. The unhealthy food and lifestyle choices have made us more prone to sleep disorders. The medications used for the treatment of sleep disorders are mainly habit forming and have tendencies of withdrawal symptoms. This inadequacy in medication has lead to search for newer, better options. The field of nutraceuticals fits apt for treating such disorders. The quality of being non-toxic, non-habit forming, and being practically more efficient has had made it an excellent option. Nutraceuticals make use of food or part of food for the treatment or to prevent any disease. Remarkable positive effects of nutraceuticals like Caffeine, Chamomile, Kava kava, Cherries and Cherry juice, L tryptophan, Valerian, Vitamin D, Marijuana, melatonin, Lemon balm had been mentioned in the treatment of sleep disorders. The present review gives a general overview of nutraceuticals and discusses their use in sleep disorders.',
'Chamomile is an aromatic oil extracted from the flowers or leaves of the daisy-like plants including German chamomile (Matricaria recutita) and Roman or English chamomile (Chamaemelum nobile). Extracts, oils and teas made from chamomile are used for its soothing qualities as a sedative, mild analgesic and sleep medication. Chamomile has not been implicated in causing serum enzyme elevations or clinically apparent liver injury.',
'This systematic review and meta-analysis aimed to study the efficacy and safety of chamomile for the treatment of state anxiety, generalized anxiety disorders (GADs), sleep quality, and insomnia in human. Eleven databases including PubMed, Science Direct, Cochrane Central, and Scopus were searched to retrieve relevant randomized control trials (RCTs), and 12 RCTs were included. Random effect meta-analysis was performed by meta package of R statistical software version 3.4.3 and RevMan version 5.3. Our meta-analysis of three RCTs did not show any difference in case of anxiety (standardized mean difference = -0.15, 95% CI [-0.46, 0.16], P = 0.4214). Moreover, there is only one RCT that evaluated the effect of chamomile on insomnia and it found no significant change in insomnia severity index (P > 0.05). By using HAM-A scale, there was a significant improvement in GAD after 2 and 4 weeks of treatment (mean difference = -1.43, 95% CI [-2.47, -0.39], P = 0.007), (MD = -1.79, 95% CI [-3.14, -0.43], P = 0.0097), respectively. Noteworthy, our meta-analysis showed a significant improvement in sleep quality after chamomile administration (standardized mean difference = -0.73, 95% CI [-1.23, -0.23], P < 0.005). Mild adverse events were only reported by three RCTs. Chamomile appears to be efficacious and safe for sleep quality and GAD. Little evidence is there to show its effect on anxiety and insomnia. Larger RCTs are needed to ascertain these findings.',
]

abstract_text = ''
i = 0
for abstract in abstracts:
    abstract_text += f'{i}. {abstract}\n'
    i += 1

prompt = f'''
Here is a numbered list of 3 abstracts from scientific studies.
{abstract_text}
Return me the number of the abstract that talk in more details about the use of chamomile for sleep in a positive way.
Reply with -1 if none of the above abstract talk about chamomile for sleep in a positive way.
Choose only 1 abstract.
Reply with only a number and don't add additional content.
'''
reply = utils_ai.gen_reply(prompt)
num = 0
if '0' in reply: num = 0
if '1' in reply: num = 1
if '2' in reply: num = 2
time.sleep(30)

prompt = f'''
Write me a summary in less than 100 words about the following text.
{abstracts[num]}
'''
reply = utils_ai.gen_reply(prompt)
time.sleep(30)
