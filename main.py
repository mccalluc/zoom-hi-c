from scipy.ndimage import geometric_transform
from math import sin, cos, pi
import png

input_data = [
    [255, 200, 200, 50, 50, 100, 100],
    [200, 255, 200, 50, 50, 100, 100],
    [200, 200, 255, 50, 50, 100, 100],
    [50, 50, 50, 255, 200, 50, 50],
    [50, 50, 50, 200, 255, 50, 50],
    [100, 100, 100, 50, 50, 255, 200],
    [100, 100, 100, 50, 50, 200, 255]
]

def log_unpolar(coord, input_len, output_len):
    r = -0.5 + coord[0] / output_len
    theta = (pi / 2) * (coord[1] / output_len)
    return (
        r * sin(theta) * input_len,
        r * cos(theta) * input_len
    )

output_width = 200
output_height = 400
output_data = geometric_transform(
    input=input_data,
    mapping=log_unpolar,
    output_shape=(output_height, output_width),
    order=0,
    extra_keywords={
        'input_len':len(input_data),
        'output_len':min(output_width, output_height)
    }
)

f = open('/tmp/warped.png', 'wb')      # binary mode is important
w = png.Writer(output_width, output_height, greyscale=True)
w.write(f, output_data)
f.close()
