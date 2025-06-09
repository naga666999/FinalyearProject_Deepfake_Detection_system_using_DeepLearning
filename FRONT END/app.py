from flask import Flask,render_template,flash,redirect,request,send_from_directory,url_for, send_file
import mysql.connector, os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# from tensorflow_docs.vis import embed
from tensorflow import keras
#from imutils import paths
import cv2


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='video_detection'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']
        if password == c_password:
            query = "SELECT UPPER(email) FROM users"
            email_data = retrivequery2(query)
            email_data_list = []
            for i in email_data:
                email_data_list.append(i[0])
            if email.upper() not in email_data_list:
                query = "INSERT INTO users (email, password) VALUES (%s, %s)"
                values = (email, password)
                executionquery(query, values)
                return render_template('login.html', message="Successfully Registered! Please go to login section")
            return render_template('login.html', message="This email ID is already exists!")
        return render_template('login.html', message="Conform password is not match!")
    return render_template('login.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT UPPER(email) FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email.upper() in email_data_list:
            query = "SELECT UPPER(password) FROM users WHERE email = %s"
            values = (email,)
            password__data = retrivequery1(query, values)
            if password.upper() == password__data[0][0]:
                global user_email
                user_email = email

                return redirect("/home")
            return render_template('home.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')




### Fake video detection


MAX_SEQ_LENGTH = 20
NUM_FEATURES = 2048
IMG_SIZE = 224

# Load the model
model = keras.models.load_model(r"Models\model.h5")

# Define the feature extractor
def build_feature_extractor():
    feature_extractor = keras.applications.InceptionV3(
        weights="imagenet",
        include_top=False,
        pooling="avg",
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
    )
    preprocess_input = keras.applications.inception_v3.preprocess_input

    inputs = keras.Input((IMG_SIZE, IMG_SIZE, 3))
    preprocessed = preprocess_input(inputs)

    outputs = feature_extractor(preprocessed)
    return keras.Model(inputs, outputs, name="feature_extractor")

feature_extractor = build_feature_extractor()

# Function to prepare a single video for prediction
def prepare_single_video(frames):
    frames = frames[None, ...]
    frame_mask = np.zeros(shape=(1, MAX_SEQ_LENGTH,), dtype="bool")
    frame_features = np.zeros(shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")

    for i, batch in enumerate(frames):
        video_length = batch.shape[0]
        length = min(MAX_SEQ_LENGTH, video_length)
        for j in range(length):
            frame_features[i, j, :] = feature_extractor.predict(batch[None, j, :])
        frame_mask[i, :length] = 1  # 1 = not masked, 0 = masked

    return frame_features, frame_mask


# Utility function to load video frames
def load_video(path, max_frames=0, resize=(IMG_SIZE, IMG_SIZE)):
    cap = cv2.VideoCapture(path)
    frames = []
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = crop_center_square(frame)
            frame = cv2.resize(frame, resize)
            frame = frame[:, :, [2, 1, 0]]
            frames.append(frame)

            if len(frames) == max_frames:
                break
    finally:
        cap.release()
    return np.array(frames)

# Utility function to crop center square of a frame
def crop_center_square(frame):
    y, x = frame.shape[0:2]
    min_dim = min(y, x)
    start_x = (x // 2) - (min_dim // 2)
    start_y = (y // 2) - (min_dim // 2)
    return frame[start_y : start_y + min_dim, start_x : start_x + min_dim]


@app.route('/video_pred', methods=['GET', 'POST'])
def video_pred():
    if request.method == 'POST':
        myfile = request.files['file']
        fn = myfile.filename
        mypath = os.path.join('static/saved_videos/', fn)
        myfile.save(mypath)

        # Load the uploaded video
        frames = load_video(mypath)

        # Prepare video frames for prediction
        frame_features, frame_mask = prepare_single_video(frames)

        # Perform prediction
        prediction = model.predict([frame_features, frame_mask])[0]
        print(prediction)

        # Determine the predicted class
        if prediction >= 0.8:
            predicted_class = 'FAKE'
        else:
            predicted_class = 'REAL'
        # Pass the prediction result to the template
        return render_template('video.html', path=mypath, prediction=predicted_class)
    return render_template('video.html')






### Fake Image Prediction

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


@app.route('/image_pred', methods=['GET', 'POST'])
def image_pred():
    if request.method == 'POST':
        classes = ["Fake", "Real"]

        myfile = request.files['file']
        fn = myfile.filename
        mypath = os.path.join('static/saved_image/', fn)
        myfile.save(mypath)

        models = load_model(r"Models\cnn.h5")
        x = image.load_img(mypath, target_size=(256, 256))
        x = image.img_to_array(x)
        x = np.expand_dims(x, axis=0)
        x /= 255
        results = models.predict(x)
        b = np.argmax(results)
        prediction = classes[b]

        return render_template('image.html', path=mypath, prediction = prediction)
    return render_template('image.html')



if __name__ == '__main__':
    app.run(debug = True)