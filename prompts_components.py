model = ''
purpose = ''
variables = ''
examples = ''
output = ''

def prompt_1():
    prompt = f'''
        ping
    '''
    return prompt


def prompt_2():
    prompt = f'''
        create a title for a blog post about llms
    '''
    return prompt


def prompt_3(topic):
    prompt = f'''
        create a title for a blog post about TOPIC

        TOPIC

        {topic} 
    '''
    return prompt


def prompt_4():
    prompt = f'''
        # new python function generator
        
        create a new python function that will meet the function requirements.
        respond with only the function in the same format as in the examples.
        
        ## function requirements
        
        replace_string_start_end(str, start_match, end_match) -> str

        ## example formats

        ### example 1
        ``` python
        def add(a: int, b: int) -> int:
            return a + b
        ```

        ### example 2
        ``` python
        def http_request(url: str) -> str:
            return requests.get(url).text
        ```

        ### example 3
        ``` python
        def write_yaml(data: dict, filename: str) -> None:
            with open(filename, 'w') as file:
                yaml.dump(data, file)
        ```
    '''
    return prompt


def prompt_5():
    prompt = f'''
        create a title for a blog post about TOPIC, with a great HOOK, and 5 seo optimized keywords.
        respond in JSON format in the EXAMPLE_STRUCTURE.

        TOPIC

        LLMs
        
        EXAMPLE_STRUCTURE
        {
            "title": "title of the blog post",
            "hook": "compelling and engaging hook",
            "seo_keywords": ["AI", "Machine Learning", "Natural Language Processing", "Large Language Models", "GPT-3"]
        }
        
    '''
    return prompt


def prompt_6():
    prompt = f'''
        # ...
        
        ## GUIDELINES

        ## TOPIC
    
        ## PREVIOUS_KNOWLEDGE

    '''
    return prompt

def prompt_test():
    prompt = f'''
        create a title for a blog post about TOPIC, with a great HOOK, and 5 seo optimized keywords.
        respond in JSON format in the EXAMPLE_STRUCTURE.

        TOPIC

        LLMs
        
        EXAMPLE_STRUCTURE
        {
            "title": "title of the blog post",
            "hook": "compelling and engaging hook",
            "seo_keywords": ["AI", "Machine Learning", "Natural Language Processing", "Large Language Models", "GPT-3"]
        }
        
    '''
    return prompt


