"""
--- Part Two ---

Now you're ready to decode the image. The image is rendered by stacking the
layers and aligning the pixels with the same positions in each layer. The
digits indicate the color of the corresponding pixel: 0 is black,
1 is white, and 2 is transparent.

The layers are rendered with the first layer in front and the last layer in
back. So, if a given position has a transparent pixel in the first and
second layers, a black pixel in the third layer, and a white pixel in the
fourth layer, the final image would have a black pixel at that position.

For example, given an image 2 pixels wide and 2 pixels tall, the image data
0222112222120000 corresponds to the following image layers:

Layer 1: 02
         22

Layer 2: 11
         22

Layer 3: 22
         12

Layer 4: 00
         00

Then, the full image can be found by determining the top visible pixel in each
position:

    The top-left pixel is black because the top layer is 0.

    The top-right pixel is white because the top layer is 2 (transparent),
    but the second layer is 1.

    The bottom-left pixel is white because the top two layers are 2, but the
    third layer is 1.

    The bottom-right pixel is black because the only visible pixel in that
    position is 0 (from layer 4).

So, the final image looks like this:

01
10

What message is produced after decoding your image?
"""


def make_into_pic(layer, rows, columns):
    """
    Do two things.
    1. Break into rows of columns length, and
    2. Change '1' (black) into a space and '0' (white) into an 'X'. This is
       being rendered in PyCharm in "Darkula" mode, e.g, a black background.
    :param layer: The merged result layer.
    :param rows: The number of rows in the picture.
    :param columns: Number of columns in each scan line (row) of the picture.
    :return: a list of rows of pixels.
    """
    rows_list = []
    translate_table = str.maketrans('01', ' X')
    for row_idx in range(rows):
        row = layer[row_idx * columns: (row_idx + 1) * columns]
        row_str = ''.join(row)
        translated_row_str = row_str.translate(translate_table)
        rows_list.append(translated_row_str)
    return rows_list


def merge_layers(layers):
    """
    Merge all the layers into one, using the rules:
    - 0 is black, and won't be changed by later layers.
    - 1 is white, and won't be changed by later layers.
    - 2 is "transparent", no action at this time, will be set by a later
      layer.
    :param layers: A list of layers of pixels
    :return: A list the same length as each of the input layers, with the
        merged values, either 0 (black) or 1 (white).
    """
    # All layers are the same length
    layer_len = len(layers[0])

    # Create the result layer and initialize to '2'.
    result = ['2'] * layer_len

    for layer in layers:
        for idx in range(layer_len):
            if result[idx] != '2':
                # This pixel is already set.
                continue
            result[idx] = layer[idx]
    return result


def layerize(pixels, rows, columns):
    """
    Take a stream of pixels and break it into a set of layers of pixels
    :param rows: The number of rows of pixels.
    :param columns: The number of columns in the picture.
    :param pixels: The data stream of pixel values
    :return: a list of layers of pixels.
    """
    pixels_per_layer = columns * rows

    # Check that we have a valid data stream.
    data_len = len(pixels)
    if data_len % pixels_per_layer != 0:
        raise ValueError("The input data stream {} is the wrong length for a "
                         "picture of {} rows by {} columns".format(
                            data_len, rows, columns
                            ))
    layers = []
    for layer_num in range(data_len // pixels_per_layer):
        layers.append(pixels[layer_num * pixels_per_layer:
                             (layer_num + 1) * pixels_per_layer])
    return layers


def count_characters(candidate, characters):
    """
    Count the number of instances of the supplied character in the
    candidate string.
    :param candidate: a string in which to search for the specified character.
    :param characters: a collection of the characters to search for.
    :return: the count of the number of instances of that character.
    """
    counts = {}
    for c in candidate:
        if c in characters:
            try:
                counts[c] += 1
            except KeyError:
                counts[c] = 1
    return counts


def main():
    with open('8 input.txt') as f:
        pixels = f.readline()
    layers = layerize(pixels, 6, 25)
    merged = merge_layers(layers)
    for row in make_int0_pic(merged, 6, 25):
        print(row)


if __name__ == '__main__':
    main()
