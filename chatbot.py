# -------------------------------------------------------------------------
# 참고: 이 코드의 일부는 다음 GitHub 리포지토리에서 참고하였습니다:
# https://github.com/lim-hyo-jeong/Wanted-Pre-Onboarding-AI-2407
# 해당 리포지토리의 라이센스에 따라 사용되었습니다.
# -------------------------------------------------------------------------

# Streamlit 라이브러리 및 기타 필요한 라이브러리 임포트
import streamlit as st
import time
from langchain_core.messages import HumanMessage, AIMessage
from utils import load_model, set_memory, initialize_chain, generate_message

# 애플리케이션 제목 설정
st.title("페르소나 챗봇")
st.markdown("<br>", unsafe_allow_html=True)  # 브라우저에 줄 바꿈을 삽입합니다.

<<<<<<< HEAD
# 사용자로부터 캐릭터를 선택받기 위한 드롭다운 메뉴 설정
character_name = st.selectbox(
    "**캐릭터를 골라줘!**",
    ("baby_shark", "one_zero"),
    index=0,
    key="character_name_select",
)
# 선택된 캐릭터 이름을 세션 상태에 저장
st.session_state.character_name = character_name

# 사용자로부터 모델을 선택받기 위한 드롭다운 메뉴 설정
model_name = st.selectbox(
    "**모델을 골라줘!**",
    ("gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"),
    index=0,
    key="model_name_select",
)
# 선택된 모델 이름을 세션 상태에 저장
=======
character_name = st.selectbox("**캐릭터를 골라줘!**", 
                              ("baby_shark", "one_zero"), 
                              index=0, 
                              key="character_name_select")

st.session_state.character_name = character_name

model_name = st.selectbox("**모델을 골라줘!**", 
                          ("gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"), 
                          index=0, 
                          key="model_name_select")

>>>>>>> parent of dfc07c7 (🎨Ref/black formatting chatbot.py)
st.session_state.model_name = model_name

# 세션 상태에서 채팅 시작 여부를 확인 및 초기화
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
    st.session_state.memory = None
    st.session_state.chain = None

<<<<<<< HEAD

# 채팅을 시작하는 함수 정의
def start_chat():
    llm = load_model(st.session_state.model_name)  # 선택된 모델을 로드합니다.
    st.session_state.chat_started = True  # 채팅 시작 상태를 True로 설정합니다.
    st.session_state.memory = set_memory()  # 메모리를 초기화합니다.
    st.session_state.chain = initialize_chain(
        llm, st.session_state.character_name, st.session_state.memory
    )  # 체인을 초기화합니다.

=======
def start_chat() -> None:
    """
    선택된 모델과 캐릭터를 기반으로 채팅을 시작합니다.
    """
    llm = load_model(st.session_state.model_name)
    st.session_state.chat_started = True
    st.session_state.memory = set_memory()
    st.session_state.chain = initialize_chain(llm, st.session_state.character_name, st.session_state.memory)
>>>>>>> parent of dfc07c7 (🎨Ref/black formatting chatbot.py)

# "Start Chat" 버튼을 클릭했을 때 start_chat 함수를 호출
if st.button("Start Chat"):
    start_chat()

st.markdown("<br>", unsafe_allow_html=True)  # 브라우저에 줄 바꿈을 삽입합니다.

# 채팅이 시작된 경우
if st.session_state.chat_started:
    if st.session_state.memory is None or st.session_state.chain is None:
        start_chat()  # 메모리나 체인이 초기화되지 않은 경우 다시 초기화합니다.

    # 메모리에 저장된 모든 메시지를 화면에 표시
    for message in st.session_state.memory.chat_memory.messages:
        if isinstance(message, HumanMessage):
            role = "user"  # HumanMessage는 "user" 역할로 설정
        elif isinstance(message, AIMessage):
            role = "assistant"  # AIMessage는 "assistant" 역할로 설정
        else:
            continue
        with st.chat_message(role):  # 해당 역할로 메시지를 화면에 표시
            st.markdown(message.content)

    # 사용자가 입력한 새로운 메시지를 처리
    if prompt := st.chat_input():
        with st.chat_message("user"):  # 사용자 메시지를 화면에 표시
            st.markdown(prompt)

        with st.chat_message("assistant"):  # AI 응답을 화면에 표시
            message_placeholder = st.empty()  # 응답을 표시할 자리 확보
            full_response = ""
            response_content = generate_message(
                st.session_state.chain, prompt
            )  # AI 응답 생성

            # 응답을 단어 단위로 나누어 점진적으로 화면에 표시
            for chunk in response_content.split():
                full_response += chunk + " "
<<<<<<< HEAD
                time.sleep(0.05)  # 각 단어 사이에 지연을 추가하여 애니메이션 효과
                message_placeholder.markdown(full_response + "▌")  # 진행 중 표시
            message_placeholder.markdown(full_response.strip())  # 최종 응답 표시
=======
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
>>>>>>> parent of dfc07c7 (🎨Ref/black formatting chatbot.py)
