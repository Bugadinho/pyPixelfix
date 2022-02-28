from PIL.Image import Image
from joblib import Parallel, delayed
from scipy import spatial

NEIGHBOR_LOCATIONS = [
    [-1, -1],
    [ 0, -1],
    [ 1, -1],
    [ 1,  0],
    [ 1,  1],
    [ 0,  1],
    [-1,  1],
    [-1,  0]
]


def PixelFix(image: Image, threshold: int = 0) -> Image:
    """Function that returns the pixelfixed image.

    Args:
        image (Image): The image to be pixelfixed
        threshold (int, optional): Maximum alpha value to be pixelfixed

    Returns:
        Image: The pixelfixed image
    
    """

    output_image = image.copy().convert('RGBA')

    points_list = []
    empty_points = []
    colors = {}
    any_empty_point = False

    def process_x(x):
        nonlocal output_image
        nonlocal points_list
        nonlocal empty_points
        nonlocal colors
        nonlocal any_empty_point

        for y in range(output_image.height):
            r, g, b, a = output_image.getpixel((x, y))

            if a > threshold:
                for location in NEIGHBOR_LOCATIONS:
                    if (x, y) not in colors and 0 <= x + location[0] <= output_image.width - 1 and 0 <= y + location[1] <= output_image.height - 1:
                        _, _, _, a2 = output_image.getpixel((x + location[0], y + location[1]))
                        if a2 <= threshold:
                            points_list.append((x, y))
                            colors[(x, y)] = (r, g, b)
                            break
            else:
                any_empty_point = True
                empty_points.append((x, y))
    
    Parallel(n_jobs=-2)(delayed(process_x)(x) for x in range(output_image.width))
    
    if any_empty_point == True:
        tree = spatial.KDTree(points_list)
        distances, indexes = tree.query(empty_points, workers = -1)
        for point, index in zip(empty_points, indexes):
            closest_point = points_list[index]

            closest_color = colors[closest_point]
            _, _, _, a = output_image.getpixel((point[0], point[1]))
            
            output_image.putpixel((point[0], point[1]), (closest_color[0], closest_color[1], closest_color[2], a))
    
    return output_image
