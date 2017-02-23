def remove_trash(base_list, requirement_list):
    x = 0
    while x < len(base_list):
        if base_list[x] not in requirement_list:
            del(base_list[x])
        else:
            x += 1
    return base_list
