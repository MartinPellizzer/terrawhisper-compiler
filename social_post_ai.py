from oliark_llm import llm_reply

model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

########################################
# ;headline
########################################

'''
NOTES
big numbers
the success story
dollar signs
things that shouldn't go together
credible names
for the industry
"this just happened"
the topic within the topic ()
question/answer
x number
'''

def headlines_ai():
    topic = 'surface sanitization for food safety industry'
    headline_example = f'''9 reasons writers experience writer's block'''
    how_many = '9'
    what = 'reasons'
    who = 'writer'
    feel = 'experience'
    outcome = '''writer's block'''
    prompt = f'''
        write a list of 10 titles for an article post about {topic} with the following components:
        - how many things the article teaches: for example the number "7"
        - what are these things the article teaches: for example the word "reasons"
        - who is the audience article for: for example the word "writer"
        - a feel word that resonate with the audience: for example the word "experience"
        - outcome or promise of this article: for example the words "writer's block"
        example of title is: {headline_example}.
        /no_think
    '''
    reply = llm_reply(prompt, model_path=model_filepath).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

def headlines_templates_ai():
    topic = 'surface sanitization for food safety industry'
    headline_example = f'''9 reasons writers experience writer's block'''
    how_many = '9'
    what = 'reasons'
    who = 'writer'
    feel = 'experience'
    outcome = '''writer's block'''
    prompt = f'''
        write a list of 10 headlines for an article post about {topic}.
        Take inspiration from the structures of the headline examples below:
        - big numbers: 3000 people just filed for unemployment in this small town in arkansas. here's why.
        - the success story: how this small team managed to secure a six-figure investment in less than 1 week.
        - dollar signs: $400 millions is how much you need to make in order to afford this insane mansion in malibu.
        - things that shouldn't go together: 7 things kfc and miley cyrus have in common
        - credible names: will smith'x advice on how to live a fulfilling lige will hcange the way you see the world forever
        - for the industry: 3 things all successful small business owners do to stay profitable
        - this just happened: michael jordan just gave a press conference and nba executives are furious
        - the topic within the topic: 7 ways the real estate indutry is changing (and how you should be investing your money)
        - question/answer: can't be productive in the office? try organizing your calendar like this
        - x number: 13 things mentally strong people don't do
        /no_think
    '''
    reply = llm_reply(prompt, model_path=model_filepath).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

def headlines_0000_ai():
    topic = 'surface sanitization for food safety industry'
    headline_example = f'''9 reasons writers experience writer's block'''
    how_many = '9'
    what = 'reasons'
    who = 'writer'
    feel = 'experience'
    outcome = '''writer's block'''
    prompt = f'''
        write a list of 10 headlines for an article post with the following TOPIC, COMPONENTS, and STRUCTURES. 
        TOPIC:
        {topic} with the following components:
        COMPONENTS:
        - how many things the article teaches: for example the number "7"
        - what are these things the article teaches: for example the word "reasons"
        - who is the audience article for: for example the word "writer"
        - a feel word that resonate with the audience: for example the word "experience"
        - outcome or promise of this article: for example the words "writer's block"
        example of title is: {headline_example}.
        STRUCTURES:
        - big numbers: 3000 people just filed for unemployment in this small town in arkansas. here's why.
        - the success story: how this small team managed to secure a six-figure investment in less than 1 week.
        - dollar signs: $400 millions is how much you need to make in order to afford this insane mansion in malibu.
        - things that shouldn't go together: 7 things kfc and miley cyrus have in common
        - credible names: will smith'x advice on how to live a fulfilling lige will hcange the way you see the world forever
        - for the industry: 3 things all successful small business owners do to stay profitable
        - this just happened: michael jordan just gave a press conference and nba executives are furious
        - the topic within the topic: 7 ways the real estate indutry is changing (and how you should be investing your money)
        - question/answer: can't be productive in the office? try organizing your calendar like this
        - x number: 13 things mentally strong people don't do
        /no_think
    '''
    reply = llm_reply(prompt, model_path=model_filepath).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

headline_manual = '3 herbs to help night owls finally sleep'

# headlines_ai()
# headlines_templates_ai()
headlines_0000_ai()
