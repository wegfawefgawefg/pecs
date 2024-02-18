def variad(dog, *args, has=None, without=None):
    # throw exception if theres no args
    if not args:
        raise Exception("No args")
    print(f"dog, {dog}, args, {args}, has, {has}, without, {without}")


variad(1, 2, 3, has=4, without=5)
# variad(1, has=[4, 5], without=5)
# variad(has=[4, 5], without=5)


# a = {"a": 3}
# del a["a"]
# print("removed a")
# if "b" in a:
#     del a["b"]
# print("removed b")


# def query(a):
#     if isinstance(a, int):
#         return a
#     return None


# if result := query(a):
#     print(result + 3)


def query_one(a):
    if isinstance(a, int):
        return a, a, a
    return None


if result := query_one(0):
    e, p, v = result


try:
    e, p, v = query_one(0)
except:
    pass

for e, p, v in ecs.query(Position, Velocity):
    p += v
