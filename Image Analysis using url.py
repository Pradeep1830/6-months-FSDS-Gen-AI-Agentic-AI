import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO #bytes io used for buffer memory to store or capture images )


def load_image_from_url(url):
      response = requests.get(url)
      return Image.open(BytesIO(response.content))


elephant_url = 'https://cdn.mos.cms.futurecdn.net/v2/t:0,l:420,cw:1080,ch:1080,q:80,w:1080/TVR7E3Kuzg2iRhKkjZPeWk.jpg'
#lion_url = 'https://static.vecteezy.com/system/resources/previews/026/525/162/non_2x/lion-animal-isolated-photo.jpg'

elephant = load_image_from_url(elephant_url)
#lion= load_image_from_url(lion_url)

# display an original image
plt.figure(figsize=(6,4))
plt.imshow(elephant)
plt.title('elephant')
plt.axis( 'off')
plt.show()

# display an original image
#plt.figure(figsize=(6,4))
#plt.imshow(lion)
#plt.title('lion')
#plt.axis( 'off')
#plt.show()