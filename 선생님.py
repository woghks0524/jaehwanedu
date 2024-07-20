# 문항 설정 페이지

# 라이브러리
import streamlit as st
from openai import OpenAI
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
 
# API KEY, THREAD, client 생성
# api_key = st.session_state['usingapikey']
# thread_id = st.session_state['usingthread']
client = OpenAI(api_key=st.session_state['usingapikey'])
assistant_id = 'asst_t0CtEvNce3uo8pMqY4BjLY78'

# 홈페이지 구성 
st.subheader('초등학교 사회 5학년 2학기 서술형 평가 연습 도구')

# 비밀번호 설정
passwordinput = st.text_input("[[사전 설정]] 페이지에서 등록한 비밀번호를 입력하세요.")
if passwordinput == st.session_state['passwordsetting']:

# 사용 방법 소개
    with st.container(border=True):
        st.write(
    """
    [[서술형 평가 문항 설정]] 페이지 사용 방법

    1. [단원 선택]에서 평가하고자 하는 단원을 선택합니다.
        
    2. [추가 자료 입력]에서 평가에 활용할 추가 자료를 입력합니다. 수업 시간에 활용한 수업자료나 활동지를 pdf로 변환하여 업로드할 수 있습니다. 
    - 추가 자료를 입력하면 모범 답안을 생성하거나 채점 및 피드백을 제공하는 데 활용됩니다.

    3. [평가 문항 입력]에서 평가 문항을 입력합니다. 평가 문항은 최대 3개 입력할 수 있습니다. 
    - 모범 답안을 입력하면 사용자가 입력한 모범 답안이 활용되고, 모범 답안을 입력하지 않으면 자체적으로 생성된 모법 답안이 활용됩니다.

    4. [주의사항 입력]에서 채점 및 피드백에 대해 설정하고 싶은 내용을 입력합니다.
    """)
    
# 탭설정
    tab1, tab2, tab3, tab4 = st.tabs(["1. 단원 선택", "2. 추가 자료 입력", "3. 평가 문항 입력", "4. 주의사항 입력"])

# 탭1: 단원 선택
# 단원에 따라 assistant ID 변경(미리 입력한 파일이 다름. 이유는 가볍게 만들기 위해, 아래 어시스턴트 아이디 다르게 해야함.)
    with tab1:
        st.subheader("1. 단원 선택")
        chapter_select = st.selectbox
        st.selectbox("",("1-1 나라의 등장과 발전","1-2 독창적 문화를 발전시킨 고려", "1-3 민족 문화를 지켜 나간 조선"), index=None, placeholder="단원을 선택해주세요.")
        if chapter_select == "1-1 나라의 등장과 발전":
            assistant_id = assistant_id

        elif chapter_select == "1-2 독창적 문화를 발전시킨 고려":
            assistant_id = assistant_id

        elif chapter_select == "1-3 민족 문화를 지켜 나간 조선":
            assistant_id = assistant_id

# 탭2: 추가 자료 입력
    with tab2:
        st.subheader("2. 추가 자료 입력")

# 파일 업로더 입력
        uploaded_file = st.file_uploader("")

# 파일이 선택되어 있고 업로드 버튼을 누르면 파일 업로드 
        run_file_button = st.button('파일 등록') 

        if uploaded_file is not None and run_file_button:
            uploaded_file_response = client.files.create(
            file=uploaded_file, 
            purpose="assistants"
            )

# 생성된 파일 id를 vector stores에 입력하는 과정
            vector_store_file = client.beta.vector_stores.files.create(
            vector_store_id='vs_FtRt7SEalipabRPrOk0usxl8',
            file_id=uploaded_file_response.id
            )
            st.success(f'파일이 성공적으로 등록되었습니다.')
        
# 업로드된 파일 목록 표시
        filelist = st.checkbox("등록된 파일 목록 (확인 후에는 체크 박스를 해제 해주세요.)")
        if filelist:
            thread_message = client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='벡터 스토어 vs_FtRt7SEalipabRPrOk0usxl8 파일 서치해서 업로드된 파일 목록을 모두 보여주세요. 파일 목록 외에 아무 문장도 넣지 마세요. 줄 바꿈으로 해서 보기 쉽게 보여주세요.',
            )

            run = client.beta.threads.runs.create(
            thread_id=st.session_state['usingthread'],
            assistant_id=assistant_id
            )
            run_id = run.id

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run.id
                    )   
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            msg = thread_messages.data[0].content[0].text.value
            st.write(msg)

