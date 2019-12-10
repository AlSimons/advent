"""
--- Day 8: Space Image Format ---

The Elves' spirits are lifted when they realize you have an opportunity to
reboot one of their Mars rovers, and so they are curious if you would spend
a brief sojourn on Mars. You land your ship near the rover.

When you reach the rover, you discover that it's already in the process of
rebooting! It's just waiting for someone to enter a BIOS password. The Elf
responsible for the rover takes a picture of the password (your puzzle
input) and sends it to you via the Digital Sending Network.

Unfortunately, images sent via the Digital Sending Network aren't encoded
with any normal encoding; instead, they're encoded in a special Space Image
Format. None of the Elves seem to remember why this is the case. They send
you the instructions to decode it.

Images are sent as a series of digits that each represent the color of a
single pixel. The digits fill each row of the image left-to-right, then move
downward to the next row, filling rows top-to-bottom until every pixel of
the image is filled.

Each image actually consists of a series of identically-sized layers that
are filled in this way. So, the first digit corresponds to the top-left
pixel of the first layer, the second digit corresponds to the pixel to the
right of that on the same layer, and so on until the last digit,
which corresponds to the bottom-right pixel of the last layer.

For example, given an image 3 pixels wide and 2 pixels tall, the image data
123456789012 corresponds to the following image layers:

Layer 1: 123
         456

Layer 2: 789
         012

The image you received is 25 pixels wide and 6 pixels tall.

To make sure the image wasn't corrupted during transmission, the Elves would
like you to find the layer that contains the fewest 0 digits. On that layer,
what is the number of 1 digits multiplied by the number of 2 digits?
"""


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
            if c not in counts:
                counts[c] = 0
            counts[c] += 1
    return counts


def main():
    """
    8-2 will invariably make this more complicated, but for this one, we
    only care about layers.
    :return: None
    """
    with open('8 input.txt') as f:
        pixels = f.readline()

    smallest_num_zeroes = 9999999999999999
    best_layer = None
    layers = layerize(pixels, 6, 25)
    for idx, layer in enumerate(layers):
        num_zeroes = count_characters(layer, ('0'))['0']
        if num_zeroes < smallest_num_zeroes:
            smallest_num_zeroes = num_zeroes
            best_layer = idx

    # Now count the number of ones and twos.
    counts = count_characters(layers[best_layer], ('1', '2'))
    print("There are {} '1's and {} '2's, which multiply to {}".format(
            counts['1'], counts['2'], counts['1'] * counts['2']))


if __name__ == '__main__':
    main()
