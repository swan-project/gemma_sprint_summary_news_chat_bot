from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline, TrainingArguments

# Replace 'your_token_here' with your actual Hugging Face token
token = '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'
login(token)
BASE_MODEL = "google/gemma-2b-it"

model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, device_map={"":0})
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)


messages = [
    {"role": "user",
     "content": "...."}
     ]

prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)

from datasets import load_dataset
dataset = load_dataset("wisenut-nlp-team/llama_ko_smr","technology_science")

doc= dataset['train']['input'][0]

messages = [
    {
        "role": "user",
        "content": "다음 글을 요약해주세요:\n\n{}".format(doc)
    }
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

print(prompt)


# 데이터셋의 분할 및 정보 확인
print(dataset)


outputs = pipe(
    prompt,
    do_sample=True,
    temperature=0.2,
    top_k=50,
    top_p=0.95,
    add_special_tokens=True
)

print(outputs[0]["generated_text"][len(prompt):])
