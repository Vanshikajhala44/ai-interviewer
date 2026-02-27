from groq import Groq
from django.conf import settings

client = Groq(api_key=settings.GROQ_API_KEY2)



def generate_coding_question(topic, difficulty, language):
    prompt = f"""
    Generate a coding interview question with the following details:
    - Topic: {topic}
    - Difficulty: {difficulty}
    - Language: {language}

    Respond in EXACTLY this format and nothing else:
    TITLE: <question title>
    DESCRIPTION: <detailed problem description>
    EXAMPLE INPUT: <example input>
    EXAMPLE OUTPUT: <example output>
    CONSTRAINTS: <constraints>
    STARTER CODE: <starter code in {language}>
    """

    response = client.chat.completions.create(
        model="groq/compound",
        messages=[
            {"role": "system", "content": "You are an expert coding interview question generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1024
    )

    return parse_question(response.choices[0].message.content)


def parse_question(text):
    result = {
        'title': '',
        'description': '',
        'example_input': '',
        'example_output': '',
        'constraints': '',
        'starter_code': ''
    }

    lines = text.strip().split('\n')
    current_key = None

    for line in lines:
        if line.startswith('TITLE:'):
            current_key = 'title'
            result['title'] = line.replace('TITLE:', '').strip()
        elif line.startswith('DESCRIPTION:'):
            current_key = 'description'
            result['description'] = line.replace('DESCRIPTION:', '').strip()
        elif line.startswith('EXAMPLE INPUT:'):
            current_key = 'example_input'
            result['example_input'] = line.replace('EXAMPLE INPUT:', '').strip()
        elif line.startswith('EXAMPLE OUTPUT:'):
            current_key = 'example_output'
            result['example_output'] = line.replace('EXAMPLE OUTPUT:', '').strip()
        elif line.startswith('CONSTRAINTS:'):
            current_key = 'constraints'
            result['constraints'] = line.replace('CONSTRAINTS:', '').strip()
        elif line.startswith('STARTER CODE:'):
            current_key = 'starter_code'
            result['starter_code'] = line.replace('STARTER CODE:', '').strip()
        elif current_key and line.strip():
            result[current_key] += '\n' + line.strip()

    return result