from flask import Flask, render_template, request, redirect, url_for, session
import speech_recognition as sr
import pyttsx3
import time
import json
import boto3
import os

app = Flask(__name__)
app.secret_key = 'sanmugamhm2004'  

# AWS S3 configuration
AWS_ACCESS_KEY_ID = 'Your AWS Access Key'
AWS_SECRET_ACCESS_KEY = 'Your AWS Secret key'
S3_BUCKET_NAME = 'newreactbucket'
OUTPUT_BUCKET_NAME = 'mockinterviewoutput'

# Initialize boto3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Load questions from JSON files based on the selected stack
def load_questions(stack):
    filename = f'{stack}questions.json'
    with open(filename, 'r') as file:
        questions = json.load(file)
    return questions

def write_to_useranswer_file(answer, question_number):
    useranswer_filename = 'useranswer.json'
    if not os.path.exists(useranswer_filename):
        user_answers = []
    else:
        with open(useranswer_filename, 'r') as file:
            user_answers = json.load(file)
    user_answer = {"answer": answer}
    if answer is None or answer.isspace():
        user_answer = {"answer": None}
    user_answers.append(user_answer)
    with open(useranswer_filename, 'w') as file:
        json.dump(user_answers, file, indent=4)

def record_speech(duration=3):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    audio_segments = []
    print(f"Recording for {duration} seconds...")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        start_time = time.time()
        while time.time() - start_time < duration:
            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
                audio_segments.append(audio)
            except sr.WaitTimeoutError:
                # pass
                print("Listening timed out while waiting for phrase to start")
    print("Recording complete.")
    return audio_segments

def recognize_speech_from_segments(audio_segments):
    recognizer = sr.Recognizer()
    full_text = ""
    for audio in audio_segments:
        try:
            print("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            # print(f"You said: {text}")
            full_text += text + " "
        except sr.RequestError:
            print("API was unreachable or unresponsive")
        except sr.UnknownValueError:
            print("Unable to recognize speech")
    return full_text.strip()

def speak_text(text):
    voice = pyttsx3.init()
    voice.say(text)
    voice.runAndWait()
    
def upload_to_s3(file_path, bucket_name, s3_key):
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
    except Exception as e:
        print(f"Error uploading {file_path} to S3: {e}")

@app.route('/')
def index():
    session.clear()
    try:
        useranswer_filename = 'useranswer.json'
        if os.path.exists(useranswer_filename):
            os.remove(useranswer_filename)
            print('User answers cleared successfully')
        else:
            print('User answers file not found')
    except:
        print("Error While deletion")
    return render_template('index.html')

@app.route('/select-stack', methods=['POST'])
def select_stack():
    stack = request.form['stack']
    session['stack'] = stack
    session['question_number'] = 0
    return redirect(url_for('start_interview'))

@app.route('/start-interview')
def start_interview():
    stack = session.get('stack')
    if not stack:
        return redirect(url_for('index'))

    questions = load_questions(stack)
    session['questions'] = questions
    session['num_questions'] = len(questions)

    return redirect(url_for('next_question'))

@app.route('/start-recognition', methods=['POST'])
def start_recognition():
    question_number = session.get('question_number', 0)
    questions = session.get('questions', [])
    num_questions = session.get('num_questions', 0)

    if question_number < num_questions:
        question = questions[question_number]
        speak_text(question)
        audio_segments = record_speech(duration=5)
        recognized_text = recognize_speech_from_segments(audio_segments)
        write_to_useranswer_file(recognized_text, question_number)

        session['question_number'] += 1

        if session['question_number'] < num_questions:
            return redirect(url_for('next_question'))
        else:
            return redirect(url_for('completed'))
    else:
        return redirect(url_for('completed'))

@app.route('/next-question', methods=['GET','POST'])
def next_question():
    question_number = session.get('question_number', 0)
    questions = session.get('questions', [])
    num_questions = session.get('num_questions', 0)

    if question_number < num_questions:
        question = questions[question_number]
        question = question['question'] 
        return render_template('question.html', question=question)
    else:
        return redirect(url_for('completed'))

@app.route('/completed')
def completed():
    stack = session.get('stack', 'default')
    answer_file = f"{stack}answer.json"
    print(answer_file)
    upload_to_s3('useranswer.json', S3_BUCKET_NAME, 'useranswer.json')
    # Trigger Lambda function after uploading the file
    print("Lambda triggered")
    lambda_client = boto3.client('lambda')
    response = lambda_client.invoke(
        FunctionName='mockinterview',
        InvocationType='Event',
        Payload=json.dumps({'bucket': S3_BUCKET_NAME, 'data_key_answer': answer_file})
    )
    time.sleep(20)
    # return render_template('completed.html')
    return redirect(url_for('display_result'))

def read_json_from_s3(bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    return json.loads(content)

@app.route('/result')
def display_result():
    result_key = 'result'
    result_data = read_json_from_s3(OUTPUT_BUCKET_NAME, result_key)
    overall_score = result_data['overall_score']
    return render_template('results.html', overall_score=overall_score)


if __name__ == '__main__':
    app.run(debug=True)
