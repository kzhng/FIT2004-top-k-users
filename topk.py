

def read_in_data(file_name):
    """
    this function reads in the data from a given file into a list of size n where n is the number of users.
    each user's data is represented by a tuple where the first element is their id and the second element is their time
    spent on the app.
    :param file_name:
    :return: list of data from file
    :time complexity: O(N) where N is the number of users
    :space complexity: O(N) where N is the number of users
    """
    file = open(file_name)
    data_list = [None]
    for line in file:
        line = line.strip()
        line = line.split(":")
        user_id = int(line[0])
        time_spent = int(line[1])
        user_data = (user_id, time_spent)
        data_list.append(user_data)
    file.close()
    return data_list


def heapify(my_list):
    """
    this function heapifys the list using the sift_down method into a max heap. It works by starting from the last
    parent node and calls the sift_down method iteratively up to the first parent node(the root).
    :param my_list
    :return: a max heap
    :time complexity: O(N) where N is the number of users
    :space complexity: O(1) constant space
    """
    count = len(my_list) - 1
    sub_root = count // 2
    while sub_root >= 1:
        sift_down(my_list, sub_root, count)
        sub_root -= 1
    return my_list


def sift_down(a_list, root, count):
    """
    this function calls the largest_child function to get the largest child of the parent(root), and swaps the root that
    is smaller than its largest child with the largest child until the parent is at least larger than both of its child,
    or has a smaller user id than the largest child if the time spent on the app is the same.
    :param a_list: the list of elements in which we are trying to heapify
    :param root: the root of the heap structure
    :param count: size of the heap
    :return: none
    :time complexity: O(log N) where N is the number of users
    :space complexity: O(1) constant space
    """
    parent = root
    while 2*parent <= count:
        left_child = 2*parent
        largest_child = find_largest_child(a_list, parent, left_child, count)
        if a_list[parent][1] > a_list[largest_child][1]:
            return
        elif (a_list[parent][1] == a_list[largest_child][1]) and (a_list[parent][0] < a_list[largest_child][0]):
            return
        else:
            swap(a_list, parent, largest_child)
            parent = largest_child


def find_largest_child(a_heap, parent, left_child, count):
    """
    this function first determines if the parent has a right child. If it doesn't, then the largest child is the left
    child. If it does, then we compare the time spent on the app of the two children. Whoever has a higher time spent
    is the largest child. If the time spent is equal, then the largest child is the one with the smaller user id.
    Returns the array position of the largest child.
    :param a_heap: the array that stores the heap
    :param parent: array position of the parent
    :param left_child: array position of the heap
    :param count: number of nodes in the heap
    :return: the largest child of the parent
    :time complexity: O(1) constant time
    :space complexity: O(1) constant space
    """
    if 2 * parent + 1 <= count:
        right_child = 2 * parent + 1
        if a_heap[left_child][1] > a_heap[right_child][1]:
            largest_child = left_child
        elif a_heap[right_child][1] > a_heap[left_child][1]:
            largest_child = right_child
        else:
            if a_heap[left_child][0] < a_heap[right_child][0]:
                largest_child = left_child
            else:
                largest_child = right_child
    else:
        largest_child = left_child
    return largest_child


def swap(an_array, i, j):
    """
    this function swaps the element at position i with the element at position j
    :param an_array: an array
    :param i: position i
    :param j: position j
    :return: none
    :time complexity: O(1) constant time
    :space complexity: O(1) constant space
    """
    an_array[i], an_array[j] = an_array[j], an_array[i]


def get_max(my_heap, count, a):
    """
    this function gets the max node of the heap, which is at the root, and swaps it with the last node of the heap. It
    prints the maximum node's user id and time spent. Then it calls the sift_down method on the node at the root until
    the heap property is satisfied where the parent is at least larger than both of its parents.
    :param my_heap:
    :param count:
    :param a:
    :return: none
    :time complexity: O(log N) where N is the number of users
    :space complexity: O(1) constant space
    """
    max_element = my_heap[1]
    print("#{}: User ID: {} Time spent: {}".format(a, max_element[0], max_element[1]))
    swap(my_heap, 1, count)
    count -= 1
    sift_down(my_heap, 1, count)


def get_topk_users():
    """
    this function calls the above functions. It calls the get_max function k times, top get the top-k users of time
    spent on the app, where k is the number given by the user.
    :raises: ValueError if 1 > k > N, where N is the number of users.
    :return: none
    :time complexity: O(N log k). Since k <= N, a tighter upper bound time complexity is O(k log N)
    :space complexity: O(1) constant space
    """
    data_list = read_in_data("timeSpent.txt")
    data_heap = heapify(data_list)
    count = len(data_heap)
    k = int(input("Enter the value of k: "))
    if not 1 <= k <= count - 1:
        raise ValueError("invalid input for k")
    for x in range(1, k + 1):
        get_max(data_heap, count-x, x)


if __name__ == '__main__':
    get_topk_users()
