import numpy as np

def get_angle(a, b, c):
    """
    Calculates the angle between three points a, b, c.
    Points should be (x, y) tuples or arrays.
    """
    # Using arctan2 for correct quadrant handling
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(np.degrees(radians))
    return angle

def get_distance(landmark_list):
    """
    Calculates the distance between the first two points in the list.
    Returns a value interpolated from [0, 1] to [0, 1000].
    """
    if len(landmark_list) < 2:
        return 0
    
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
    
    # Calculate Euclidean distance
    l = np.hypot(x2 - x1, y2 - y1)
    
    # Interpolate from [0, 1] to [0, 1000]
    # Note: This assumes input coordinates are normalized [0, 1].
    # If using pixel coordinates, this range might need adjustment.
    return np.interp(l, [0, 1], [0, 1000])
