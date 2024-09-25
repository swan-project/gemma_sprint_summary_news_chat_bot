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