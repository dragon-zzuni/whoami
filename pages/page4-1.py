import streamlit as st
import speech_recognition as sr
import pyttsx3
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from pages.page4 import user1, user2

# Vertex AI 초기화
vertexai.init(project="gen-lang-client-0723754498", location="asia-northeast3")

# 모델 생성
model = GenerativeModel(
    "gemini-1.5-pro-001",
    system_instruction=[
        """스무고개 게임 - 게임 마스터 가이드 🎮 
        역할: 스무고개 게임의 게임 마스터
        목표: 스무고개 게임의 게임 마스터가 되어 사용자로 하여금 질문을 하여 정답을 유추하게 도와주기
        🤖 gemini 지침: 
        상호 작용 시작: 
        - 친절한 인사로 시작합니다. 
        - 사용자에게 스무고개 게임을 하고 싶은지 물어봅니다. 
        규칙 설명: 
        - 스무고개 게임의 규칙을 간략히 설명합니다. 
        - 예를 들어 사용자의 기대를 명확하게 설정합니다.
        - 또한 초반에 유리한 질문 몇개를 샘플로 알려줍니다.
        - 두명의 사용자가 게임을 진행합니다.
        - 번갈아 가면서 질문을 합니다.
        - 정답을 먼저 맞춘 사용자는 점수를 얻고 게임을 종료합니다.
        - 점수를 3점 먼저 얻는 사용자가 승리합니다.
        - gemini는 두 명의 사용자에게 문제를 제시하는 역할입니다.
        - gemini는 두 명의 사용자에게 각각 문제를 제시하고 설명합니다.
        - 사용자가 번갈아가면서 질문하지 않으면 경고를 하고 번갈아가면서 질문할 수 있게 합니다.
        카테고리 :
        -주제는 동물입니다.
        -사용자가 질문하기 전 랜덤으로 한 동물을 생각합니다. 비교적 보편적인 동물이면 좋습니다.
        질문 루프: 
        - 카테고리 에 명시된 동물로 사용자가 질문을 시작합니다.
        - 꼭 예 와 아니오 가 아니더라도 최대한 답변해줍니다.
        - 사용자가 명확하지 않거나 이탈하는 답변을 할 경우, 그에 적절히 대응합니다. 
        전략 조정: 
        - 정답을 여러번 틀릴 경우 힌트를 줍니다.
        카운트 유지: 
        - 각 질문 후에 현재 질문 번호와 남은 질문 수를 사용자에게 알립니다. 
        최종 추측: 
        - 20번의 질문이 끝나거나 더 일찍 추측을 하여 정답을 맞춘 경우 축하 메시지와 함께 초기화 이후 재시작을 묻습니다.
        -틀렸을경우 정답을 알려주고 초기화 이후 재시작을 묻습니다.   
        결과 및 피드백: 
        - 사용자에게 실제 답을 공개하고 만약 틀렸을 경우 얼마나 가까웠는지 피드백을 줍니다. 
        재시작 옵션: 
        - 게임을 다시 시작하거나 종료할지 사용자에게 물어봅니다. 
        상호 작용 종료: 
        - 이겼다면 축하의 인사를 건냅니다.
        - 게임에 참여해 주셔서 감사하다는 말을 합니다. 
        - 게임 개선을 위한 피드백을 요청합니다. """
    ]
)

# 생성 설정
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# 안전 설정
safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# 텍스트를 음성으로 변환하는 함수
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# 음성 입력을 얻는 함수
def get_audio_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    # Google 음성 인식을 사용하여 음성 인식
    try:
        return r.recognize_google(audio, language='ko')
    except sr.UnknownValueError:
        st.error("오디오를 이해하지 못했습니다. 다시 시도해 주세요.")
        return None
    except sr.RequestError:
        st.error("음성 인식 서비스에 접근할 수 없습니다.")
        return None

# 대화 기록 출력 함수
def display_chat_history(container, chat_history, last_tts_index_key):
    if last_tts_index_key not in st.session_state:
        st.session_state[last_tts_index_key] = -1

    with container:
        for i, message in enumerate(chat_history):
            with st.chat_message(message["role"]):
                st.markdown(message["message"])
            if message["role"] == "🤖" and i > st.session_state[last_tts_index_key]:
                text_to_speech(message["message"])
                st.session_state[last_tts_index_key] = i

