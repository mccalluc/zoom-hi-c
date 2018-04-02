from scipy.ndimage import geometric_transform
from math import pi
from cmath import exp
import png

input_data = [
    [255, 200, 50, 50, 100, 100],
    [200, 255, 50, 50, 100, 100],
    [50, 50, 255, 200, 50, 50],
    [50, 50, 200, 255, 50, 50],
    [100, 100, 50, 50, 255, 200],
    [100, 100, 50, 50, 200, 255]
]

def conformal(coord, input_len, output_len):
    # In the range 0 to 1:
    x = pi / 2 * coord[0] / output_len
    y = coord[1] / output_len
    real = x - 3
    imag = y * pi / 2
    mapped = exp(complex(real, imag))
    return (
        mapped.real * input_len,
        mapped.imag * input_len
    )

output_width = 400
output_height = 800
output_data = geometric_transform(
    input=input_data,
    mapping=conformal,
    output_shape=(output_height, output_width),
    order=0,
    extra_keywords={
        'input_len':len(input_data),
        'output_len':min(output_width, output_height)
    }
)

f = open('/tmp/warped.png', 'wb')
w = png.Writer(output_width, output_height, greyscale=True)
w.write(f, output_data)
f.close()
