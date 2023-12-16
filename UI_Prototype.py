import streamlit as st
import requests
import json
import webbrowser

DEBUG = False
DUMMY = False

### Title
st.title("Singing-Voice-Conversion Demonstration")
st.write("Graduation Project Team 2")

### Sidebar for debugging
if DEBUG:
    st.sidebar.header("DEBUG = True")
    st.sidebar.markdown("---")

if DUMMY:
    st.sidebar.header("DUMMY = True")
    st.sidebar.markdown("---")







### Step 1: Seperate music
st.markdown('<hr style="border:1px solid">', unsafe_allow_html=True)
st.header("✅ Step 1: Select Music")
st.markdown("---")

col1, col2 = st.columns([5, 95]) ### 5:95 ratio for padding
with col2:
    ### Step 1-1 : Select Music
    st.subheader("Step 1-1: Select Music to apply your voice")
    st.write("Please select a Song from the dropdown list below: ")

    if 'json_available_music' not in st.session_state:
        st.session_state['json_available_music'] = []

    if not DUMMY:
        response = requests.get(
        url = "https://cn7qctd66b.execute-api.ap-northeast-2.amazonaws.com/singtome/original-songs"
        )   

        response_data = response.json()

        ### Display Response
        print()
        print(json.loads(response.text))

        if DEBUG:
            st.sidebar.write(json.loads(response.text))

        ### Parsing Response Body into Json
        st.session_state['json_available_music'] = json.loads(response.json()['body'])

    else:
        st.session_state['json_available_music'] = ["1.wav", "2.wav", "3.wav"]
            
    col1, col2 = st.columns(2)
    with col1:
        selected_song = st.selectbox("", st.session_state['json_available_music'])

    if selected_song is not None:
        selected_song_id = selected_song.replace('.wav', '')

    if DEBUG:
        st.sidebar.write("selected_music: ", selected_song)
        if selected_song is not None:
            st.sidebar.write("selected_music_id: ", selected_song_id)

st.markdown("---")

col1, col2 = st.columns([5, 95]) ### 5:95 ratio for padding
with col2:
    ### Step 1-2: Initiate Vocal and Instrument Separation
    st.subheader("Step 1-2: Initiate Music Separation")
    st.write("Please press the button below to initiate Vocal and Instrument Separation. <br>This process will take up to 3 minutes.", unsafe_allow_html=True)
    st.write("")

    st.write()
    if st.button("START SEPERATION"):    

        response = requests.post(
            url = "https://cn7qctd66b.execute-api.ap-northeast-2.amazonaws.com/singtome/uvr-inference",
            data = json.dumps ({"song_id": selected_song_id}),
            headers={"Content-Type": "application/json"}
        )

        ### Display Response
        print()
        print(json.loads(response.text))

        if DEBUG:
            st.sidebar.write(json.loads(response.text))

        st.session_state['step1_button_pushed'] = True


### Step 1 Complete
if 'step1_button_pushed' in st.session_state:
    if st.session_state['step1_button_pushed']:
        st.markdown("---")

        col1, col2 = st.columns([5, 95]) ### 5:95 ratio for padding
        with col2:
            st.subheader("⌛ Step 1 in Progress..")

            st.write()
            st.write("Please press this button before proceeding to next step")

            if st.button("CHECK IF STEP 1 HAS BEEN COMPLETED"):
                response = requests.get(
                url = "https://cn7qctd66b.execute-api.ap-northeast-2.amazonaws.com/singtome/check/uvr-complete",
                data = json.dumps ({"song_id": selected_song_id}),
                headers={"Content-Type": "application/json"}
            )
                
                response_data = response.json()
                st.session_state['step1_body_value'] = response_data.get('body')


        if 'step1_body_value' in st.session_state:
            if st.session_state['step1_body_value']:
                st.session_state['step1_complete'] = True

                st.markdown("---")

                col1, col2, col3 = st.columns([3,4,3]) ### 3:4:3 Ratio
                with col2: 
                    st.subheader("🎉 Step 1 Complete!")

        ### Display Response
        print()
        print(json.loads(response.text))

        if DEBUG:
            st.sidebar.write(json.loads(response.text))

            

        







### Step 2: Train Your Voice

