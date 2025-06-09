# FinalyearProject_Deepfake_Detection_system_using_DeepLearning
A deepfake detection system using CNN &amp; GRU


# DeepFake Detection System for Face-Swap Videos Using Deep Learning

This project aims to detect deepfake media—particularly face-swapped videos—using advanced deep learning models. We use GRUs for temporal video analysis and CNN-based architectures (VGG16 and MobileNet) for image analysis. A web-based user interface allows users to upload media and receive real-time authenticity verification.

---

## 🧠 Technologies Used

- *Programming Language*: Python 3.6+
- *Deep Learning Models*: GRU, VGG16, MobileNet
- *Libraries*: Flask, Pandas, NumPy, OpenCV, Keras, TensorFlow
- *Frontend*: HTML, CSS, Bootstrap, JavaScript
- *Backend*: Flask + MySQL
- *Deployment*: XAMPP Server
- *IDE*: VS Code

---

## 🏗 System Architecture

- *Image Analysis* → CNN (VGG16 / MobileNet)
- *Video Analysis* → GRU (Sequence modeling of facial movements)
- *Web Interface* → Flask app with user login, upload, and results dashboard

---

✅ README for Deepfake Detection System using Deep Learning

# 🔍 Deepfake Detection System using Deep Learning

This is my Final Year Project for detecting deepfake videos or images using deep learning techniques. The project uses a Convolutional Neural Network (CNN) to classify whether a given video or image is real or fake.

---

## 📁 Project Files

- train_model.py → For training the model.
- test_model.py → For testing the model with test data.
- predict.py → For predicting if an image or video is deepfake.
- model/ → Contains saved trained model (model.h5).
- dataset/ → Your dataset of real and fake videos/images.
- output/ → Stores prediction results, charts, graphs.

---

## 💻 How to Run This Project

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/naga666999/FinalyearProject_Deepfake_Detection_system_using_DeepLearning.git
cd FinalyearProject_Deepfake_Detection_system_using_DeepLearning


---

🔹 2. Install Required Python Libraries

You must have Python installed (preferably 3.7+). Then run:

pip install tensorflow keras opencv-python numpy matplotlib

Or use:

pip install -r requirements.txt

(if you create a requirements.txt file)


---

🔹 3. Prepare the Dataset

Put your images/videos inside the dataset/ folder.

Recommended structure:

dataset/
├── real/
│   └── real1.jpg
├── fake/
    └── fake1.jpg


---

🔹 4. Train the Model

python code/train_model.py

> This will train the CNN and save it as model/model.h5.




---

🔹 5. Test the Model

python code/test_model.py

> Displays model accuracy and performance.




---

🔹 6. Predict with a New Image or Video

python code/predict.py --file path/to/image_or_video

> It will print whether the input is REAL or FAKE.




---

---

📃 License

This project is licensed under the MIT License.


---

📬 Contact

GitHub: naga666999

Email: youremail@example.com


---

- Help push the README.md to your GitHub repo via Git commands?

Thank you!
