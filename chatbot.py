# -------------------------------------------------------------------------
# 참고: 이 코드의 일부는 다음 GitHub 리포지토리에서 참고하였습니다:
# https://github.com/lim-hyo-jeong/Wanted-Pre-Onboarding-AI-2407
# 해당 리포지토리의 라이센스에 따라 사용되었습니다.
# -------------------------------------------------------------------------

import streamlit as st
import time
from typing import Optional
from langchain_core.messages import HumanMessage, AIMessage
from utils import load_model, set_memory, initialize_chain, generate_message
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

st.title("페르소나 챗봇")
st.markdown("<br>", unsafe_allow_html=True)

character_name = st.selectbox("**캐릭터를 골라줘!**", 
                              ("baby_shark", "one_zero"), 
                              index=0, 
                              key="character_name_select")

st.session_state.character_name = character_name

model_name = st.selectbox("**모델을 골라줘!**", 
                          ("gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"), 
                          index=0, 
                          key="model_name_select")

st.session_state.model_name = model_name

if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
    st.session_state.memory = None
    st.session_state.chain = None

def start_chat() -> None:
    """
    선택된 모델과 캐릭터를 기반으로 채팅을 시작합니다.
    """
    llm = load_model(st.session_state.model_name)
    st.session_state.chat_started = True
    st.session_state.memory = set_memory()
    st.session_state.chain = initialize_chain(llm, st.session_state.character_name, st.session_state.memory)

if st.button("Start Chat"):
    start_chat()

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.chat_started:
    if st.session_state.memory is None or st.session_state.chain is None:
        start_chat()

    for message in st.session_state.memory.chat_memory.messages:
        if isinstance(message, HumanMessage):
            role = "user"
        elif isinstance(message, AIMessage):
            role = "assistant"
        else:
            continue
        with st.chat_message(role):
            st.markdown(message.content)

    if prompt := st.chat_input():
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            response_content = generate_message(st.session_state.chain, prompt)

            for chunk in response_content.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response.strip())


def load_model(model_name: str) -> ChatOpenAI:
    """
    주어진 모델 이름을 기반으로 ChatOpenAI 모델을 로드합니다.

    Args:
        model_name (str): 사용할 모델의 이름.

    Returns:
        ChatOpenAI: 로드된 ChatOpenAI 모델.
    """
    load_dotenv()
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name=model_name)
    return llm 


def load_prompt(character_name: str) -> str:
    """
    캐릭터 이름에 따라 프롬프트 파일을 로드합니다.

    Args:
        character_name (str): 캐릭터의 이름.

    Returns:
        str: 로드된 프롬프트 내용.
    """
    with open(f"prompts/{character_name}.prompt", "r", encoding="utf-8") as file:
        prompt = file.read().strip()
    return prompt


def set_memory() -> ConversationBufferMemory:
    """
    대화 히스토리를 저장하기 위한 메모리를 설정합니다.

    Returns:
        ConversationBufferMemory: 초기화된 대화 메모리.
    """
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)


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
    system_prompt = load_prompt(character_name)
    custom_prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )
    chain = LLMChain(llm=llm, prompt=custom_prompt, verbose=True, memory=memory)
    return chain


def generate_message(chain: LLMChain, user_input: str) -> str:
    """
    사용자 입력을 기반으로 메시지를 생성합니다.

    Args:
        chain (LLMChain): 사용할 체인.
        user_input (str): 사용자의 입력.

    Returns:
        str: 생성된 응답 메시지.
    """
    result = chain({"input": user_input})
    response_content = result["text"]
    return response_content
