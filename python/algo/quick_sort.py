def quick_sort(arg):
	if (arg == []): return []
	return quick_sort([i for i in arg[1:] if i<arg[0]]) + [arg[0]] + quick_sort([i for i in arg[1:] if i>arg[0]])
	

print quick_sort([6, 1, 2, 7, 9, 3, 4, 5, 10,8])
