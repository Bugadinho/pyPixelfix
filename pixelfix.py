from PIL.Image import Image
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

    image = image.convert('RGBA')
    output_image = image.copy()

    points_list = []
    empty_points = []
    colors = {}
    any_empty_point = False

    for x in range(image.width):
        for y in range(image.height):
            r, g, b, a = image.getpixel((x, y))

            if a > threshold:
                for location in NEIGHBOR_LOCATIONS:
                    if 0 <= x + location[0] <= image.width - 1 and 0 <= y + location[1] <= image.height - 1:
                        _, _, _, a2 = image.getpixel((x + location[0], y + location[1]))
                        if a2 <= threshold:
                            points_list.append((x, y))
                            colors[(x, y)] = (r, g, b)
                            break
            else:
                any_empty_point = True
                empty_points.append((x, y))
    
    if any_empty_point == True:
        tree = spatial.KDTree(points_list)
        distances, indexes = tree.query(empty_points, workers = -1)
        for point, index in zip(empty_points, indexes):
            closest_point = points_list[index]

            closest_color = colors[closest_point]
            _, _, _, a = image.getpixel((point[0], point[1]))
            
            output_image.putpixel((point[0], point[1]), (closest_color[0], closest_color[1], closest_color[2], a))
    
    return output_image
