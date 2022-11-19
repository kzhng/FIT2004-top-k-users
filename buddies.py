

def read_in_data(file_name):
    """
    this function reads in the the data stored in the given file into a list of size U where U is the number of users.
    It keeps track of the maximum number of characters of all the users and the maximum number of characters for a movie
    for each user. The user's id and movie characters are stored in a list. The user id is at the start of each user's
    list, followed by the movies. The maximum number of characters for a movie for each user is stored at the end. The
    maximum number of characters of all the users is stored at the end of the list containing all the user's data.
    :param file_name:
    :return: a list of the data stored in the file
    :time complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    :space complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    """
    file = open(file_name)
    data_list = []
    max_char = 0
    for line in file:
        user_list = []
        line = line.strip()
        line = line.split(":")
        user_id = int(line[0])
        user_list.append(user_id)
        line = line[1]
        line = line.split(",")
        num_of_movies = len(line)
        users_max_movie_char = 0
        user_total_char = 0
        for i in range(num_of_movies):
            movie = line[i]
            movie_char = len(movie)
            if movie_char > users_max_movie_char:
                users_max_movie_char = movie_char
            user_total_char += movie_char
            movie = [movie]
            user_list.append(movie)
        if user_total_char > max_char:
            max_char = user_total_char
        user_list.append(users_max_movie_char)
        data_list.append(user_list)
    data_list.append(max_char)
    file.close()
    return data_list


def padding_users_movies(users_list):
    """
    This function pads each user's movies with "@" at the end of the movie's string until it has the same string length
    as the maximum character length of a movie for each user. The maximum character of a movie for each user is equal to
    the element stored at the end of a user's data list. This is done so that it is possible to radix sort the user's
    movies. @ was chosen as it has an ascii code of 64, one less than A, because whitespace comes before letters of the
    alphabet when sorting. It also keeps track of the length of the movie name so that we know how much padding we need
    to remove when we print the movie name.
    :param users_list:
    :return: none
    :time complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    :space complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    """
    num_of_users = len(users_list)
    for i in range(num_of_users):
        user_data = users_list[i]
        user_max_char = user_data.pop()
        num_of_movies = len(user_data) - 1
        for j in range(1, num_of_movies + 1):
            movie_name = user_data[j][0]
            movie_name_length = len(movie_name)
            if movie_name_length < user_max_char:
                movie_name += "@" * (user_max_char - movie_name_length)
            user_data[j] = [movie_name, movie_name_length]


def sort_users_movies(users_list):
    """
    This function sorts each user's movies alphabetically by calling the radix_sort_users_movies function U times,
    where U is the number of users.
    :param users_list:
    :return: list of users movies where the movies are sorted alphabetically.
    :time complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    :space complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    """
    number_of_users = len(users_list)
    for x in range(number_of_users):
        user_id = users_list[x][0]
        sorted_user_movies = radix_sort_users_movies(users_list[x], user_id)
        users_list[x] = sorted_user_movies
    return users_list


def radix_sort_users_movies(my_list, user_id):
    """
    this function sorts each user's movies alphabetically with the least significant digit(LSD) radix sort. It uses
    an auxiliary stable sort (counting sort) to sort each column of letters.
    :param my_list:
    :param user_id:
    :return:
    :time complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    :space complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    """
    def list_into_bucket(a_list, column):
        """
        this function sorts each movies by its letter in a given column. The letters are mapped by their ASCII value, in
        that we can get the index for a given letter. Whitepsace and @ (which represents whitespace) are mapped to index
        0, A is mapped to index 1 and so on. To maintain stability, we create a list of 27 lists, and append the movies
        by relative order.
        :param a_list:
        :param column:
        :return: a "bucket" of "buckets" that contain the movies sorted by a given column's letter.
        :time complexity: O(CK) where C is the maximum number of characters for any movie, and K is the maximum number
        of movies liked by a user.
        :space complexity: O(CK) where C is the maximum number of characters for any movie, and K is the maximum number
        of movies liked by a user.
        """
        bucket = [[] for _ in range(27)]
        num_movies = len(a_list) - 1
        for x in range(1, num_movies + 1):
            element = a_list[x]
            movie = element[0]
            char = movie[-column]
            char_num = ord(char) - 64
            if char_num == -32:
                bucket[0].append(element)
            else:
                bucket[char_num].append(element)
        return bucket

    def bucket_into_list(bucket, user_num):
        """
        this function creates an output list, puts the user id at the start of the list, and appends the movies that
        were sorted by the list_into_bucket function starting with the first "bucket" of 27 buckets, maintaining
        relative order.
        :param bucket:
        :param user_num:
        :return: a list that is sorted by the given column's letter in the list_into_bucket function.
        :time complexity: O(K) where K is the maximum number of movies liked by a user.
        :space complexity: O(K) where K is the maximum number of movies liked by a user.
        """
        your_list = [user_num]
        for x in range(27):
            bucket_size = len(bucket[x])
            for y in range(bucket_size):
                movie = bucket[x][y]
                your_list.append(movie)
        return your_list
    users_characters = len(my_list[1][0])
    for a in range(1, users_characters + 1):
        my_list = bucket_into_list(list_into_bucket(my_list, a), user_id)
    return my_list


def remove_padding_of_movies(users_list):
    """
    this function removes the padding that was added to the movie's string that was needed for radix sort. It does this
    by string slicing the difference of the user's maximum character for a movie and the length of the movie name that
    was recorded in the padding_users_movies function.
    :param users_list:
    :return: none
    :time complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    :space complexity: O(1) constant space
    """
    num_of_users = len(users_list)
    for p in range(num_of_users):
        user_data = users_list[p]
        num_of_movies = len(user_data) - 1
        for q in range(1, num_of_movies + 1):
            movie_data = user_data[q]
            movie_name = movie_data[0]
            movie_length = movie_data[1]
            user_data[q] = movie_name[:movie_length]


