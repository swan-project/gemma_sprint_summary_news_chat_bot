import asyncio
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

import torch
async def load_models():
    # Hugging Face 모델 설정
    BASE_MODEL = "google/gemma-2b-it"
    FINETUNE_MODEL = "swanii/gemma-2b-it-ko_science_summary"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 모델과 토크나이저 로드
    finetune_model = await asyncio.to_thread(AutoModelForCausalLM.from_pretrained, FINETUNE_MODEL)
    finetune_model.to(device)  # 모델을 GPU로 이동
    tokenizer = await asyncio.to_thread(AutoTokenizer.from_pretrained, BASE_MODEL)

    return await asyncio.to_thread(pipeline, "text-generation", model=finetune_model, tokenizer=tokenizer, max_new_tokens=512)

async def summarize_text(doc, pipe_finetuned):
    # 메시지 생성 및 프롬프트 설정
    messages = [
        {
            "role": "user",
            "content": f"다음 글을 자새하 세부적으로 요약해주세요:\n\n{doc}"
        }
    ]
    prompt = pipe_finetuned.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # 모델을 사용한 텍스트 생성
    outputs = await asyncio.to_thread(pipe_finetuned, prompt, do_sample=True, temperature=0.2, top_k=50, top_p=0.95, add_special_tokens=True)
    
    print(outputs[0]["generated_text"][len(prompt):])

    return outputs[0]["generated_text"][len(prompt):]

# async def summarize_text(doc):
#     pipe_finetuned = await load_models()
#     summary = await summarize(doc, pipe_finetuned)
#     return summary