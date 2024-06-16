import streamlit as st
from PIL import Image

st.title("🙌 멀티모드")

st.write("멀티모드는 2인용으로 친구랑 같이 게임할 수 있어요! 먼저 정답을 맞춘 친구가 승리합니다. 먼저 두분의 이름을 각각 입력해 주세요")
st.write('')

one, two = st.columns(2)


if 'user1' not in st.session_state:
    st.session_state['user1'] = []

if 'user2' not in st.session_state:
    st.session_state['user2'] = []



with one:
    user1 = st.text_input("첫번째 친구의 이름:")
    if user1:
        if user1 not in st.session_state['user1']:
            st.session_state['user1'].append(user1)
        st.write(user1, '친구! 반가워요')
        
with two:
    user2 = st.text_input("두번째 친구의 이름:")
    if user2:
        if user2 not in st.session_state['user2']:
            if user1 != user2:
                st.session_state['user2'].append(user2)
                st.write(user2, "친구! 반가워요")
            else:
                st.warning('이름이 같아요! 다시 입력해주세요')

        

st.write('')

if st.session_state['user1'] and st.session_state['user2'] and (st.session_state['user1'][0] != st.session_state['user2'][0]):
    st.page_link("pages/page4-1.py", label="멀티 모드 스무고개 시작", icon="🎮")


st.page_link("home.py", label="홈으로 돌아가기", icon="🏠")