import streamlit as st
from openai import OpenAI
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import random
import json

# API KEY, THREAD, client 생성
api_keys = st.secrets["api"]["keys"]
selected_api_key = random.choice(api_keys)
client = OpenAI(api_key=selected_api_key)
assistant_id = 'asst_2FrZmOonHQCPO6EhXzQ6u3nr'
new_thread = client.beta.threads.create()

# 화면 페이키 크기 설정
st.set_page_config(layout="wide")

# 전체 제목
st.header(':memo:서술형 평가 설정 페이지')

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state['page'] = 0
if 'settingname' not in st.session_state:
    st.session_state['settingname'] = ''
if 'question1' not in st.session_state:
    st.session_state['question1'] = ''
if 'question2' not in st.session_state:
    st.session_state['question2'] = ''
if 'question3' not in st.session_state:
    st.session_state['question3'] = ''
if 'correctanswer1' not in st.session_state:
    st.session_state['correctanswer1'] = ''
if 'correctanswer2' not in st.session_state:
    st.session_state['correctanswer2'] = ''
if 'correctanswer3' not in st.session_state:
    st.session_state['correctanswer3'] = ''
if 'feedbackinstruction' not in st.session_state:
    st.session_state['feedbackinstruction'] = ''

# 페이지 전환 함수 정의
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

def go_home():
    st.session_state.page = 0

# 홈 
def home():
    with st.container(border=True):
            st.write("""
            서술형 평가 설정 페이지 사용 방법
                     
            총 4단계로 이루어져 있습니다. 각 단계에 필요한 내용을 입력하고 다음 단계로 넘어가주세요.""")

            st.info("""1. [평가 코드 만들기]:
- 선생님이 만든 서술형 평가의 평가 코드를 만든 뒤 등록 버튼을 눌러주세요.
- 평가 코드는 학생 페이지에서 선생님이 만든 평가를 불러오는 데 사용됩니다.""")
                     
            st.success("""2. [자료 입력하기]: 
- 서술형 평가에 활용할 수 있는 자료를 입력해 주세요. 
- 교과서 pdf, 수업 자료 pdf 등을 입력할 수 있습니다. 
- 입력한 자료를 근거로 모범 답안을 생성하거나 학생 답안을 채점할 수 있습니다.""")

            st.error("""3. [평가 문항 및 주의사항 입력하기]: 
- 서술형 평가 문항과 모범답안(선택 사항)을 입력해 주세요. 
- 서술형 평가 문항은 최대 3개까지 입력 가능합니다. 
- 평가 주의사항을 입력할 수 있습니다.
- 입력한 평가 주의사항을 근거로 채점 및 피드백을 생성할 수 있습니다.""")

            st.warning("""4. [평가 확인 및 저장하기]: 
- 선생님이 만든 서술형 평가를 확인하고 저장합니다. 
- 수정이 필요하다면 수정이 필요한 부분으로 돌아가서 다시 입력한 다음 저장합니다.""")

    st.button("다음 단계", on_click=next_page)

# 1단계
def step1():
    st.subheader("1단계. 평가 코드 만들기")
    st.info("선생님이 만든 평가를 찾기 위한 평가 코드를 만들어주세요. 학생 페이지에서 선생님이 만든 평가를 불러오는 데 사용됩니다. 예를 들어 [고조선은 어떤 나라였을까요], [240907], [A-1] 처럼 다양하게 만들 수 있습니다.")

# 평가 이름 입력
    with st.container(border=True):
        st.caption("평가 코드")
        settingname = st.text_input("평가 코드를 만들어주세요.")

# 평가 이름 등록        
        settingnameinput = st.button("평가 코드 등록하기")
        if settingnameinput:
            st.session_state['settingname'] = settingname
            st.session_state['api_key'] = selected_api_key
            st.session_state['usingthread'] = new_thread.id
            st.success("평가 코드가 성공적으로 등록되었습니다.")

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.button("이전 단계", on_click=prev_page)

    with col2:
        st.button("다음 단계", on_click=next_page, disabled=not bool(st.session_state['settingname']))
    
    with col3:
        st.button("처음 화면으로", on_click=go_home) 

# 2단계
def step2():
    st.subheader("2단계. 자료 입력하기")
    st.success("서술형 평가에 활용할 자료를 입력해 주세요. 교과서 pdf, 수업 자료 pdf 등을 입력할 수 있습니다. 입력한 자료를 근거로 모범 답안이나 피드백을 생성할 수 있습니다.")

