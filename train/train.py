from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline, TrainingArguments
from datasets import load_dataset, concatenate_datasets

from datasets import load_dataset
from peft import LoraConfig, PeftModel
from trl import SFTTrainer
import torch
import bitsandbytes

#-----------------------------------------------------------------------------

def generate_prompt(example):
    prompt_list = []
    for i in range(len(example['input'])):
        prompt_list.append(r"""<bos><start_of_turn>user
{}:
{}<end_of_turn>
<start_of_turn>model
{}<end_of_turn><eos>""".format(example['instruction'][i], example['input'][i], example['output'][i]))
    return prompt_list


lora_config = LoraConfig(
    r=6,
    lora_alpha = 8,
    lora_dropout = 0.05,
    target_modules=["q_proj", "o_proj", "k_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
    task_type="CAUSAL_LM",
)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)


data_subsets = [
    'law', 'newspaper', 'editorial', 'art', 'technology_science', 'social_science', 'etc',
    'paper', 'patent', 'patent_section', 'fm_drama', 'fs_drama', 'history', 'culture', 'enter',
    'c_event', 'news_r', 'briefing', 'his_cul', 'paper2', 'minute', 'edit', 'public', 'speech',
    'literature', 'narration', 'relationships', 'beauty_and_health', 'shopping', 'education',
    'food_and_drink', 'leisure', 'daily_and_occupation', 'housing_and_living', 'event',
    'life_science', 'artifact_science', 'nature_science'
]


dataset = load_dataset("wisenut-nlp-team/llama_ko_smr", data_subsets[0])['train']

# Iterate through the remaining subsets and concatenate them
for i in range(1, len(data_subsets)):
    new_dataset = load_dataset("wisenut-nlp-team/llama_ko_smr", data_subsets[i])['train']
    dataset = concatenate_datasets([dataset, new_dataset])



print(dataset)

# dataset_tech = load_dataset("wisenut-nlp-team/llama_ko_smr","technology_science")
# dataset_social = load_dataset("wisenut-nlp-team/llama_ko_smr","social_science")

# print(dataset_social['train'])
# print(dataset_tech['train'])
BASE_MODEL = "google/gemma-2b-it"

model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, device_map="auto", quantization_config=bnb_config)
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.padding_side = 'right'

#train_data = dataset_tech['train']+dataset_social['train']
#train_data = dataset['train']+dataset_social['train']

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    max_seq_length=512,
    args=TrainingArguments(
        output_dir="outputs",
#        num_train_epochs = 1,
        max_steps=3000,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        optim="paged_adamw_8bit",
        warmup_steps=int(3000 * 0.03),  # Converts 3% of 3000 to an integer
        learning_rate=2e-4,
        fp16=True,
        logging_steps=100,
        push_to_hub=False,
        report_to='none',
    ),
    peft_config=lora_config,
    formatting_func=generate_prompt,
)

trainer.train()


ADAPTER_MODEL = "lora_adapter"

trainer.model.save_pretrained(ADAPTER_MODEL)


#---------------------------------------------------------------------------------------

#SAVE MODEL

#BASE_MODEL = "google/gemma-2b-it"

ADAPTER_MODEL = "lora_adapter"

model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, device_map='auto', torch_dtype=torch.float16)
model = PeftModel.from_pretrained(model, ADAPTER_MODEL, device_map='auto', torch_dtype=torch.float16)

model = model.merge_and_unload()
model.save_pretrained('gemma-2b-it-sum-ko-science_v2')