def concatenate_and_pad_user_movies(users_list, maximum_char):
    """
    for each user, this function concatenates their favourite movies into one big string and then pads the string with
    "@" at the end. The number of @ that are padded onto the concatenated string is the difference between the user with
    the most number of characters used for the favourite movies and the number of characters used for the favourite
    movies for the user in question.
    :param users_list:
    :param maximum_char:
    :return: none
    :time complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    :space complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    """
    number_of_users = len(users_list)
    for s in range(number_of_users):
        user_info = users_list[s]
        concatenated_movies = ""
        number_of_movies = len(user_info) - 1
        user_movie_total_char = 0
        for t in range(1, number_of_movies + 1):
            movie_name = user_info[t]
            movie_length = len(movie_name)
            user_movie_total_char += movie_length
            concatenated_movies += movie_name
        concatenated_movies_with_padding = concatenated_movies + "@" * (maximum_char - user_movie_total_char)
        user_info.append(concatenated_movies_with_padding)


def radix_sort_concatenated_movies(users_list, max_char):
    """
    This function sorts each user's concatenated string of favourite movies alphabetically by implementing the least
    significant digit (LSD) radix sort. It uses an auxiliary stable sort (counting sort) to sort each column of letters.
    :param users_list:
    :param max_char:
    :return: a list that is sorted alphabetically by the concatenated string of favourite movies.
    :time complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    :space complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    """
    def list_into_buckets(data_list, column):
        """
        this function sorts each movies by its letter in a given column. The letters are mapped by their ASCII value, in
        that we can get the index for a given letter. Whitepsace and @ (which represents whitespace) are mapped to index
        0, A is mapped to index 1 and so on. To maintain stability, we create a list of 27 lists, and append the movies
        by relative order.
        :param data_list:
        :param column:
        :return: a "bucket" of "buckets" that contain the movies sorted by a given column's letter.
        :time complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie,
        and K is the maximum number of movies liked by a user.
        :space complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie,
        and K is the maximum number of movies liked by a user.
        """
        bucket = [[] for _ in range(27)]
        num_users = len(data_list)
        for m in range(num_users):
            user_data = data_list[m]
            concatenated_movies = user_data[-1]
            character = concatenated_movies[-column]
            character_num = ord(character) - 64
            if character_num == -32:
                bucket[0].append(user_data)
            else:
                bucket[character_num].append(user_data)
        return bucket

    def buckets_into_list(big_bucket):
        """
        this function creates an output list and appends the user's data that were sorted by the list_into_buckets
        function starting with the first "bucket" of 27 buckets, maintaining relative order.
        :param big_bucket:
        :return: a list that is sorted by the given column's letter in the list_into_bucket function.
        :time complexity: O(U) where U is the number of users.
        :space complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie,
        and K is the maximum number of movies liked by a user.
        """
        the_list = []
        for g in range(27):
            size_of_bucket = len(big_bucket[g])
            for h in range(size_of_bucket):
                user_info = big_bucket[g][h]
                the_list.append(user_info)
        return the_list

    for x in range(1, max_char + 1):
        users_list = buckets_into_list(list_into_buckets(users_list, x))
    return users_list


def group_and_print_movie_buddies(sorted_list):
    """
    this function does a linear scan of the sorted list, and if the concatenated string of favourite movies are the
    same, then we keep checking subsequent elements to see if the concatenated strings are equal until they are not.
    We print the group number, the names of the movies they like, and the user id of the people who like the exact same
    movies. If the function finds that the concatenated string is equal, the first counter is changed to be equal to the
    first element that does not have the same string and the second counter to be the one after. Otherwise, the two
    counters are increased by one for each iteration.
    :param sorted_list:
    :return: none
    :time complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    :space complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    """
    num_users = len(sorted_list)
    group_num = 0
    i = 0
    j = 1
    while i < num_users - 1:
        while j < num_users:
            has_matched = False
            if sorted_list[i][-1] == sorted_list[j][-1]:
                has_matched = True
                group_num += 1
                print("GROUP {}".format(group_num))
                movies = ""
                num_of_movies = len(sorted_list[i]) - 2
                for k in range(1, num_of_movies + 1):
                    movies += "{},".format(sorted_list[i][k])
                print("Movies: {}".format(movies[:-1]))
                buddies = "{},{},".format(sorted_list[i][0], sorted_list[j][0])
                y = j + 1
                while (y < num_users) and (sorted_list[i][-1] == sorted_list[y][-1]):
                    buddies += "{},".format(sorted_list[y][0])
                    y += 1
                print("Buddies: {}\n".format(buddies[:-1]))
            if has_matched:
                i = y
                j = y + 1
            else:
                i += 1
                j += 1


def group_users_by_movies():
    """
    this function calls the above functions to execute the algorithm.
    :return: none
    :time complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    :space complexity: O(UCK) where U is the number of users, C is the maximum number of characters for any movie, and K
    is the maximum number of movies liked by a user.
    """
    data = read_in_data("favoriteMovies.txt")
    max_characters = data.pop()
    padding_users_movies(data)
    sort_users_movies(data)
    remove_padding_of_movies(data)
    concatenate_and_pad_user_movies(data, max_characters)
    data = radix_sort_concatenated_movies(data, max_characters)
    group_and_print_movie_buddies(data)


if __name__ == '__main__':
    group_users_by_movies()
