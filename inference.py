from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline, TrainingArguments

from peft import LoraConfig, PeftModel
from trl import SFTTrainer
import torch

BASE_MODEL = "google/gemma-2b-it"
FINETUNE_MODEL = "./gemma-2b-it-sum-ko-science"

finetune_model = AutoModelForCausalLM.from_pretrained(FINETUNE_MODEL, device_map={"":0})
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

pipe = pipeline("text-generation", model=finetune_model, tokenizer=tokenizer, max_new_tokens=512)

pipe_finetuned = pipeline("text-generation", model=finetune_model, tokenizer=tokenizer, max_new_tokens=512)
#doc = dataset['train']['input'][10]

doc=None
doc = r"그렇게 등장한 것이 원자시계다. 원자가 1초 동안 움직이는 횟수인 ‘고유진동수’를 이용해 정확한 1초를 측정한다. 원자 속에 있는 전자들은 특정 에너지 상태로 있다. 이 상태에서 다른 상태로 변화하려면 에너지를 두 상태의 차이만큼 흡수하거나 방출해야 한다. 전자가 에너지를 얻기 위해(다른 에너지 상태로 변하기 위해) 전자기파를 흡수할 때 진동이 발생하는데, 이것이 바로 고유진동수다."
#doc = r"천년만년 지나도 변하지 않는 곳이 있을까. 과학자들은 천년만년을 넘어 수억 년이 지나도 1초의 오차도 없이 일정하게 흐르는 시계를 개발하고 있다. 지구가 한 바퀴 자전하는 시간을 1일이라고 한다. 이것을 쪼개 시간과 분, 초를 정했다. 하지만 지구 자전 속도는 시간에 따라 변하므로 시간에 오차가 생겼다. 새로운 시간의 정의가 필요해진 이유다."
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