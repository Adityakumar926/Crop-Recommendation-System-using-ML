# 🌱 Crop Recommendation System using Machine Learning

## Overview

The Crop Recommendation System is a machine learning–based web application that helps users determine the most suitable crop to grow based on soil nutrients and environmental conditions.

The system analyzes agricultural parameters such as nitrogen, phosphorus, potassium, temperature, humidity, pH level, and rainfall, and predicts the best crop using a trained machine learning model.

---

## Features

* Crop prediction using machine learning
* User-friendly web interface
* User registration and login system
* Password reset functionality
* Admin dashboard for managing users
* SQLite database integration
* ML model trained on agricultural dataset

---

## Technologies Used

* Python
* Flask
* Scikit-learn
* HTML
* CSS
* SQLite
* Jupyter Notebook

---

## Machine Learning Model

The machine learning model is trained using the Crop Recommendation dataset.

Input features used for prediction:

* Nitrogen (N)
* Phosphorus (P)
* Potassium (K)
* Temperature
* Humidity
* pH
* Rainfall

The trained model files used in the project:

* model.pkl
* minmaxscaler.pkl
* standscaler.pkl

---

## Project Structure

```
Crop-Recommendation-System-using-ML
│
├── app.py
├── model.pkl
├── minmaxscaler.pkl
├── standscaler.pkl
│
├── dataset
│   └── Crop_recommendation.csv
│
├── templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── Admin.html
│   ├── forgot_password.html
│   └── reset_password.html
│
├── static
│   ├── background.jpg
│   ├── crop.png
│   └── logo.png
│
└── README.md
```

## Installation

Clone the repository:

git clone https://github.com/Adityakumar926/Crop-Recommendation-System-using-ML.git

Move into the project folder:

cd Crop-Recommendation-System-using-ML

Install required dependencies:

pip install flask scikit-learn pandas numpy

---

## Running the Project

Run the Flask application:

python app.py

Open your browser and go to:

http://127.0.0.1:5000

---

## Future Improvements

* Integration with real-time weather APIs
* Cloud deployment
* Mobile-friendly interface
* More advanced machine learning models

---

## Author

**Aditya Kumar**  
Machine Learning and AI Enthusiast
