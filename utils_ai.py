from groq import Groq

client = Groq(
    api_key='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',
)



def gen_reply(prompt):
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
