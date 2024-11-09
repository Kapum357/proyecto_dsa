# Sorting Algorithms Implementation
def quick_sort(books, key, low=0, high=None):
    if high is None:
        high = len(books) - 1
    if low < high:
        pi = partition(books, key, low, high)
        quick_sort(books, key, low, pi - 1)
        quick_sort(books, key, pi + 1, high)

def partition(books, key, low, high):
    pivot = getattr(books[high], key)
    i = low - 1
    for j in range(low, high):
        if getattr(books[j], key) <= pivot:
            i += 1
            books[i], books[j] = books[j], books[i]
    books[i + 1], books[high] = books[high], books[i + 1]
    return i + 1

def merge_sort(books, key):
    if len(books) > 1:
        mid = len(books) // 2
        L = books[:mid]
        R = books[mid:]

        merge_sort(L, key)
        merge_sort(R, key)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if getattr(L[i], key) < getattr(R[j], key):
                books[k] = L[i]
                i += 1
            else:
                books[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            books[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            books[k] = R[j]
            j += 1
            k += 1

def binary_search(books, key, value):
    low = 0
    high = len(books) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_val = getattr(books[mid], key)
        if mid_val == value:
            return books[mid]
        elif mid_val < value:
            low = mid + 1
        else:
            high = mid - 1
    return None