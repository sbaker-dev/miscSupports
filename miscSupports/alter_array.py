from itertools import groupby, chain
from collections import Counter
import numpy as np


def flatten(list_of_lists):
    """
    Flatten a list of lists into a list
    """
    return list(chain(*list_of_lists))


def chunk_list(list_to_chunk, chunk_length):
    """
    Returns n-sized chunks from list.
    """
    return [list_to_chunk[i:i + max(1, chunk_length)] for i in range(0, len(list_to_chunk), max(1, chunk_length))]


def find_duplicates(list_to_check):
    """
    This finds duplicates in a list of values of any type and then returns the values that are duplicates. Given Counter
    only works with hashable types, ie it can't work with lists, create a tuple of the lists and then count if the
    list_to_check contains un-hashable items

    :param list_to_check: A list of values with potential duplicates within it
    :type list_to_check: list

    :return:The values that where duplicates
    :rtype: list
    """
    try:
        counted_list = Counter(list_to_check)
    except TypeError:
        counted_list = Counter([tuple(x) for x in list_to_check])

    return [key for key in counted_list if counted_list[key] > 1]


class Key:
    def __init__(self, diff):
        """
        This callable class acts as the key for group-by to construct a consecutive list of 0, 1s so that group-by can
        then group elements into groups where groups are defined as a consecutive key.

        :param diff: The tolerance gap allowed between the individual elements in the list
        """
        self.diff = diff
        self.flag = [0, 1]
        self.prev = None

    def __call__(self, elem):
        """
        # Source https://stackoverflow.com/questions/21142231/group-consecutive-integers-and-tolerate-gaps-of-1

        The way this works is that the key is the acting as a function because of the call. The call is called on each
        individual item in a list. For the first item, there is no previous item so it takes the none defined in the
        __init__. Otherwise, at the end of each call self.prev is assigned the current value so it is kept in memory.

        The diff is user defined, its the tolerance or maximum distance allowed between items. If set to zero, all items
        are set to there own sub group. The elem is the current element that has been taken for group by. The flag could
        be many things, but is designed to be toggle. When something meets the diff criteria then we want to invert our
        flag so we create the separation.

        Example

        Lets say i have a list of the following [1, 2, 5, 6, 9, 10] and i want to group them with a tolerance of 1
        The group-by instance that will call this method is for loop or sorts. So the elem is 1, self.prev has not yet
        been re-defined so it is None and we add this element to our sub group with a given flag. The next element 2 is
        then brought in and now we have a previous element to compare to. We check our condition of self.prev - elem
        and we get a value of 1. 1 is not greater than the tolerance we set of 1 so we add this to our sub list and
        update the self.prev to 2. Then we bring in the next element of 5, here 5 - 2 is greater than 1 so we want to
        change the flag.

        The changes of the flag means we end up with a list of 0, 0, 1, 1, 0, 0. Group-by then uses these keys to group
        the individual components by the same consecutive elements with the same keys. So this results in the list being
        group currently as [[1, 2], [5, 6], [9, 10]]

        :param elem: The current element from the given list
        :type elem: int, float
        :return: The first instance of the key to construct the consecutive element list for group-by to use.
        :rtype: int
        """

        if self.prev and abs(self.prev - elem) > self.diff:
            self.flag = self.flag[::-1]

        self.prev = elem
        return self.flag[0]


def group_adjacent(list_to_group, distance=1):
    """
    This is the call method to group elements by constructing a chain of consecutive keys via the Key callable class
    method that are within a given distance of each other
    """
    return [list(g) for k, g in groupby(list_to_group, key=Key(distance))]


def in_between_list(points, subdivision):
    """
    This takes a list of floats or ints and returns a list with a number of sub-divisions between each element
    :param points: A list of points
    :param subdivision: Number of sub-divisions between each pair of points
    :return: list of points with subdivisions
    """

    # Numpy is inclusive, so if the user wants 5 subdivisions then by default only 3 points would be added
    subdivision = subdivision + 2

    # Use numpy to in-between by the number of subdivisions for each element in the list to its previous element
    spaced_lists = [np.linspace(points[i - 1], v, subdivision).tolist() for i, v in enumerate(points) if i > 0]

    # As the numpy lists are inclusive the last point of ever sub list bar the last will be a duplicate so we remove it
    list_return = [spaced[:-1] if i != len(spaced_lists) - 1 else spaced for i, spaced in enumerate(spaced_lists)]

    # Return the flattened list
    return flatten(list_return)


