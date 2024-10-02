# Gemma LLM Model Fine-Tuning for Technical Summarization Chat Bot

The Gemma LLM model is being fine-tuned specifically for use in a technical summarization chatbot. This chatbot will leverage the model's ability to understand and summarize complex technical content, making it easier for users to engage with technical materials. The fine-tuning process is aimed at improving the model's performance in accurately capturing the essential points from dense, technical information, and providing concise, user-friendly summaries. The end goal is to enhance user experience in environments where quick, reliable technical insights are required.

## Table of Contents

1. [ Dataset ](#dataset)
2. [ Model ](#model)
3. [ Project Structure ](#project-structure)
4. [ App ](#app)
5. [_Demo_](#demo)

## Dataset

The dataset used for this project is sourced from the Hugging Face repository, specifically from the [wisenut-nlp-team/llama_ko_smr](https://huggingface.co/datasets/wisenut-nlp-team/llama_ko_smr) collection. This dataset contains various types of summarization data, including document summaries, book summaries, research paper summaries, TV content script summaries, Korean dialogue summaries, and technical/scientific summaries. Each entry in the dataset consists of the instruction, main text, and its corresponding summary.

Instead of limiting the training to just the technical and scientific summarization data, I opted to use the entire dataset to expose the model to a wider variety of content types. This decision was made to ensure the model is well-rounded and can handle diverse types of summarization tasks, improving its overall performance across different domains.

Here is an example of the dataset:

```json
{
  "instruction": "이 글의 주요 내용을 짧게 설명해 주실 수 있습니까?",
  "input": "북한 연극에 대한 나의 탐구는 해방공간에 북으로 사라져 간 수많은 연극인들의 행적을 찾아보고자 하는 단순한 호기심에서 시작되었다. 해방공간에서 활동하던 연극인의 대다수가 납․월북의 과정을 거쳐 북한 연극계에 자리를 잡았기 때문이다. 그 안에는 극작가 송영, 함세덕, 박영호, 조영출, 연출가 이서향, 안영일, 신고송, 무대미술가 김일영, 강호, 배우 황철, 김선영, 문예봉, 만담가 신불출 등 기라성 같은 멤버들이 포함되어 있었다. 그 숫자로만 본다면 일제강점기 서울의 연극계가 통으로 평양으로 옮겨간 셈이었다. 그렇지만 이제 북한 연극에서 더 이상 그들의 존재를 확인하기 어려운 상황이다. 그들은 남에서도 북에서도 시계에서 영원히 사라져버린 ‘잃어버린 세대’ 그 자체이다. 그들의 흔적을 찾는 것은 차라리 고고학의 과제가 되었다. 그들이 역사의 저편으로 사라진 그 자리에 오늘의 북한 연극이 성채처럼 위용을 자랑하고 있다. 오늘날의 북한 연극은 모두가 주체사실주의에 입각하여 만들어지는 이른바 ‘<성황당>식 혁명연극’ 일색이다. 1978년 국립연극단의 <성황당> 공연의 성과를 본보기로 삼아 모든 연극이 ‘따라 배우기’를 하고 있기 때문이다. 북한의 연극과 희곡은 정점에서 내려 쏟는 단성적(單聲的) 문화회로 안에 갇혀 있다. 혁명연극 <성황당>(1978)의 본보기는 혁명가극 <피바다>(1971)이며, 그 근저에는 1960년대부터 시작된 김정일 주도의 문화예술혁명이 가로놓여 있다. 북한 연극의 창작과 향유, 그 모든 과정에서 김정일의 그림자에 맞닥뜨리지 않을 수 없다. 최근에 방문한 조선예술영화촬영소 에 있는 ‘문화성혁명사적관’(김정일관)에는 1960년대 중반부터 2000년대까지 40년 동안 김정일의 문화예술 부문 지도가 11,890건이며, 그 중 문화예술기관을 직접 방문하여 지도한 이른바 ‘현지지도’가 1,770건이라는 안내판이 있었다. 북한 연극이 김정일과 주체사상이라는 키워드를 떠나 존재할 수 없다는 것을 단적으로 말해 준다.",
  "output": "해방공간에서 활동한 대다수의 연극인은 납·월북을 통해 북한 연극계에 자리 잡았지만 이제 북한 연극에서 그들을 보기 어렵다. 그 자리에 지금 북한 연극이 자리 잡았다. 1978년 국립연극단 <성황당> 공연을 토대로 북한의 모든 연극은 ‘<성황당>식 혁명연극’ 일색이다. 북한 연극과 희곡은 단성적 문화회로에 묶여있고, 그 시작은 김정일 주도 문화예술혁명이 있고, 북한 연극의 창작과 향유 등 김정일 흔적이 있다. 김정일의 문화예술 부문 지도 기록은 북한 연극이 김정일과 주체사상을 떠날 수 없는 것을 보여준다."
}
```

## Model

This model is built on the gemma-2-2b-it base and fine-tuned using advanced techniques such as BitsAndBytes for memory optimization, LoRA for efficient adaptation, and the SFTTrainer framework. You can find the fine-tuned version of this model on Hugging Face at this link.

### Highlight

1. **LoRA Configuration for Model Efficiency**: The model is fine-tuned using Low-Rank Adaptation (LoRA) with specific configurations like r=6, lora_alpha=8, and a dropout of 0.05. This allows for efficient adaptation of the model without modifying all layers.

2. **Quantization for Memory Optimization**: The BitsAndBytesConfig is set to load the model in 4-bit precision, using nf4 quantization. This reduces memory usage, making it possible to fine-tune the model on larger datasets.

3. **Fine-Tuning Parameters**: Fine-tuning is set up using SFTTrainer, with a batch size of 1, gradient_accumulation_steps=4, and max_steps=3000. The training uses 8-bit AdamW optimizer (paged_adamw_8bit) for better performance in a memory-constrained environment.

### Example

**input**

```
그렇게 등장한 것이 원자시계다. 원자가 1초 동안 움직이는 횟수인 ‘고유진동수’를 이용해 정확한 1초를 측정한다. 원자 속에 있는 전자들은 특정 에너지 상태로 있다. 이 상태에서 다른 상태로 변화하려면 에너지를 두 상태의 차이만큼 흡수하거나 방출해야 한다. 전자가 에너지를 얻기 위해(다른 에너지 상태로 변하기 위해) 전자기파를 흡수할 때 진동이 발생하는데, 이것이 바로 고유진동수다.
```

**output**

```
원자시계는 원자가 1초 동안 움직이는 횟수인 고유진동수를 이용해 정확한 1초를 측정한다.
```

## Project Structure

```
gemma_sprint_summary_news_chat_bot/
├── app/
│   ├── assets
│   ├── components
│   ├── constants
│   ├── modules
│   ├── local_storage.json
│   ├── main.py
│   └── requirements.txt
├── train/
│   ├── test
│   │    └── basic_model_inference.py
│   └── train.py
├── inference.py
└── README.md
```

## App

### About The App

TechSum is a user-friendly application designed to simplify the process of summarizing articles and text. By inputting a link from the ScienceTimes website, TechSum automatically retrieves the article and generates a concise summary. Users can also paste their own text to receive a quick summary. Additionally, TechSum allows users to save these summaries locally for easy reference. The app streamlines access to key information, making it a convenient tool for anyone seeking quick insights from technical articles or lengthy texts.

You can visit the website using this [link](https://techsum.store/)

### Getting Started

1. Clone the repo

```
git clone https://github.com/swan-project/gemma_sprint_summary_news_chat_bot.git
```

2. Move to app directory

```
cd app
```

3. Install required pacakges

```
pip install -r requirements.txt
```

4. Add huggingface token in env file

```
HUGGINGFACE_TOKEN=YourKey
```

5. Run Flet App

```
flet run
```

## Demo

https://github.com/user-attachments/assets/9ab61bcd-4174-4696-a2bd-9799ba0f867d