# 스트림릿 애플리케이션
def main():
    st.title(":cat: 스무고개")
    st.header("주제는 동물입니다.")
    st.write("먼저 3번 맞춘 친구가 승리합니다!")
    st.write("질문은 번갈아 해주세요!")
    st.warning("질문이 끝났으면 다음 친구가 진행할 수 있게 입력한 것을 항상 지워주세요")

    if "chat_history1" not in st.session_state:
        st.session_state.chat_history1 = []
    if "chat_history2" not in st.session_state:
        st.session_state.chat_history2 = []

    if "chat_session1" not in st.session_state:
        st.session_state.chat_session1 = model.start_chat(history=[])
        initial_response1 = st.session_state.chat_session1.send_message(
            "안녕하세요!",
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=True,
        )
        response_text1 = "".join([part.text for part in initial_response1])
        st.session_state.chat_history1.append({"role": "🤖", "message": response_text1})

    if "chat_session2" not in st.session_state:
        st.session_state.chat_session2 = model.start_chat(history=[])
        initial_response2 = st.session_state.chat_session2.send_message(
            "안녕하세요!",
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=True,
        )
        response_text2 = "".join([part.text for part in initial_response2])
        st.session_state.chat_history2.append({"role": "🤖", "message": response_text2})

    user1_talk, user2_talk = st.columns([0.5, 0.5])

    # 사용자 1의 입력 처리 (텍스트 및 음성)
    with user1_talk:
        # 대화 내용을 담을 컨테이너
        chat_container1 = st.container()
        st.write("사용자 1 진행할 방식을 선택해주세요.")
        user1_input_type = st.radio("입력 방식:", ("음성", "텍스트"), key="user1_input_type")

        user_input1 = None
        if user1_input_type == "음성":
            if st.button("마이크 켜기", key="mic_button_speech1"):  # 음성 입력 버튼
                user_input1 = get_audio_input()
                if user_input1:
                    st.session_state.chat_history1.append({"role": f"{user1}", "message": user_input1})
        else:
            user_input1 = st.text_input("사용자1 질문:", key="text_input1")
            if user_input1:
                st.session_state.chat_history1.append({"role": f"{user1}", "message": user_input1})

        if user_input1:
            # 챗봇 응답 생성
            ai_response1 = st.session_state.chat_session1.send_message(user_input1)
            st.session_state.chat_history1.append({"role": "🤖", "message": ai_response1.text})

        # 사용자 1의 대화 기록 출력
        display_chat_history(chat_container1, st.session_state.chat_history1, "last_tts_index1")

        if 'count1' not in st.session_state:
            st.session_state.count1 = 0
        st.write('승리했다면 버튼을 한 번 눌러주세요!')
        increment1 = st.button('점수획득!', key='increment1')

        if increment1:
            st.session_state.count1 += 1
            st.write("점수 : ", st.session_state.count1)
            if st.session_state.count1 >= 3:
                st.session_state.count1 = 0  # 점수 초기화
                st.session_state.count2 = 0  # 점수 초기화
                st.write('축하합니다! 승리했어요')
                st.page_link('pages/page4.py', label='다시시작하기', icon='🎮')

    # 사용자 2의 입력 처리 (텍스트 및 음성)
    with user2_talk:
        # 대화 내용을 담을 컨테이너
        chat_container2 = st.container()
        st.write("사용자 2 진행할 방식을 선택해주세요.")
        user2_input_type = st.radio("입력 방식:", ("음성", "텍스트"), key="user2_input_type")

        user_input2 = None
        if user2_input_type == "음성":
            if st.button("마이크 켜기", key="mic_button_speech2"):  # 음성 입력 버튼
                user_input2 = get_audio_input()
                if user_input2:
                    st.session_state.chat_history2.append({"role": f"{user2}", "message": user_input2})
        else:
            user_input2 = st.text_input("사용자2 질문:", key="text_input2")
            if user_input2:
                st.session_state.chat_history2.append({"role": f"{user2}", "message": user_input2})

        if user_input2:
            # 챗봇 응답 생성
            ai_response2 = st.session_state.chat_session2.send_message(user_input2)
            st.session_state.chat_history2.append({"role": "🤖", "message": ai_response2.text})

        # 사용자 2의 대화 기록 출력
        display_chat_history(chat_container2, st.session_state.chat_history2, "last_tts_index2")

        if 'count2' not in st.session_state:
            st.session_state.count2 = 0
        st.write('승리했다면 버튼을 한 번 눌러주세요!')
        increment2 = st.button('점수획득!', key='increment2')

        if increment2:
            st.session_state.count2 += 1
            st.write("점수 : ", st.session_state.count2)
            if st.session_state.count2 >= 3:
                st.session_state.count1 = 0  # 점수 초기화
                st.session_state.count2 = 0  # 점수 초기화
                st.write('축하합니다! 승리했어요')
                st.page_link('pages/page4.py', label='다시시작하기', icon='🎮')

    st.page_link("home.py", label="홈으로 돌아가기", icon="🏠")

if __name__ == "__main__":
    main()
