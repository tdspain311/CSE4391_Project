"""
Krishna Bhattarai
CSE 4391
The university of texas at Arlington
January 31, 2016
"""
import itertools


"""
This method assumes that the file has vertices and faces only nothing else
"""
def load_txt(file_name):
    mode = "r"
    file_pointer = open(file_name, mode)
    data = file_pointer.readlines()
    file_pointer.close()

    vertices = []
    faces = []
    for each_line in data:
        if each_line[0] == "v":
            # print(each_line)
            vertex_tokens =each_line.strip().split()

            x, y, z = float(vertex_tokens[1]), float(vertex_tokens[2]), float(vertex_tokens[3])
            vertices.append([x, y, z])
        if each_line[0] == "f":
            face_tokens = each_line.strip().split()
            k, l, m = int(face_tokens[1])-1, int(face_tokens[2])-1, int(face_tokens[3])-1
            faces.append([k, l, m])

    VERTICES = list(itertools.chain(*vertices))
    FACES = list(itertools.chain(*faces))
    print("var vertices =", VERTICES, ";")
    # print(len(VERTICES))
    print("var faces = ",FACES, ";")
    # print(len(FACES))

"""
This method assumes that ply only has vertices and faces
normals or colors are not accounted for
"""
def load_ply(file_name):
    with open(file_name) as fp:
        data = fp.readlines()[9:]

        vertices = []
        faces = []
        for each_line in data:
            tokens = each_line.strip().split()
            # print(tokens)

            # assume that faces start with '3' meaning that there are 3 faces in each line

            if tokens[0] == "3" and len(tokens) == 4:
                k, l, m = int(tokens[1]), int(tokens[2]), int(tokens[3])
                faces.append([k, l, m])
            else:

                x, y, z = float(tokens[0]), float(tokens[1]), float(tokens[2])
                vertices.append([x, y, z])

        VERTICES = list(itertools.chain(*vertices))
        FACES = list(itertools.chain(*faces))
        print("var vertices =", VERTICES, ";")
        print(len(VERTICES))
        print("var faces = ",FACES, ";")
        print(len(FACES))

# Name of the txt files
file_name = "pyramid.txt"
# file_name = "cow.txt"
# file_name = "bunny.txt"
# file_name = "teapot.txt"
load_txt(file_name)

# Name of the ply files
# file_name = "weathervane.ply"
# file_name = "ant.ply"
# file_name = "apple.ply"
# file_name = "balance.ply"
# file_name = "big_atc.ply"
# file_name = "big_dodge.ply"
# file_name = "big_porsche.ply"
# file_name = "big_spider.ply"
# file_name = "canstick.ply"
# file_name = "chopper.ply"
# file_name = "dolphins.ply"
# file_name = "pickup_big.ply"
# load_ply(file_name)
