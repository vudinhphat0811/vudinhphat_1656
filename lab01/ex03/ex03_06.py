def tim_so_lon_nhat(lst):
    if not lst:
        return None
    max_val = lst[0]
    for num in lst:
        if num > max_val:
            max_val = num
    return max_val

input_list = input("Nhập danh sách các số, cách nhau bằng dấu phẩy: ")
numbers = list(map(int, input_list.split(',')))

so_lon_nhat = tim_so_lon_nhat(numbers)
print("Số lớn nhất trong List là:", so_lon_nhat)