st.markdown('<hr style="border:1px solid">', unsafe_allow_html=True)
st.header("✅ Step 2: Train Your Voice")
st.markdown("---")

col1, col2 = st.columns([5, 95]) ### 5:95 ratio for padding
with col2:
    ### Step 2-1 : Select Music
    st.subheader("Step 2-1: Select User ID to apply.")
    st.write("Please select an User ID from the dropdown list below: ")

    if 'json_available_user' not in st.session_state:
        st.session_state['json_available_user'] = []

    if not DUMMY:
        response = requests.get(
        url = "https://cn7qctd66b.execute-api.ap-northeast-2.amazonaws.com/singtome/voices"
        )   

        response_data = response.json()

        ### Display Response
        print()
        print(json.loads(response.text))

        if DEBUG:
            st.sidebar.write(json.loads(response.text))

        ### Parsing Response Body into Json
        st.session_state['json_available_user'] = json.loads(response.json()['body'])

    else:
        st.session_state['json_available_user'] = ["1", "2", "3"]

    col1, col2 = st.columns(2)
    with col1:
        selected_user = st.selectbox(" ", st.session_state['json_available_user'])

    if selected_user is not None:
        selected_user_id = selected_user.replace('.wav', '')

    if DEBUG:
        st.sidebar.write("selected_user: ", selected_user)
        if selected_song is not None:
            st.sidebar.write("selected_user_id: ", selected_user_id)

st.markdown("---")

col1, col2 = st.columns([5, 95]) ### 5:95 ratio for padding
with col2:
    ### Step 2-2 : Select Music
    st.subheader("Step 2-2: Select Music to apply your voice")
    st.write("Please press the button below to train RVC model with your voice. <br>This process will take up to 10 minutes.", unsafe_allow_html=True)

    if st.button("START TRAINING"):
        response = requests.post(
            url = "https://cn7qctd66b.execute-api.ap-northeast-2.amazonaws.com/singtome/rvc-train",
            data = json.dumps ({"user_id": selected_user_id}),
            headers={"Content-Type": "application/json"}
        )

        ### Display Response
        print()
        print(json.loads(response.text))

        if DEBUG:
            st.sidebar.write(json.loads(response.text))

        st.session_state['step2_button_pushed'] = True

### Step 2 Complete
if 'step2_button_pushed' in st.session_state:
    if st.session_state['step2_button_pushed']:
        st.markdown("---")

        col1, col2 = st.columns([5, 95]) ### 5:95 ratio for padding
        with col2:
            st.subheader("⌛ Step 2 in Progress..")

            st.write()
            st.write("Please press this button to check if the Step 2 is completed")

            if st.button("CHECK IF STEP 2 HAS BEEN COMPLETED"):
                response = requests.get(
                url = "https://cn7qctd66b.execute-api.ap-northeast-2.amazonaws.com/singtome/check/rvc-train-complete",
                data = json.dumps ({"user_id": selected_user_id}),
                headers={"Content-Type": "application/json"}
            )
                
                response_data = response.json()
                st.session_state['step2_body_value'] = response_data.get('body')

        if 'step2_body_value' in st.session_state:
            if st.session_state['step2_body_value']:
                st.session_state['step2_complete'] = True

                st.markdown("---")

                col1, col2, col3 = st.columns([3,4,3]) ### 3:4:3 Ratio
                with col2: 
                    st.subheader("🎉 Step 2 Complete!")

        ### Display Response
        print()
        print(json.loads(response.text))

        if DEBUG:
            st.sidebar.write(json.loads(response.text))







### Step 3: Voice Conversion
st.markdown('<hr style="border:1px solid">', unsafe_allow_html=True)
st.header("✅ Step 3: Voice Conversion")
st.markdown("---")

col1, col2 = st.columns([5, 95]) ### 5:95 ratio for padding
with col2:
    st.write("Please press the button below to process the selected song with your trained voice model. <br>This process will take up to 5 minutes.", unsafe_allow_html=True)


    if st.button("START CONVERSION"):
        response = requests.post(
            url = "https://cn7qctd66b.execute-api.ap-northeast-2.amazonaws.com/singtome/rvc-inference",
            data = json.dumps ({"song_id": selected_song_id, "user_id": selected_user_id}),
            headers={"Content-Type": "application/json"}
        )

        ### Display Response
        print()
        print(json.loads(response.text))

        if DEBUG:
            st.sidebar.write(json.loads(response.text))

        st.session_state['step3_button_pushed'] = True

