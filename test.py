def variad(*args, has=None, without=None):
    print(type(args))


variad(1, 2, 3, has=4, without=5)
variad(1, has=[4, 5], without=5)
variad(has=[4, 5], without=5)
