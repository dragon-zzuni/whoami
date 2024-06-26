import datetime
import streamlit as st
from tkinter.tix import COLUMN
from pyparsing import empty
from PIL import Image
#from streamlit_custom_sidebar import CustomSidebarDefault


#CustomSidebarDefault(showSidebarNavigation=False)

st.title(' 🤔 :red[상상력] 증진 프로그램')

#with st.sidebar:
#    messages = st.container(height=300)
#    if prompt := st.chat_input("'도움말' 을 입력하여 물어보세요."):
#        messages.chat_message("😛").write(prompt)
#        messages.chat_message("😺").write(f"이 프로그램은 영유아 대상으로 만들어진 프로그램이며 왼쪽의 탭이나 아래의 링크를 통해 스무고개와 씨앗 키우기를 이용할 수 있습니다. ")


#st.markdown(
#    """
#    <style>
#    [data-testid="stSidebar"]{
#        visibility: hidden;
#    }
#    </style>
#    """, 
#    unsafe_allow_html=True
#)

with st.sidebar:
    messages = st.container(height=300)
    if prompt := st.chat_input("'도움말' 을 입력하여 물어보세요."):
        messages.chat_message("😛").write(prompt)
        messages.chat_message("😺").write(f"이 프로그램은 영유아 대상으로 만들어진 프로그램이며 왼쪽의 탭이나 아래의 링크를 통해 스무고개와 씨앗 키우기를 이용할 수 있습니다. ")


if 'name' not in st.session_state:
    st.session_state['name'] = []


name = st.text_input('사용자 이름을 입력해 주세요')
if not name:
    #st.warning('이름을 입력해주세요!')
    st.stop()
st.success('입력 완료!')

st.write('적정 사용자 연령은 5~8세 입니다.:boy: :girl:')
#st.slider(" 적정 사용자 연령은 5~8세 입니다.:boy: :girl:", 0,40,(5,8))

# Get birthdate
birthdate = st.date_input("생일을 입력해 주세요", value=None)

# Calculate age
if birthdate is not None:
    today = datetime.date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    # Check if age is within the valid range
    if age is not None and 5 <= age <= 8:
        st.success('입력 완료! {}님의 나이는 {}살이며, 적정 연령입니다. \n 진행하려는 프로그램을 눌러주세요!'.format(name, age))
        
    elif age<5:
        st.warning('입력 완료! {}님의 나이는 {}살이며, 적정 연령 범위 (5~8세)를 벗어납니다.'.format(name, age))
        st.warning('부모님의 도움이 필요할거 같아요! 같이 게임을 진행해 주세요')
    else:
        st.warning('입력 완료! {}님의 나이는 {}살이며, 적정 연령 범위 (5~8세)를 벗어납니다.'.format(name, age))
        st.warning('게임이 조금은 쉬울 수 있어요. 그래도 진행하려면 진행하려는 프로그램을 선택해주세요!')
else:
    age = None




st.page_link("home.py", label="홈", icon="🏠")
st.page_link("pages/page2.py", label="스무고개", icon="✏️")
st.page_link('pages/page4.py', label='스무고개 멀티모드', icon='🎮')
#st.page_link("pages/page1.py", label="씨앗 키우기", icon="🌱")
