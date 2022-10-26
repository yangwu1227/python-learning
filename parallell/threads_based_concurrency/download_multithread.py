from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
import time
import os


def download_image(url):
    image_data = None
    # Note that urlopen returns a bytes object
    with urlopen(url) as f:
        # Read bytes
        image_data = f.read()

    # If image_data is None, then the download failed
    if not image_data:
        raise Exception(f"Failed to download the image from {url}")

    # Return the final component of the URL
    filename = os.path.basename(url)
    # Open file in write binary mode
    with open(filename, 'wb') as image_file:
        image_file.write(image_data)
        print(f'{filename} was downloaded successfully')


if __name__ == '__main__':

    start = time.perf_counter()

    urls = ['https://upload.wikimedia.org/wikipedia/commons/9/9d/Python_bivittatus_1701.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/4/48/Python_Regius.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/d/d3/Baby_carpet_python_caudal_luring.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/f/f0/Rock_python_pratik.JPG',
            'https://upload.wikimedia.org/wikipedia/commons/0/07/Dulip_Wilpattu_Python1.jpg',
            'https://en.wikipedia.org/wiki/Image#/media/File:Image_created_with_a_mobile_phone.png',
            'https://en.wikipedia.org/wiki/Image#/media/File:TEIDE.JPG',
            'https://en.wikipedia.org/wiki/Image#/media/File:Pencil_drawing_of_a_girl_in_ecstasy.jpg',
            'https://en.wikipedia.org/wiki/Cristiano_Ronaldo#/media/File:Cristiano_Ronaldo_2018.jpg',
            'https://en.wikipedia.org/wiki/Cristiano_Ronaldo#/media/File:Ronaldo_-_Manchester_United_vs_Chelsea.jpg',
            'https://en.wikipedia.org/wiki/Cristiano_Ronaldo#/media/File:Ronaldo_in_2018.jpg',
            'https://en.wikipedia.org/wiki/Cristiano_Ronaldo#/media/File:Cristiano_Ronaldo_20120609.jpg',
            'https://en.wikipedia.org/wiki/Cristiano_Ronaldo#/media/File:1_cristiano_ronaldo_2016.jpg',
            'https://en.wikipedia.org/wiki/Cristiano_Ronaldo#/media/File:Contr%C3%B4le_de_Cristiano_Ronaldo.jpg',
            'https://en.wikipedia.org/wiki/C%2B%2B#/media/File:ANSI_ISO_C++_WP.jpg',
            'https://en.wikipedia.org/wiki/Python_(programming_language)#/media/File:Python_3._The_standard_type_hierarchy.png',
            'https://en.wikipedia.org/wiki/Python_(programming_language)#/media/File:Python_Powered.png',
            'https://en.wikipedia.org/wiki/Muhammad_Ali#/media/File:Muhammad_Ali_NYWTS.jpg',
            'https://en.wikipedia.org/wiki/Muhammad_Ali#/media/File:JoeEMartinCassiusClay1960.jpg',
            'https://en.wikipedia.org/wiki/Muhammad_Ali#/media/File:Muhammad_Ali_and_Jimmy_Carter.jpg'
            ]

    with ThreadPoolExecutor() as executor:
        executor.map(download_image, urls)

    finish = time.perf_counter()

    print(f'It took {finish-start} second(s) to finish.')
