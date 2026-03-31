import random
import string
import time


def bubble_sort(arr):
    a = arr.copy()
    n = len(a)

    comparisons = 0
    swaps = 0

    for i in range(n):
        for j in range(n-i-1):
            comparisons += 1
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swaps += 1

    return a, comparisons, swaps


def selection_sort(arr):
    a = arr.copy()
    n = len(a)
    
    comparisons = 0
    swaps = 0

    for i in range(n):
        min_i = i
        for j in range(i+1, n):
            comparisons += 1
            if a[j] < a[min_i]:
                min_i = j

        a[i], a[min_i] = a[min_i], a[i]
        swaps += 1

    return a, comparisons, swaps

def insertion_sort(arr):
    a = arr.copy()
    comparisons = 0
    swaps = 0 

    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                swaps += 1
                j -= 1
            else:
                break
        a[j + 1] = key
        swaps += 1

    return a, comparisons, swaps

def quick_sort(arr):
    if len(arr) <= 1:
        return arr, 0, 0

    pivot = arr[len(arr)//2]

    
    comparisons = len(arr) * 3
    swaps = 0 

    left_part = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right_part = [x for x in arr if x > pivot]

    left_arr, left_c, left_s = quick_sort(left_part)
    right_arr, right_c, right_s = quick_sort(right_part)

    return left_arr + mid + right_arr, comparisons + left_c + right_c, swaps + left_s + right_s


def merge_sort(arr):
    if len(arr) <= 1:
        return arr, 0, 0

    mid = len(arr)//2

    left_arr, left_c, left_s = merge_sort(arr[:mid])
    right_arr, right_c, right_s = merge_sort(arr[mid:])

    merged, merge_c, merge_s = merge(left_arr, right_arr)
    
    return merged, left_c + right_c + merge_c, left_s + right_s + merge_s


def merge(left, right):
    result = []
    i = j = 0
    
    comparisons = 0
    swaps = 0 

    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
        swaps += 1

    result.extend(left[i:])
    result.extend(right[j:])
    swaps += len(left[i:]) + len(right[j:])

    return result, comparisons, swaps


def heapify(arr, n, i, stats):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n:
        stats[0] += 1
        if arr[left] > arr[largest]:
            largest = left

    if right < n:
        stats[0] += 1
        if arr[right] > arr[largest]:
            largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        stats[1] += 1
        heapify(arr, n, largest, stats)


def heap_sort(arr):
    a = arr.copy()
    n = len(a)
    stats = [0, 0]

    for i in range(n // 2 - 1, -1, -1):
        heapify(a, n, i, stats)

    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        stats[1] += 1
        heapify(a, i, 0, stats)

    return a, stats[0], stats[1]

def counting_sort(arr):
    a = arr.copy()
    if not a: return a, 0, 0
    
    writes = 0
    count = [0] * 256 
    output = [""] * len(a)
    
    for char in a:
        count[ord(char)] += 1
        
    for i in range(1, 256):
        count[i] += count[i - 1]
        
    for i in range(len(a) - 1, -1, -1):
        output[count[ord(a[i])] - 1] = a[i]
        count[ord(a[i])] -= 1
        writes += 1
        
    return output, 0, writes

def python_builtin_sort(arr):
    a = arr.copy()
    a.sort()
    return a, 0, 0

def generate_random_chars(length):
    return [random.choice(string.ascii_letters) for _ in range(length)]


def generate_data(length, data_type):
    arr = generate_random_chars(length)

    if data_type == "sorted":
        arr.sort()

    elif data_type == "reverse":
        arr.sort(reverse=True)

    elif data_type == "almost":
        arr.sort()
        swaps = max(1, int(length * 0.02))

        for _ in range(swaps):
            i = random.randint(0, length-1)
            j = random.randint(0, length-1)
            arr[i], arr[j] = arr[j], arr[i]

    elif data_type == "flat":
        values = ['A', 'B', 'C']
        arr = [random.choice(values) for _ in range(length)]

    return arr


algorithms = {
    1: ("Bubble Sort", bubble_sort),
    2: ("Selection Sort", selection_sort),
    3: ("Insertion Sort", insertion_sort),
    4: ("Quick Sort", quick_sort),
    5: ("Merge Sort", merge_sort),
    6: ("Counting Sort", counting_sort),
    7: ("Python Built-in", python_builtin_sort)
}


def benchmark():
    sizes = [20, 50, 100, 500, 1000]
    types = ["random", "sorted", "reverse", "almost", "flat"]

    overall_stats = {
        key: {"time": 0.0, "comps": 0, "swaps": 0} 
        for key in algorithms
    }
    
    total_scenarios = len(sizes) * len(types)

    print("\n========== BENCHMARK MODE ==========\n")

    for size in sizes:
        for data_type in types:
            print(f"\nData size: {size} | Type: {data_type}")
            print(f"{'Algorithm':<15} | {'Time (s)':<10} | {'Comparisons':<12} | {'Swaps'}")
            print("-" * 55)

            for key, (name, algo) in algorithms.items():
                total_time = 0
                total_comps = 0
                total_swaps = 0
                repeats = 3

                for _ in range(repeats):
                    data = generate_data(size, data_type)

                    start = time.perf_counter()
                    _, comps, swaps = algo(data)
                    end = time.perf_counter()

                    total_time += (end - start)
                    total_comps += comps
                    total_swaps += swaps

                avg_time = total_time / repeats
                avg_comps = total_comps // repeats
                avg_swaps = total_swaps // repeats

                overall_stats[key]["time"] += avg_time
                overall_stats[key]["comps"] += avg_comps
                overall_stats[key]["swaps"] += avg_swaps

                print(f"{name:<15} | {avg_time:.6f}   | {avg_comps:<12} | {avg_swaps}")

    print("\n\n========== OVERALL AVERAGES (ALL TESTS) ==========\n")
    print(f"{'Algorithm':<15} | {'Time (s)':<10} | {'Comparisons':<12} | {'Swaps'}")
    print("-" * 55)

    for key, (name, _) in algorithms.items():
        grand_avg_time = overall_stats[key]["time"] / total_scenarios
        grand_avg_comps = overall_stats[key]["comps"] // total_scenarios
        grand_avg_swaps = overall_stats[key]["swaps"] // total_scenarios
        
        print(f"{name:<15} | {grand_avg_time:.6f}   | {grand_avg_comps:<12} | {grand_avg_swaps}")
    print("\n")

if __name__ == "__main__":
    print("Sorting Experiment Program\n")

    print("1 - Manual Mode")
    print("2 - Benchmark Mode")

    choice = input("Choose mode: ")

    if choice == "1":
        size = int(input("\nEnter data size: "))

        print("\nChoose data type:")
        print("1 - random")
        print("2 - sorted")
        print("3 - reverse")
        print("4 - almost sorted")
        print("5 - flat")

        type_choice = input("Choice: ")

        types = {
            "1": "random", "2": "sorted", "3": "reverse",
            "4": "almost", "5": "flat"
        }
        data_type = types.get(type_choice, "random")

        print("\nChoose algorithm:")
        for key, value in algorithms.items():
            print(f"{key} - {value[0]}")

        algo_choice = int(input("Choice: "))
        name, algorithm = algorithms[algo_choice]
        repeats = int(input("\nHow many repetitions? "))

        total_time, total_comps, total_swaps = 0, 0, 0

        for _ in range(repeats):
            data = generate_data(size, data_type)

            t_start = time.perf_counter()
            _, comps, swaps = algorithm(data)
            t_end = time.perf_counter()

            total_time += (t_end - t_start)
            total_comps += comps
            total_swaps += swaps

        avg_time = total_time / repeats
        avg_comps = total_comps // repeats
        avg_swaps = total_swaps // repeats

        print(f"\n{name} Results (Avg of {repeats} runs):")
        print(f"Time:        {avg_time:.6f} seconds")
        print(f"Comparisons: {avg_comps}")
        print(f"Swaps:       {avg_swaps}")

    elif choice == "2":
        benchmark()