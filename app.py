from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
import base64
from PIL import Image
import io

app = Flask(__name__)

# Cargar el modelo y definir las clases
model = tf.keras.models.load_model('gommodel.keras')
class_names = ['corazon', 'cubo', 'diente', 'fruta', 'gusano', 'huevo', 'mango', 'pandita', 'pinguino', 'tiburon']

# Ruta para renderizar la página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para recibir la imagen capturada y realizar la predicción
@app.route('/predict', methods=['POST'])
def predict():
    # Recibir la imagen capturada desde el cliente
    image_data = request.form['image_data'].split(",")[1]
    
    # Decodificar la imagen base64 y convertirla en un objeto de imagen
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    
    # Procesar la imagen y realizar la predicción con el modelo cargado
    image = image.resize((180, 180))
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0)
    
    # Realizar la predicción
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    sorted_indexes = np.argsort(score)[::-1]
    
    # Crear el texto de los resultados de la predicción
    results_text = "La imagen puede clasificarse como:<br><br>"
    for i in range(len(class_names)):
        class_name = class_names[sorted_indexes[i]]
        class_score = 100 * score[sorted_indexes[i]].numpy()
        results_text += f"{class_name}: {class_score:.2f}%<br>"
    
    # Devolver los resultados como JSON
    return jsonify({'results': results_text})

if __name__ == '__main__':
    app.run(debug=True)
