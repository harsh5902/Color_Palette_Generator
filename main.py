from flask import Flask, render_template, request
import shutil
import numpy as np
from PIL import Image
import pandas as pd


# -----------------------------------------Color Extraction Process ---------------------------------------------------#
# RGB to HEX color converter
def rgb_to_hex(r, g, b):
  return ('{:X}{:X}{:X}').format(r, g, b)


# Color Extraction
def palette_generator(picture):
    # Taking input image
    my_img = Image.open(picture)

    # Taking image as numpy array
    img_arr = np.array(my_img)
    height = img_arr.shape[0]
    width = img_arr.shape[1]
    RGB_list = []
    HEX_list = []

    # Append all the colors to the list in RGB and HEX format
    for i in range(height):
        for j in range(width):
            rgb = (img_arr[i][j][0], img_arr[i][j][1], img_arr[i][j][2])
            RGB_list.append(rgb)
            HEX_list.append(rgb_to_hex(img_arr[i][j][0], img_arr[i][j][1], img_arr[i][j][2]))

    # Creating dataframe of the RGB colors and HEX colors present in image
    df = pd.DataFrame({"RGB_color": RGB_list, "HEX_color": HEX_list})
    max_col_df = pd.DataFrame(data=df.HEX_color.value_counts().head(10), columns=['HEX_color'])

    # Returning top 10 most used colors in the input image
    return max_col_df.index


# --------------------------------------------Flask Application -------------------------------------------------------#
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/result', methods=['GET', 'POST'])
def result():
    try:
        # Taking file path adn file name from the path entered
        file_path = request.form['file-path']
        split_path = file_path.split('/')
        file_name = split_path[-1]

        # Copying the image file from original path to '../static/*.jpg'
        original = rf"{file_path}"
        target = rf"C:/Users/DELL/PycharmProject/Color_Palette_Generator/static/{file_name}"
        new_path = shutil.copyfile(src=original, dst=target)

    except FileNotFoundError:
        return "<h1>The file you chose does not exist or it is not an image file</h1>"

    else:
        colors_used = palette_generator(new_path)
        return render_template("colors.html", img=new_path, file=file_name, colors=colors_used)


if __name__ == "__main__":
    app.run(debug=True)




