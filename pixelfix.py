from scipy import spatial

neighborLocations = [
    [-1, -1],
    [ 0, -1],
    [ 1, -1],
    [ 1,  0],
    [ 1,  1],
    [ 0,  1],
    [-1,  1],
    [-1,  0]
]

def pixelFix(image):
    image = image.convert('RGBA')
    outputImage = image.copy()

    pointsList = []
    emptyPoints = []
    colors = {}

    for x in range(image.width):
        for y in range(image.height):
            r, g, b, a = image.getpixel((x, y))

            if a != 0:
                for location in neighborLocations:
                    _, _, _, a2 = image.getpixel((x + location[0], y + location[1]))
                    if a2 == 0:
                        pointsList.append((x, y))
                        colors[(x, y)] = (r, g, b)
                        break
            else:
                emptyPoints.append((x, y))
    
    tree = spatial.KDTree(pointsList)
    distances, indexes = tree.query(emptyPoints, workers = -1)
    for point, index in zip(emptyPoints, indexes):
        closestPoint = pointsList[index]

        closestColor = colors[closestPoint]
        outputImage.putpixel((point[0], point[1]), (closestColor[0], closestColor[1], closestColor[2], 0))
    return outputImage