# 탭3: 문항 입력
    with tab3:
        st.subheader("3. 평가 문항 입력")

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

# 평가 문항 입력
        question_input_button = st.button('문항 등록')

        if question_input_button:
            st.session_state['question1'] = question1
            st.session_state['question2'] = question2
            st.session_state['question3'] = question3

            thread_message = client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='평가 문항과 모범답안을 새롭게 등록합니다. 기존 평가 문항과 모범답안은 잊고 지금부터 입력한 것을 기억하세요. 1번 문항은 <' + question1 + 
            '> 입니다. 사용자가 입력한 모범답안은 <' + correctanswer1 + 
            ' 입니다. 2번 문항은 <' + question2 + '> 입니다. 사용자가 입력한 모범답안은 <' + correctanswer2 + 
            ' 입니다. 3번 문항은 <' + question3 +'> 입니다. 사용자가 입력한 모범답안은 <' + correctanswer3 + ' 입니다. '
            )

            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id
                )

            run_id = run.id

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run_id
                    )   
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)
            st.success(f'서술형 문항이 성공적으로 등록되었습니다.')

# 서술형 평가 문항 및 모범답안 확인
        questioncorrectanswerlist = st.checkbox("서술형 평가 문항 및 모범답안 확인 (확인 후에는 체크 박스를 해제 해주세요.)")
        if questioncorrectanswerlist:
            thread_message = client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='현재 업로드된 서술형 평가 문항과 모범답안을 모두 보여주세요. user(teacher)가 입력한 평가 문항을 그대로 보여주세요. 모범답안의 경우 user(teacher)가 입력한 것이 있으면 그것을 보여주고, 없으면 file search를 통해 모범답안을 만들어서 보여주세요. 어떤 파일 어떤 페이지를 보면 되는지 함께 보여주세요. 표 형태로 보여주세요. 반드시 서술형 평가 문항와 모범답안 외에 다른 문장을 넣지 마세요.',
            )

            run = client.beta.threads.runs.create(
            thread_id=st.session_state['usingthread'],
            assistant_id=assistant_id
            )
            run_id = run.id

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run_id
                    )   
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            msg = thread_messages.data[0].content[0].text.value
            st.write(msg)

# 탭4: 평가 주의사항 입력
    with tab4:
        st.subheader("4. 평가 주의사항 입력")
        with st.container(border=True):
            st.write(
    """
    평가 주의사항을 입력할 때 아래와 같은 점을 고려할 수 있습니다.

    1. 피드백 분위기: 피드백 말투, 긍정/부정 등
    2. 채점 방법: 모범답안을 생성하여 채점, 모범답안 생성 없이 채점, 개별적으로 기준 만들어서 채점, 절대평가로 채점 등
    3. 점수 구분: 3단계, 5단계 등
    4. 피드백 구성: 피드백 문단 구성
    5. 점수 구분별 주된 피드백 내용: 점수 구분에 따라 다른 피드백 내용 구성 
    6. 기타 사항

    """)
        feedbackinstruction = st.text_area("평가 주의사항")
        st.divider()

        feedbackinstruction_input_button = st.button('평가 주의사항 등록')

        if feedbackinstruction_input_button:
            thread_message = client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='평가 주의사항은 <' + feedbackinstruction + '> 입니다. 피드백을 제공할 때 위 내용을 고려해서 작성해주시기 바랍니다.'
            )

            run = client.beta.threads.runs.create(
                thread_id=st.session_state['usingthread'],
                assistant_id=assistant_id
                )

            run_id = run.id

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run_id
                    )   
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)

            st.success(f'평가 주의사항이 입력되었습니다.')

# 평가 주의사항 확인
        guidelinelist = st.checkbox("평가 주의사항 확인 (확인 후에는 체크 박스를 해제 해주세요.)")
        if guidelinelist:
            thread_message = client.beta.threads.messages.create(
            thread_id=st.session_state['usingthread'],
            role="user",
            content='현재 업로드된 평가 주의사항을 모두 보여주세요. 반드시 평가 주의사항 외에 다른 문장을 넣지 마세요.',
            )

            run = client.beta.threads.runs.create(
            thread_id=st.session_state['usingthread'],
            assistant_id=assistant_id
            )
            run_id = run.id

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state['usingthread'],
                    run_id=run_id
                    )   
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)

            thread_messages = client.beta.threads.messages.list(st.session_state['usingthread'])
            msg = thread_messages.data[0].content[0].text.value
            st.write(msg)

else:
    st.error("비밀번호를 바르게 입력하세요.")