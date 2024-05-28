from flask import Flask, request, send_file
from PIL import Image, ImageOps
import io
from rembg import remove
import requests
from io import BytesIO
import os
import base64


from flask_cors import CORS


app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return 'Hello World'

def data_uri_to_pil_image(data_uri):

    # Remove the data URI header
    header, encoded = data_uri.split(',', 1)

    # Decode the base64 data
    data = base64.b64decode(encoded)

    # Create a BytesIO object from the decoded data
    image_data = io.BytesIO(data)

    # Open the image from the BytesIO object
    image = Image.open(image_data)

    return image


# Function to process the image
def process_image(image_file):

    print(image_file)

    os.makedirs('original', exist_ok=True)
    os.makedirs('masked', exist_ok=True)

    image = image_file.convert("RGB")

    image.save('original/image.jpg', format = "jpeg")

    output_path = "masked/image.png"

    with open(output_path, "wb") as f:
        input = open('original/image.jpg', 'rb').read()
        subject = remove(input)
        f.write(subject)

    palestine_bg = "https://flagdownload.com/wp-content/uploads/Flag_of_Palestine_Flat_Round-1024x1024.png"
    background_img = Image.open(BytesIO(requests.get(palestine_bg).content))


    palestine_bg = "https://flagdownload.com/wp-content/uploads/Flag_of_Palestine_Flat_Round-1024x1024.png"
    background_img = Image.open(BytesIO(requests.get(palestine_bg).content))

    # Create a semi-transparent overlay
    overlay = Image.new('RGBA', background_img.size, (0, 0, 0, 120))  # Adjust the last value (120) to control transparency
    background_img = Image.alpha_composite(background_img.convert('RGBA'), overlay)

    background_img = background_img.resize((image.width, image.height))
    #image = image.resize((background_img.width, background_img.height))

    background_img = background_img.convert("RGBA")

    input_img = Image.open('original/image.jpg')

    input_img = input_img.convert("RGBA")

    combined_img = Image.alpha_composite(input_img, background_img)

    combined_img = combined_img.convert('RGB')
    # combined_img.save('masked/finale.jpg', format='jpeg')

    foreground_img = Image.open(output_path)
    combined_img.paste(foreground_img, (0,0), foreground_img)

    combined_img = combined_img.convert('RGB')
    # combined_img.save("masked/background_final.jpg", format="jpeg")

    img_bytes = BytesIO()
    combined_img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    return img_bytes

@app.route('/process_image', methods=['POST'])
def upload_image():
    if 'image' not in request.form:
        return 'No image uploaded', 400

    data_uri = request.form['image']
    
    
    image_file = data_uri_to_pil_image(data_uri)


    processed_image = process_image(image_file)

    return send_file(
        io.BytesIO(processed_image),
        mimetype='image/png',
        as_attachment=True,
        download_name='free_palestine.png'
    )

if __name__ == '__main__':
    app.run(debug=True)