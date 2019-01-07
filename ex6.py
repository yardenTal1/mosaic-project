import math
import mosaic
from copy import deepcopy
import sys

NUMBER_OF_ARGUMENTS=6


def compare_pixel(pixel1, pixel2):
    '''A function that receive two pixels (tuple with 3 value) and compare the distance between them'''
    distance_pixel = 0
    for color in range(len(pixel1)):
        distance_pixel += math.fabs(pixel1[color] - pixel2[color])
    return distance_pixel


def compare(image1, image2):
    '''
    A function that receive two images (list of lists) and compare
    the distance between them (use with compare_pixel function)
     '''
    distance_image = 0
    height = min(len(image1),len(image2))
    width = min(len(image1[0]),len(image2[0]))
    for h in range(height):
        for w in range(width):
            distance_image += compare_pixel(image1[h][w],image2[h][w])
    return distance_image


def get_piece(image, upper_left, size):
    '''
    A function that receive image (list of lists), upper_left (location of pixel in the original image)
    and size ot the output image. The function return a new image (a list of lists of
     image pixels) that each row is a list of length 'Width' with 'Height' column
    '''
    height, width = size
    row, column = upper_left
    output_image = []
    for r in range(height):
        column_list=[]
        if row+r >= len(image): #If the image exceeds the limits of the original image
            break
        for c in range(width):
            if column+c >= len(image[0]): #If the image exceeds the limits of the original image
                break
            else:
                column_list.append(image[row+r][column+c])
        if len(column_list) != 0:
            output_image.append(column_list)
    return output_image


def set_piece(image, upper_left, piece):
    '''A function that receive image (list of lists), upper_left (like in the previous function) and piece, another
    image. the function changes origin image according to data received.
    '''
    height, width = len(piece), len(piece[0])
    row, column = upper_left
    for r in range(height):
        if row+r >= len(image): #If the image exceeds the limits of the original image
            break
        for c in range(width):
            if column+c >= len(image[0]): #If the image exceeds the limits of the original image
                break
            else:
                image[row+r][column+c]=piece[r][c]


def average(image):
    '''A function that receive image (list of lists) and return the average for each color (red,green,blue) in the image'''
    average_red=0
    average_green=0
    average_blue=0
    height, width= len(image), len(image[0])
    for r in range(len(image)):
        for c in range(len(image[0])):
            red,green,blue = image[r][c]
            average_red+=red
            average_green+=green
            average_blue+=blue
    average_red=average_red/(height*width)
    average_green=average_green/(height*width)
    average_blue=average_blue/(height*width)
    return (average_red,average_green,average_blue)


def preprocess_tiles(tiles):
    '''
    A function that receive a list of tiles (images) and return the average (like in the average function)
    for each tile.
    '''
    list_average_tiles = list()
    for image in tiles:
        average_tiles = average(image)
        list_average_tiles.append(average_tiles)
    return list_average_tiles


def get_best_tiles(objective, tiles, averages , num_candidates):
    '''
    A function that receive objective (image), a list of tiles, averages- a list containing all tile colors average,
    and num of candidates to return. The function return a list (in length num_candidates) of tiles that their colors
     average  is similar to the colors average  of the image.
    '''
    list_average=[]
    list_candidates=[]
    average_objective= average(objective)
    for i in range(len(tiles)):
        list_average.append(compare_pixel(average_objective,averages[i]))
    for num in range(num_candidates):
        if num > len(list_average):
            break
        list_candidates.append(tiles[list_average.index(min(list_average))]) #add to candidates the tiles
        #  wite the most similar average
        list_average[list_average.index(min(list_average))]=max(list_average)+1 #change the best tile to enable find
        #  the best next one
    return list_candidates


def choose_tile(piece, tiles):
    '''A function that receive piece of image and list of tiles (with same size) and return the best tile for changing'''
    list_compare=[]
    for tile in tiles:
        list_compare.append(compare(tile,piece))
    best_tile=tiles[list_compare.index(min(list_compare))] # the best tile is the one with the minimum
    #  distance from the image
    return best_tile


def make_mosaic(image, tiles, num_candidates):
    '''A function that receive image, tiles (in same size) and num candidates, and creates a photomosaic, use with all
    the relevant function.
'''
    image_copy=deepcopy(image)
    average_tiles=preprocess_tiles(tiles)
    height = len(tiles[0])
    width = len(tiles[0][0])
    for r in range(height):
        for c in range(width):
            upper_left =(r*height,c*width) #upper left in eact tile according to its size
            if upper_left[1] >= len(image[0]) or upper_left[0] >= len(image): #If the upper left exceeds the limits
                break
            piece=get_piece(image,upper_left,(height,width))
            filter_tiles=get_best_tiles(piece,tiles,average_tiles,num_candidates)
            tile=choose_tile(piece,filter_tiles)
            set_piece(image_copy,upper_left,tile)
    return image_copy


if __name__ == '__main__':
    if len(sys.argv) == NUMBER_OF_ARGUMENTS:
        image_source= sys.argv[1]
        images_dir = sys.argv[2]
        output_name = sys.argv[3]
        tile_height = int(sys.argv[4]) # given as string
        num_candidates = int(sys.argv[5]) # given as string
        image = mosaic.load_image(image_source)
        tiles = mosaic.build_tile_base(images_dir, tile_height)
        new_image = make_mosaic(image,tiles,num_candidates)
        mosaic.save(new_image,output_name)
    elif len(sys.argv) != NUMBER_OF_ARGUMENTS:
        print('Wrong number of parameters. The correct usage is:' + '\n' +
              'ex6.py <image_source> <images_dir> <output_name> <tile_height> <num_candidates>')