def in_between_points_list(points, subdivision):
    """
    This will in-between a list of points, where it will add a number of points equal to subdivisions between each point

    :param points: A list of points, that may be Tuples or Lists or (x, y) or Vector2D.
    :type points: list

    :param subdivision: The number of points to add between each set of points
    :type subdivision: int

    :return: A list of Vector2D points
    :rtype: list[Vector2D]
    """

    # Create a number of points equal to subdivision between each point
    sub_divided = []
    for index, point in enumerate(points):
        if index == 0:
            sub_divided.append(point)
        else:
            for sub in point.sub_divide(points[index - 1], subdivision, from_self=False, include_points=False):
                sub_divided.append(sub)
            sub_divided.append(point)
    return sub_divided


def in_between_points_on_list(points_list, divisions):
    """
    This takes a list of numerical values (floats or ints) and a list of divisions of ints of (points_list) - 1. This
    method will then uses the number of sub divisions within the list of divisions to add new points to the points list
    where you have request them

    Example
    ----------
    points_list = [5, 10, 12.5]
    divisions = [1, 0]
    values = in_between_points_on_list(points_list, divisions) = [5, 7.5, 10, 12.5]

    :param points_list: List of points to be in-between
    :param divisions: list of ints that shows the number of divisions to apply between a given pair of points. Needs to
        be of length points_list - 1
    :return: List of points with added points
    """
    points_out = []
    for index, point in enumerate(points_list):
        if index > 0 and divisions[index - 1] > 0:
            # Get the value to multiple by an index to get the subdivisions
            sub_points = (points_list[index] - points_list[index - 1]) / (divisions[index - 1] + 1)

            # multiple the sub_points values by 1, 2, N etc and add it to the previous entry into the list of points
            for ii in range(1, divisions[index - 1] + 2):
                points_out.append(points_list[index - 1] + (sub_points * ii))

        else:
            points_out.append(point)
    return points_out


def flip_list(list_of_lists, length_return=False):
    """
    This will take a list of lists, and then flip it. It requires all sub lists to be the same length.
    """
    list_of_keys = Counter([len(sub_list) for sub_list in list_of_lists])
    sub_key_length = list(list_of_keys.keys())

    assert len(list_of_keys.keys()) == 1, f"Sub lists should be all of the same length yet found lengths" \
                                          f"{sub_key_length}"
    if length_return:
        return [[sub[i] for sub in list_of_lists] for i in range(sub_key_length[0])], sub_key_length[0]
    else:
        return [[sub[i] for sub in list_of_lists] for i in range(sub_key_length[0])]


def spaced_points(points_list, return_spacing=False):
    """
    Spaces a list of points based on the average distance between each point

    This will create a spacing parameter base on the average distance between each numeric in a list of numeric, and
    create a new list with spacing to ensure there is no gap larger than the spacing parameter. This **does not**
    produce an  equally spaced list, as this keeps the original elements. If you want the spacing returned you can pass
    True to the second parameter, else only the spaced list will be returned
    """
    # We use the average distance between each point to get a length for rough spacing between the edge loops
    distance_y = [points_list[i] - points_list[i - 1] for i in range(len(points_list)) if i > 0]
    spacing = np.mean(distance_y)

    # This is the number of subdivisions between each ordered y intersection that is required
    subdivisions = [int((points_list[i] - points_list[i - 1]) / spacing) for i in range(1, len(points_list))]

    # Now we space the region between the min and max of our points of intersection with the spacing
    points_spaced = in_between_points_on_list(points_list, subdivisions)

    if return_spacing:
        return spacing, points_spaced
    else:
        return points_spaced