# ### Step 3 Complete
# if 'step3_button_pushed' in st.session_state:
#     if st.session_state['step3_button_pushed']:
#         st.markdown("---")
#         col1, col2, col3 = st.columns([3,4,3]) ### 3:4:3 Ratio
#         with col2: st.subheader("🎉 Step 3 Complete!")

### Step 3 Complete
if 'step3_button_pushed' in st.session_state:
    if st.session_state['step3_button_pushed']:
        st.markdown("---")

        col1, col2 = st.columns([5, 95]) ### 5:95 ratio for padding
        with col2:
            st.subheader("⌛ Step 3 in Progress..")

            st.write()
            st.write("Please press this button to check if the Step 3 is completed")

            if st.button("CHECK IF STEP 3 HAS BEEN COMPLETED"):
                response = requests.get(
                url = "https://cn7qctd66b.execute-api.ap-northeast-2.amazonaws.com/singtome/check/rvc-infer-complete",
                data = json.dumps ({"song_id": selected_song_id,"user_id": selected_user_id}),
                headers={"Content-Type": "application/json"}
            )
                
                response_data = response.json()
                st.session_state['step3_body_value'] = response_data.get('body')

    if 'step3_body_value' in st.session_state:
        if st.session_state['step3_body_value']:
            st.session_state['step3_complete'] = True

            st.markdown("---")

            col1, col2, col3 = st.columns([3,4,3]) ### 3:4:3 Ratio
            with col2: 
                st.subheader("🎉 Step 3 Complete!")

        ### Display Response
        print()
        print(json.loads(response.text))

        if DEBUG:
            st.sidebar.write(json.loads(response.text))






### Step 4: Combine
st.markdown('<hr style="border:1px solid">', unsafe_allow_html=True)
st.header("✅ Step 4: Combine")
st.markdown("---")

col1, col2 = st.columns([5, 95]) ### 5:95 ratio for padding
with col2:

    st.write("Please press the button below to Combine the converted vocal file and the instrumental file <br>This process will take up to 3 minutes.", unsafe_allow_html=True)

    if st.button("COMBINE"):
        response = requests.post(
            url = "https://cn7qctd66b.execute-api.ap-northeast-2.amazonaws.com/singtome/vocal-mr-merge",
            data = json.dumps ({"song_id": selected_song_id, "user_id": selected_user_id}),
            headers={"Content-Type": "application/json"}
        )

        ### Display Response
        print()
        print(json.loads(response.text))

        if DEBUG:
            st.sidebar.write(json.loads(response.text))

        # message = json.loads(response.text).get("message")
        # st.write("Result: " + message)

        st.session_state['step4_complete'] = True


### Step 4 Complete
if 'step4_complete' in st.session_state:
    if st.session_state['step4_complete']:
        st.markdown("---")
        col1, col2, col3 = st.columns([3,4,3]) ### 3:4:3 Ratio
        with col2:
            st.subheader("🎉 Step 4 Complete!")

    col1, col2 = st.columns([16, 74])
    with col2:
        st.subheader("")
        st.subheader("Here is the final song with your voice")

        col1, col2, col3 = st.columns([25,50,25])
        with col2:
            st.write()
            st.write()
            if st.button("DOWNLOAD"):
                response = requests.get(
                url = "https://cn7qctd66b.execute-api.ap-northeast-2.amazonaws.com/singtome/download/song",
                data = json.dumps ({"song_id": selected_song_id, "user_id": selected_user_id}),
                headers={"Content-Type": "application/json"}
                )

                response_data = response.json()
                st.session_state['download_url'] = response_data.get('body')

                if DEBUG:
                    st.sidebar.write(st.session_state['download_url'])

                if 'download_url' in st.session_state:
                    if st.session_state['download_url'] == "Object not found":
                        st.write("The file is still being processed. <br> Please try again later.", unsafe_allow_html=True)
                    else:
                        webbrowser.open_new_tab(st.session_state['download_url'])
        
st.markdown('<hr style="border:1px solid">', unsafe_allow_html=True)