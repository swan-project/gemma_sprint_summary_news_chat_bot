# from datasets import load_dataset
# dataset = load_dataset("wisenut-nlp-team/llama_ko_smr","technology_science")

# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

# model_id = "beomi/gemma-ko-2b"
# #model_id = "google/gemma-7b"
# #model_id = "google/gemma-2b-it"
# #odel_id = "google/gemma-2b"

# bnb_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_compute_dtype=torch.bfloat16
# )

# model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map={"":0})
# tokenizer = AutoTokenizer.from_pretrained(model_id, add_eos_token=True)

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

# doc= dataset['train']['input'][0]

# messages = [
#     {
#         "role": "user",
#         "content": "다음 글을 요약해주세요:\n\n{}".format(doc)
#     }
# ]
# prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

# print(prompt)


# # 데이터셋의 분할 및 정보 확인
# print(dataset)


# outputs = pipe(
#     prompt,
#     do_sample=True,
#     temperature=0.2,
#     top_k=50,
#     top_p=0.95,
#     add_special_tokens=True
# )

# print(outputs[0]["generated_text"][len(prompt):])







from peft import LoraConfig, PeftModel
from trl import SFTTrainer
import torch
import bitsandbytes
#-----------------------------------------------------------------------------

# def generate_prompt(example):
#     prompt_list = []
#     for i in range(len(example['input'])):
#         prompt_list.append(r"""<bos><start_of_turn>user
# {}:
# {}<end_of_turn>
# <start_of_turn>model
# {}<end_of_turn><eos>""".format(example['instruction'][i], example['input'][i], example['output'][i]))
#     return prompt_list


# lora_config = LoraConfig(
#     r=6,
#     lora_alpha = 8,
#     lora_dropout = 0.05,
#     target_modules=["q_proj", "o_proj", "k_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
#     task_type="CAUSAL_LM",
# )

# bnb_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_compute_dtype=torch.float16
# )

# BASE_MODEL = "google/gemma-2b-it"

# model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, device_map="auto", quantization_config=bnb_config)
# tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
# tokenizer.padding_side = 'right'

# train_data = dataset['train']

# trainer = SFTTrainer(
#     model=model,
#     train_dataset=train_data,
#     max_seq_length=512,
#     args=TrainingArguments(
#         output_dir="outputs",
# #        num_train_epochs = 1,
#         max_steps=3000,
#         per_device_train_batch_size=1,
#         gradient_accumulation_steps=4,
#         optim="paged_adamw_8bit",
#         warmup_steps=int(3000 * 0.03),  # Converts 3% of 3000 to an integer
#         learning_rate=2e-4,
#         fp16=True,
#         logging_steps=100,
#         push_to_hub=False,
#         report_to='none',
#     ),
#     peft_config=lora_config,
#     formatting_func=generate_prompt,
# )

# trainer.train()


# ADAPTER_MODEL = "lora_adapter"

# trainer.model.save_pretrained(ADAPTER_MODEL)


#---------------------------------------------------------------------------------------

#BASE_MODEL = "google/gemma-7b-it"

# ADAPTER_MODEL = "lora_adapter"

# model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, device_map='auto', torch_dtype=torch.float16)
# model = PeftModel.from_pretrained(model, ADAPTER_MODEL, device_map='auto', torch_dtype=torch.float16)

# model = model.merge_and_unload()
# model.save_pretrained('gemma-2b-it-sum-ko-science')



#-----------------------------------------------------------------


BASE_MODEL = "google/gemma-2b-it"
FINETUNE_MODEL = "./gemma-2b-it-sum-ko-science"

finetune_model = AutoModelForCausalLM.from_pretrained(FINETUNE_MODEL, device_map={"":0})
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

pipe_finetuned = pipeline("text-generation", model=finetune_model, tokenizer=tokenizer, max_new_tokens=512)
doc = dataset['train']['input'][10]

doc = r"그렇게 등장한 것이 원자시계다. 원자가 1초 동안 움직이는 횟수인 ‘고유진동수’를 이용해 정확한 1초를 측정한다. 원자 속에 있는 전자들은 특정 에너지 상태로 있다. 이 상태에서 다른 상태로 변화하려면 에너지를 두 상태의 차이만큼 흡수하거나 방출해야 한다. 전자가 에너지를 얻기 위해(다른 에너지 상태로 변하기 위해) 전자기파를 흡수할 때 진동이 발생하는데, 이것이 바로 고유진동수다."
doc = r"천년만년 지나도 변하지 않는 곳이 있을까. 과학자들은 천년만년을 넘어 수억 년이 지나도 1초의 오차도 없이 일정하게 흐르는 시계를 개발하고 있다. 지구가 한 바퀴 자전하는 시간을 1일이라고 한다. 이것을 쪼개 시간과 분, 초를 정했다. 하지만 지구 자전 속도는 시간에 따라 변하므로 시간에 오차가 생겼다. 새로운 시간의 정의가 필요해진 이유다."
print(doc)
messages = [
    {
        "role": "user",
        "content": "다음 글을 요약해주세요:\n\n{}".format(doc)
    }
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


outputs = pipe_finetuned(
    prompt,
    do_sample=True,
    temperature=0.2,
    top_k=50,
    top_p=0.95,
    add_special_tokens=True
)
print(outputs[0]["generated_text"][len(prompt):])