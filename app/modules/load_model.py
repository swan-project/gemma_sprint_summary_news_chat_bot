import asyncio
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
# 전역 변수로 모델과 토크나이저 선언
finetune_model = None
tokenizer = None
async def load_models():
    global finetune_model, tokenizer

    # Hugging Face 모델 설정
    BASE_MODEL = "google/gemma-2b-it"
    FINETUNE_MODEL = "swanii/gemma-2b-it-ko_science_summary"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if finetune_model is None or tokenizer is None:
        # 모델과 토크나이저 로드
        finetune_model = await asyncio.to_thread(AutoModelForCausalLM.from_pretrained, FINETUNE_MODEL)
        finetune_model.to(device)  # 모델을 GPU로 이동
        tokenizer = await asyncio.to_thread(AutoTokenizer.from_pretrained, BASE_MODEL)


    # # 모델과 토크나이저 로드
    # finetune_model = await asyncio.to_thread(AutoModelForCausalLM.from_pretrained, FINETUNE_MODEL)
    # finetune_model.to(device)  # 모델을 GPU로 이동
    # tokenizer = await asyncio.to_thread(AutoTokenizer.from_pretrained, BASE_MODEL)

    return await asyncio.to_thread(pipeline, "text-generation", model=finetune_model, tokenizer=tokenizer, max_new_tokens=512)