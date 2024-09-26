import asyncio

async def generate_title(doc, pipe_finetuned):
    # 메시지 생성 및 프롬프트 설정
    messages = [
        {
            "role": "user",
            "content": f"다음 글의 핵심을 잘 표현하는 세 단어로 된 제목을 만들어 주세요:\n\n{doc}"
        }
    ]
    prompt = pipe_finetuned.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # 모델을 사용한 텍스트 생성
    outputs = await asyncio.to_thread(pipe_finetuned, prompt, do_sample=True, temperature=0.2, top_k=50, top_p=0.95, add_special_tokens=True)
    
    print(outputs[0]["generated_text"][len(prompt):])

    return outputs[0]["generated_text"][len(prompt):]
