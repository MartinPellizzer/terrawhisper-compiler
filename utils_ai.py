from groq import Groq
from ctransformers import AutoModelForCausalLM


with open('C:/api/groq.txt', 'r', encoding='utf-8') as f:
    api = f.read()


client = Groq(
    api_key=api,
)


MODELS = [
    'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.1.Q8_0.gguf',
    'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.2.Q8_0.gguf',
    'C:\\Users\\admin\\Desktop\\models\\neural-chat-7b-v3-3.Q8_0.gguf',
    'C:\\Users\\admin\\.cache\\lm-studio\\models\\TheBloke\\Starling-LM-7B-alpha-GGUF\\starling-lm-7b-alpha.Q8_0.gguf',
]
MODEL = MODELS[1]

llm = AutoModelForCausalLM.from_pretrained(
    MODEL,
    model_type="mistral", 
    context_length=2048, 
    max_new_tokens=2048,
    )


def gen_reply_api(prompt):
    completion = client.chat.completions.create(
        # model="llama2-70b-4096",
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=1,
    )

    reply = completion.choices[0].message.content
    print()
    print()
    print()
    print("Q:")
    print()
    print(prompt)
    print()
    print("A:")
    print()
    print(reply)
    print()
    return reply


def gen_reply_local(prompt):
    print()
    print("Q:")
    print()
    print(prompt)
    print()
    print("A:")
    print()
    reply = ''
    for text in llm(prompt, stream=True):
        reply += text
        print(text, end="", flush=True)
    print()
    print()
    return reply


def gen_reply(prompt):
    reply = gen_reply_api(prompt)
    # reply = gen_reply_local(prompt)

    return reply
