def insertion_sort_by_key(items: list[dict], key: str) -> list[dict]:
    """
    Sorts a list of dictionaries in descending order
    using insertion sort based on the given numeric key.
    """

    sorted_items = items.copy()

    for i in range(1, len(sorted_items)):

        current_item = sorted_items[i]

        j = i - 1

        while (
            j >= 0
            and sorted_items[j][key] < current_item[key]
        ):

            sorted_items[j + 1] = sorted_items[j]

            j -= 1

        sorted_items[j + 1] = current_item

    return sorted_items
def binary_search_iterative(
    sorted_titles: list[str],
    target: str
) -> int:

    start = 0
    end = len(sorted_titles) - 1

    while start <= end:

        mid = start + (end - start) // 2

        if sorted_titles[mid] == target:
            return mid

        elif sorted_titles[mid] < target:
            start = mid + 1

        else:
            end = mid - 1

    return -1
def binary_search_recursive(
    sorted_titles: list[str],
    target: str,
    start: int,
    end: int
) -> int:

    if start > end:
        return -1

    mid = start + (end - start) // 2

    if sorted_titles[mid] == target:
        return mid

    elif sorted_titles[mid] < target:

        return binary_search_recursive(
            sorted_titles,
            target,
            mid + 1,
            end
        )

    else:

        return binary_search_recursive(
            sorted_titles,
            target,
            start,
            mid - 1
        )
def linear_search(
    items: list[dict],
    key: str,
    value
) -> dict | None:

    found = False

    result = None

    for item in items:

        if item[key] == value:

            found = True

            result = item

            break

    if found:
        return result

    return None
