def rectangle(canvas, x0, y0, x1, y1, r, **kwargs):
    points = [
        x0 + r, y0,   # Top-left corner
        x1 - r, y0,   # Top-right corner
        x1, y0 + r,   # Top-right corner round
        x1, y1 - r,   # Bottom-right corner round
        x1 - r, y1,   # Bottom-right corner
        x0 + r, y1,   # Bottom-left corner
        x0, y1 - r,   # Bottom-left corner round
        x0, y0 + r,   # Top-left corner round
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)