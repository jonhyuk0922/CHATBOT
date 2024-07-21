# -------------------------------------------------------------------------
# 참고: 이 코드의 일부는 다음 GitHub 리포지토리에서 참고하였습니다:
# https://github.com/lim-hyo-jeong/Wanted-Pre-Onboarding-AI-2407
# 해당 리포지토리의 라이센스에 따라 사용되었습니다.
# -------------------------------------------------------------------------

import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# 환경 변수에서 모델 로드 함수
def load_model(model_name: str) -> ChatOpenAI:
    """dotenv 로부터 key 저장하고, model_name 으로 모델 버전 받아와서 LLM 할당하여 반환합니다.

    Args:
        model_name (str): streamlit 에서 옵션으로 받아오는 모델 버전.

    Returns:
        ChatOpenAI: llm 모델 반환합니다.
    """
    load_dotenv()
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name=model_name)
    return llm 

# 캐릭터 이름에 따라 프롬프트 파일 로드 함수
def load_prompt(character_name: str) -> str:
    """받아온 캐릭터에 대한 사전정의 prompt 를 읽어옵니다.

    Args:
        character_name (str): streamlit 에서 옵션으로 받는 캐릭터명.

    Returns:
        str: 사전에 정의된 프롬프트 내용.
    """
    with open(f"prompts/{character_name}.prompt", "r", encoding="utf-8") as file:
        prompt = file.read().strip()  # 프롬프트 파일을 읽어옵니다.
    return prompt

# 메모리 설정 함수
def set_memory() -> ConversationBufferMemory:
    """ConversationBufferMemory 객체를 생성하고 반환합니다.

    Returns:
        ConversationBufferMemory: 메모리 키 'chat_history'로 설정되고 메시지를 반환하도록 구성된 ConversationBufferMemory 인스턴스.
    """
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True) # 대화 히스토리를 저장하는 메모리를 초기화합니다.

# 체인 초기화 함수
def initialize_chain(llm: ChatOpenAI, character_name: str, memory: ConversationBufferMemory) -> LLMChain:
    """
    주어진 LLM과 캐릭터 이름, 메모리를 기반으로 체인을 초기화합니다.

    Args:
        llm (ChatOpenAI): 사용할 언어 모델.
        character_name (str): 캐릭터의 이름.
        memory (ConversationBufferMemory): 대화 메모리.

    Returns:
        LLMChain: 초기화된 LLM 체인.
    """
    system_prompt = load_prompt(character_name) # 시스템 프롬프트를 로드합니다.
    custom_prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_prompt),  # 시스템 메시지 프롬프트를 설정합니다.

            MessagesPlaceholder(variable_name="chat_history"),   # 대화 히스토리를 위한 플레이스홀더를 설정합니다.
            HumanMessagePromptTemplate.from_template("{input}"),  # 사용자 입력을 위한 프롬프트를 설정합니다.
        ]
    )
    chain = LLMChain(llm=llm, prompt=custom_prompt, verbose=True, memory=memory)  # LLM 체인을 초기화합니다.
    return chain

# 메세지 생성 함수
def generate_message(chain: LLMChain, user_input: str) -> str:
    """
    사용자 입력을 기반으로 메시지를 생성합니다.

    Args:
        chain (LLMChain): 사용할 체인.
        user_input (str): 사용자의 입력.

    Returns:
        str: 생성된 응답 메시지.
    """
    result = chain({"input": user_input}) # 사용자 입력을 기반으로 결과를 생성합니다. 
    response_content = result["text"] # 결과에서 텍스트를 추출합니다.
    return response_content
