from scipy.ndimage import geometric_transform
from math import sin, cos, pi
import png

input_data = [
    [1,2,255],
    [2,255,4],
    [255,4,5]
]

def log_unpolar(coord, input_len, output_len):
    r = coord[0] / output_len
    theta = (pi / 2) * (coord[1] / output_len)
    return (
        r * sin(theta) * input_len,
        r * cos(theta) * input_len
    )

output_len = 200
output_data = geometric_transform(
    input=input_data,
    mapping=log_unpolar,
    output_shape=(output_len, output_len),
    order=0,
    extra_keywords={
        'input_len':len(input_data),
        'output_len':output_len
    }
)

f = open('/tmp/warped.png', 'wb')      # binary mode is important
w = png.Writer(output_len, output_len, greyscale=True)
w.write(f, output_data)
f.close()