# 자료 등록
    with st.container(border=True):
        st.caption("자료")
        uploaded_file = st.file_uploader("", label_visibility="collapsed")
        run_file_button = st.button('자료 등록하기')

        if uploaded_file is not None and run_file_button:
            uploaded_file_response = client.files.create(
                file=uploaded_file,
                purpose="assistants")

            vector_store_file = client.beta.vector_stores.files.create(
                vector_store_id='vs_FtRt7SEalipabRPrOk0usxl8',
                file_id=uploaded_file_response.id)
            
            st.success("자료가 성공적으로 등록되었습니다.")

# 등록된 자료 확인
        filelist = st.checkbox("등록된 자료 목록(확인 후에는 체크 박스를 해제 해주세요.)")
        
        if filelist:
            client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='vs_FtRt7SEalipabRPrOk0usxl8을 file search합니다. vs_FtRt7SEalipabRPrOk0usxl8에 있는 파일 목록을 오름차순으로 정리합니다. 파일 이름은 파일 확장자 부분을 제거한 다음 한 줄에 하나씩 줄 바꿈해서 제시합니다. 다른 문장은 넣지 말고 파일 이름만 제시합니다. 5번 이상 반복적으로 file search한 다음 제시합니다. 분명히 있을 거니까 꼭 찾아보고 알려주세요.')
            
            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id)
            
            run_id = run.id

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run_id)
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)
                    
            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            msg = thread_messages.data[0].content[0].text.value
            st.text(msg)

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.button("이전 단계", on_click=prev_page)

    with col2:
        st.button("다음 단계", on_click=next_page)
    
    with col3:
        st.button("처음 화면으로", on_click=go_home) 

# 단계 3
def step3():
    st.subheader("3단계. 평가 문항 및 주의사항 입력하기")
    st.error("서술형 평가 문항과 모범답안(선택 사항)을 입력하세요. 최대 3개 문항까지 입력 가능합니다. 모범답안의 경우 선택 사항으로 모범답안을 입력하지 않으면 자동으로 모범답안을 생성합니다. 평가 주의사항을 입력하면 이를 근거로 채점 및 피드백을 생성할 수 있습니다.")

# 문항 및 모범답안 입력
    with st.container(border=True):
        st.caption("평가 문항 및 모범답안")
        col1, col2 = st.columns(2)
        with col1:
            question1 = st.text_area("1번 문항")
            st.divider()
            question2 = st.text_area("2번 문항")
            st.divider()
            question3 = st.text_area("3번 문항")
            st.divider()
        with col2:
            correctanswer1 = st.text_area("1번 모범답안")
            st.divider()
            correctanswer2 = st.text_area("2번 모범답안")
            st.divider()
            correctanswer3 = st.text_area("3번 모범답안")
            st.divider()

# 문항 및 모범답안 등록
        question_input_button = st.button('평가 문항 및 모범답안 등록하기')

        if question_input_button:
            st.session_state['question1'] = question1
            st.session_state['question2'] = question2
            st.session_state['question3'] = question3
            st.session_state['correctanswer1'] = correctanswer1
            st.session_state['correctanswer2'] = correctanswer2
            st.session_state['correctanswer3'] = correctanswer3
            st.success("문항 및 모범답안이 성공적으로 등록되었습니다.")

# 평가 주의사항 입력
    with st.container(border=True):
        st.caption("평가 주의사항")
        st.write("""
        평가 주의사항을 입력할 때 다음과 같은 점을 고려할 수 있습니다.

        1. 피드백 분위기: 피드백 말투, 긍정/부정 등
        2. 채점 방법: 모범답안을 생성하여 채점, 모범답안 생성 없이 채점, 개별적으로 기준 만들어서 채점, 절대평가로 채점 등
        3. 점수 구분: 3단계, 5단계 등
        4. 피드백 구성: 피드백 문단 구성
        5. 점수 구분별 주된 피드백 내용: 점수 구분에 따라 다른 피드백 내용 구성 
        6. 기타 사항
        """)

        feedbackinstruction = st.text_area("평가 주의사항")
        st.divider()

# 평가 주의사항 등록
        feedbackinstruction_input_button = st.button('평가 주의사항 등록하기')

        if feedbackinstruction_input_button:
            st.session_state['feedbackinstruction'] = feedbackinstruction
            st.success("평가 주의사항이 성공적으로 등록되었습니다.")

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.button("이전 단계", on_click=prev_page)

    with col2:
        st.button("다음 단계", on_click=next_page)
    
    with col3:
        st.button("처음 화면으로", on_click=go_home)

def step4():
    st.subheader("4단계. 평가 확인 및 저장하기")
    st.warning("선생님이 만든 서술형 평가를 확인하고 저장합니다. 수정이 필요하다면 이전 단계로 돌아가서 다시 입력한 다음 저장합니다.")

