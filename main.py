from scipy.ndimage import geometric_transform
from math import pi
from cmath import exp
import png
from base64 import b64decode
import requests
from struct import iter_unpack


def hi_c(x, y, z):
    tile_id = 'CQMd6V_cRw6iCI_-Unl3PQ.{}.{}.{}'.format(x, y, z)
    params = {
        'd': tile_id,
        's': 'AD_Srgd6S1uCsmnFmRJZ3Q'
    }
    url = 'http://higlass.io/api/v1/tiles/'
    tile_data = requests.get(url, params=params).json()[tile_id]
    dtype = tile_data['dtype']
    # scale by max_value / min_value
    if dtype == 'float16':
        bytes = b64decode(tile_data['dense'])
        ints = list([i[0] for i in iter_unpack('<H', bytes)])
        # TODO: Return floats
        # max_val = tile_data['max_value']
        # min_val = tile_data['min_value']
        # span = max_val - min_val
        # floats = [i[0] * span + min_val for i in ints]
        # return [floats[i:i + 256] for i in range(0, len(floats), 256)]
        triangle = [[j/256 for j in ints[i:i + 256]] for i in range(0, len(ints), 256)]
    else:
        raise RuntimeError('Unsupported type: ' + dtype)
    # Mirror:
    for x in range(256):
        for y in range(1,x):
            triangle[y][x] = triangle[x][y]
    # Increase brightness:
    for x in range(256):
        for y in range(256):
            triangle[x][y] = min(4 * triangle[x][y], 255)
    return triangle

def conformal(coord, input_len, output_len):
    # In the range 0 to 1:
    x = pi / 2 * coord[0] / output_len
    y = coord[1] / output_len
    real = x - 4.5
    imag = y * pi / 2
    mapped = exp(complex(real, imag))
    return (
        mapped.real * input_len,
        mapped.imag * input_len
    )

input_data = hi_c(0,0,0)

output_width = 300
output_height = 900
output_data = geometric_transform(
    input=input_data,
    mapping=conformal,
    output_shape=(output_height, output_width),
    order=0,  # "1" to smooth
    extra_keywords={
        'input_len':len(input_data),
        'output_len':min(output_width, output_height)
    }
)

f = open('/tmp/warped.png', 'wb')
w = png.Writer(output_width, output_height, greyscale=True)
w.write(f, output_data)
f.close()
