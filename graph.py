from cImage import *

blank_graph = EmptyImage(300, 300)
graph_window = ImageWin('Graph', blank_graph.width, blank_graph.height)

for x in range(graph_window.height):
    for y in range(graph_window.width):
        if y == graph_window.height - x:
            pixel = Pixel(0, 0, 0)
            blank_graph.setPixel(x, y, pixel)

blank_graph.draw(graph_window)
graph_window.exitOnClick()
