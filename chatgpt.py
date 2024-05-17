import tiktoken
import config
import requests


def estimated_cost(input_price, output_price, model, prompt, count_lines, url):
    prompt = prompt.replace("url", url)
    input_price /= 1000000
    output_price /= 1000000
    tokenizer = tiktoken.encoding_for_model(model)
    input_total = tokenizer.encode(prompt)
    input_total = len(input_total)
    input_total *= 1.15
    input_total = input_total * input_price
    output_total = "00.00, EUR"
    output_total = tokenizer.encode(output_total)
    output_total = len(output_total)
    output_total = output_total * output_price
    total_cost = input_total + output_price
    total_cost = total_cost * count_lines
    return (total_cost)

def get_price_format(fetched_content, country):
    model = config.model
    api_key = config.api_key
    endpoint_url = "https://api.openai.com/v1/chat/completions"
    prompt = config.prompt
    url = config.url
    prompt = prompt.replace("url", url)
    prompt = prompt.replace("country", country)
    prompt = prompt.replace("fetched_content", fetched_content)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ]
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(endpoint_url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return (data["choices"][0]["message"]["content"])