# 설정 확인
    with st.container(border=True):
        st.caption("평가 확인")
        testcheck = st.button("평가 확인")

        if testcheck:
            client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='평가 문항과 모범답안을 새롭게 등록합니다.' 
                        '기존 평가 문항과 모범답안은 지우고 지금부터 입력한 것을 기억합니다.'
                        '1번 문항은 <' + st.session_state['question1'] +'> 입니다.'
                        'user(teacher)가 입력한 모범답안은 <' + st.session_state['correctanswer1'] + '> 입니다.'
                        '2번 문항은 <' + st.session_state['question2'] + '> 입니다.'
                        'user(teacher)가 입력한 모범답안은 <' + st.session_state['correctanswer2'] + '> 입니다.' 
                        ' 3번 문항은 <' + st.session_state['question3'] + '> 입니다.' 
                        'user(teacher)가 입력한 모범답안은 <' + st.session_state['correctanswer3'] + '> 입니다.')
                    
            client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='평가 주의사항은 <' + st.session_state['feedbackinstruction'] + '> 입니다.' 
                        '피드백을 제공할 때 입력한 평가 주의사항을 고려해서 작성해주시기 바랍니다.'
                        '만약 특별히 입력한 평가 주의사항이 없다면 instruction에 있는 평가 주의사항을 고려해서 작성해주시기 바랍니다.')
            
            client.beta.threads.messages.create(
                thread_id=st.session_state['usingthread'],
                role="user",
                content='현재 업로드된 서술형 평가 문항과 모범답안, 평가 주의사항을 모두 보여주세요.'
                        'user(teacher)가 입력한 평가 문항을 입력한 그대로 보여주세요.'
                        '만약 user(teacher)가 입력한 모범답안이 있으면 user(teacher)가 입력한 것을 보여줍니다.'
                        '만약 user(teacher)가 입력한 모범답안이 없으면 vs_FtRt7SEalipabRPrOk0usxl8을 file search하여 문항과 관련된 내용을 찾아 모범답안을 만듭니다.'
                        '**vs_FtRt7SEalipabRPrOk0usxl8에서 서술형 문항과 관련된 내용을 찾을 수 없다면 모범답안을 작성하지 않습니다.**'
                        '반드시 vs_FtRt7SEalipabRPrOk0usxl8을 file search하여 내용을 찾는 과정을 거쳐야 합니다.'
                        '반드시 vs_FtRt7SEalipabRPrOk0usxl8에 있는 내용과 그 내용 수준으로 모범답안을 작성합니다.'
                        'vs_FtRt7SEalipabRPrOk0usxl8을 file search하였을 때 여러 file에서 내용을 참고할 수 있다면 여러 file 내용을 종합적으로 활용합니다.'
                        '**어떤 파일에서 어떤 페이지를 보면 되는지 함께 보여주세요.**'
                        '문단을 나눠서 서술형 평가 문항과 모범답안을 함께 보여줍니다. 서술형 평가 문항과 모범답안을 보여줄 때 **줄을 바꿔서** 구분하여 보기 쉽게 보여줍니다.')
            
            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id)

            run_id = run.id

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run_id)
                
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            msg = thread_messages.data[0].content[0].text.value
            st.write(msg)


# 설정 저장
    with st.container(border=True):
        st.caption("설정 저장하기")
        savesetting = st.button("설정 저장하기")

        if savesetting:
            credentials_dict = json.loads(st.secrets["gcp"]["credentials"])
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/spreadsheets"
            ])
            gc = gspread.authorize(credentials)
            spreadsheet = gc.open(st.secrets["google"]["spreadsheet_name"])
            worksheet = spreadsheet.sheet1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            worksheet.append_row([
            current_time, 
            st.session_state['settingname'], 
            st.session_state['question1'], 
            st.session_state['question2'], 
            st.session_state['question3'], 
            st.session_state['correctanswer1'], 
            st.session_state['correctanswer2'], 
            st.session_state['correctanswer3'], 
            st.session_state['feedbackinstruction']])
            st.success("설정이 성공적으로 저장되었습니다.")

    st.write("---")
    col1, col2, col3 = st.columns([1, 1, 3 ])

    with col1:
        st.button("이전 단계", on_click=prev_page)

    with col2:
        st.button("처음 화면으로", on_click=go_home) 

    with col3:
        st.write()

# 현재 페이지 상태에 따라 적절한 페이지 표시
current_page = st.session_state['page']

if current_page == 0:
    home()
elif current_page == 1:
    step1()
elif current_page == 2:
    step2()
elif current_page == 3:
    step3()
elif current_page == 4:
    step4()