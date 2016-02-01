# Bhattarai, Krishna
# 1000-793-292
# 2015-03-17
# Assignment_05

import sys
import OpenGL

from OpenGL.GL import *     
from OpenGL.GLU import *    
from OpenGL.GLUT import *
from tkinter import *
from tkinter import filedialog
import math

# global variables
total_data = []
count = 1 # for parallel or perspective count

camera_list = [] # this is a global list that gets populated by load data method
# 2d list of camera objects
# End of global variable declarations



class Camera:
    """
    This is my camera class, it has all the features of the camera_05.txt file and it can handle them all
    """
    def __init__(self):
        self.camera_name = "dummy_name"             # Default = ""
        self.projection = "parallel"                # Default = "parallel"
        self.eye = []                               # eye = [x, y, z]
        self.look_at = []                           # look at point =[x, y, z]
        self.vup = []                               # View UP = [x, y, z]
        self.vrc = []                               # Default [-1, 1, -1, 1, -1, 1]
        self.viewport = []                          # Default [0.1, 0.1, 0.9, 0.9]

        self.VPN = []                               # VPN is view point normal vector which is: eye - look_at
        self.normalized_VPN = []                    # this is the Normalized VPN
        self.distance = 1                           # this is the distance between eye and look_at

def display():
    """
    this method display() needs to reload the camera file and
    reset all the viewing coordinates
    :return:
    """
    global camera_list      # receive the global camera list
    # a list of 2d camera objects

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the buffer
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)

    # Experimentation
    glColor3f(0.0, 0.0, 0.0)                # to draw black lines
    for co in camera_list:                  # for camera object in the 2d camera_list
        glEnable(GL_SCISSOR_TEST)
        glScissor(int(w * co.viewport[0]), int(h * co.viewport[1]), int(w *(co.viewport[2] - co.viewport[0])), int(h *(co.viewport[3] - co.viewport[1])))
        glClearColor(co.viewport[2], co.viewport[0], co.viewport[3], co.viewport[1])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if co.projection == "parallel":
            glOrtho(co.vrc[0], co.vrc[1], co.vrc[2], co.vrc[3], co.vrc[4], co.vrc[5])       # for parallel projection I am using ortho
        elif co.projection == "perspective":
            glFrustum(co.vrc[0], co.vrc[1], co.vrc[2], co.vrc[3], co.vrc[4], co.vrc[5])     # for perspective projection I am using Frustum
        gluLookAt(co.eye[0], co.eye[1], co.eye[2], co.look_at[0], co.look_at[1], co.look_at[2], co.vup[0], co.vup[1], co.vup[2] )
        glMatrixMode(GL_MODELVIEW)
        glViewport(int(w * co.viewport[0]), int(h * co.viewport[1]), int(w *(co.viewport[2] - co.viewport[0])), int(h *(co.viewport[3] - co.viewport[1])))
        glCallList(3)
        glFlush()
    # end of experimentation


    glutSwapBuffers()



def make_camera_object(camera1d):
    """
    receives a 1d list of raw camera data and makes it camera object and returns it
    :param camera1d: ['', 'front', 'parallel', '0 0 4', '0 0 -1', '0 1 0', '-4 4 -4 4 -20 100', '0.1 0.1 0.4 0.4']
    :return: 1 camera object with all the properties
    """
    #ignore the '' camera1d[0] item its useless
    camera_name = camera1d[1]
    if camera1d[2] == "parallel":
        projection = "parallel"
    elif camera1d[2] == "perspective":
        projection = "perspective"

    eye_data = camera1d[3].split()
    eye = [int(eye_data[0]), int(eye_data[1]), int(eye_data[2])]

    look_at_data = camera1d[4].split()
    if (len(look_at_data) == 2):
        nl = list(look_at_data[1])
        look_at = [int(look_at_data[0]), int(nl[0]), int(nl[1]) ]
    else:
        look_at = [int(look_at_data[0]), int(look_at_data[1]), int(look_at_data[2]) ]

    vup_data = camera1d[5].split()
    vup = [int(vup_data[0]), int(vup_data[1]), int(vup_data[2])]

    vrc_data = camera1d[6].split()
    vrc = [int(vrc_data[0]),int(vrc_data[1]), int(vrc_data[2]),int(vrc_data[3]),int(vrc_data[4]), int(vrc_data[5])]

    vp_data = camera1d[7].split()
    viewport = [float(vp_data[0]),float(vp_data[1]), float(vp_data[2]),float(vp_data[3])]

    ### FIND VPN AND NORMALIZED VPN

    #VPN = look_at - eye
    VPN = sub(look_at, eye)
    normalized_VPN = unit_vector(VPN)
    distance = find_distance(eye, look_at)

    mycamera = Camera() # initialize the camera class

    # assign the values of the camera to the instance of  camera class (camera_data()) mycamera
    mycamera.camera_name = camera_name
    mycamera.projection = projection
    mycamera.eye = eye
    mycamera.look_at = look_at
    mycamera.vup = vup
    mycamera.vrc = vrc
    mycamera.viewport = viewport
    mycamera.VPN = VPN
    mycamera.normalized_VPN = normalized_VPN
    mycamera.distance = distance

    #print ("camera name = ", mycamera.camera_name)
    #print ("camera projection = ", mycamera.projection)
    # print ("camera eye= ", mycamera.eye)
    # print ("camera lookat  = ", mycamera.look_at)
    # print ("camera vup = ", mycamera.vup)
    # print ("camera vrc = ", mycamera.vrc)
    # print ("camera viewport = ", mycamera.viewport)
    # print ("camera VPN = ", mycamera.VPN)
    # print("Normalized VPN =", mycamera.normalized_VPN)
    #print("distance =", mycamera.distance)

    #print(" ")
    return mycamera


def sub(A, B):
    return [A[0]-B[0], A[1]-B[1], A[2]-B[2]]

def magnitude(vector):
    x, y, z = vector[0], vector[1], vector[2]
    mag = math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2))
    return mag

def unit_vector(vector):
    mag = magnitude(vector)
    x = vector[0]/mag
    y = vector[1]/mag
    z = vector[2]/mag
    return [x, y, z]

def find_distance(a, b):
    """
    :param a:  [x1, y1, z1]
    :param b:  [x2, y2, z2]
    :return: sqrt ( (x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2 ) )
    """
    x1, y1, z1 = a[0], a[1], a[2]
    x2, y2, z2 = b[0], b[1], b[2]
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2) + math.pow((z2 - z1), 2))

def cross_product(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]
    return c

def load_cameras():
    """
    Opens the camera file and does little bit of dirty job
    :return:#returns a 2d list of cameras raw data. They are still strings they need to be tokenized
    """
    filename = "cameras_05.txt"
    mode = "r"
    fp = open(filename, mode) # fp means file pointer
    s = []
    for line in fp:
        s.append(line)
    n = []
    for each_item in s:
        new_item = each_item.strip()
        n.append(new_item)

    size = len(n)
    total_cameras = int(size/8)
    fp.close()
    data = []
    i = 0
    while i < size:
        cam = []
        cam = n[i:i+8]
        data.append(cam)
        i += 8
    newd =[]
    for i in range(0, len(data)):
        one_d=[]
        for items in data[i]:
            #print (items, type(items))
            first = items[1:].strip()
            one_d.append(first)
        newd.append(one_d)

    return newd

def dirty_job(filename):
    """
    :param filename: receives a filename and does all the dirty job that needs to be done
    :return: returns a 2d list; my_data = [[vertices], [faces]]
    """
    fp = open(filename, "r") # open the file with filepointer
    v, f = [], []
    vertices, faces = [], []
    my_data = []
    for line in fp.readlines():
        #strip the line to remove whitespace
        line = line.strip() # this strips any extra spaces
        line = line.split() # this tokenizes and puts everything into list
        #print (line)
        if (line != []): # some times some lines in the file might be empty
            if (line[0] == "v"):
                v.append(line[1:])
            if (line[0] == "f"):
                f.append(line[1:])

    for ev in v: # for each 1D list in the 2D list of v
        newV = [float(ev[0]), float(ev[1]), float(ev[2])]
        vertices.append(newV) # so now they look like [x, y, z, 1]

    for ef in f: # for each 1d list in the 2D list of f
        if (len(ef) == 3):
            newF = [int(ef[0])-1, int(ef[1])-1, int(ef[2])-1] # automatically reducing 1 from each items in faces
        elif (len(ef) == 4):
            newF = [int(ef[0])-1, int(ef[1])-1, int(ef[2])-1, int(ef[3])-1]
        faces.append(newF)

    fp.close()
    my_data.append(vertices)
    my_data.append(faces)
    return my_data

def input_file():
    """
    This command loads all the data and parameters from a text file.
    Hitting the "n" key should prompt the user for the name of the file.
    (The default value for the file name should be "pyramid_05.txt")
    :return:
    """
    root = Tk()                                         # initialize the tkinter root
    root.withdraw()                                     # put the root on the background
    filename = filedialog.askopenfilename()             # prompt the user for the filename
    print("The filename that you entered is", filename)
    my_data = dirty_job(filename)
    return my_data

def load(my_data):
        """
        this command should load . Hitting the "d" key should load
        the input file and and redisplay all the viewports.Notice that this command should reload
        the "cameras_05.txt" file and reset all the viewing coordinates.
        :parameter: it recieves a 2d list. First 1d list is vertices, second 1d list is faces
        :return:
        """
        global camera_list                    # the global list of camera objects

        cameras2d = load_cameras()

        for each_camera in cameras2d:
            camera_objects = make_camera_object(each_camera)
            camera_list.append(camera_objects)
        # global camera_list now is a 2d list of camera objects

        vertices = my_data[0]
        faces = my_data[1]

        glNewList(3, GL_COMPILE)
        #glBegin(GL_LINE_STRIP) # Draws a connected group of line segments from the first vertex to the last. Best so far
        glBegin(GL_LINES)
        for each_face in faces:
            k, l, m = each_face[0], each_face[1], each_face[2] # f = [k, l, m] , where k, l, m are vertices
            # draw (k,l) and (l,m), and (k,m)
            # do k and l
            glVertex3f(vertices[k][0], vertices[k][1], vertices[k][2])
            glVertex3f(vertices[l][0], vertices[l][1], vertices[l][2])
            # do l and m
            glVertex3f(vertices[l][0], vertices[l][1], vertices[l][2])
            glVertex3f(vertices[m][0], vertices[m][1], vertices[m][2])
            # do k and m
            glVertex3f(vertices[k][0], vertices[k][1], vertices[k][2])
            glVertex3f(vertices[m][0], vertices[m][1], vertices[m][2])
        glEnd()
        glEndList()



def keyHandler(Key, MouseX, MouseY):
        """
        :param Key: The user enter the key in the keyboard
        :return: None
        """
        global total_data
        global count
        global camera_list                    # the global list of camera objects
        # trial
        # dummy = input_file()
        # load(dummy)
        # end trial
        if Key == b'n' or Key == b'N':
            print (b"Prompting the User for input file")
            glMatrixMode(GL_MODELVIEW)  # clear the modelview matrix
            glLoadIdentity()            # load identity
            total_data = input_file()   # get the data from the input_file method # total_data  = [[vertices], [faces]]

        elif Key == b'd' or Key == b'D':
            load(total_data)            # Actually send the data into the global list called total_data, so it can be displayed

        elif Key == b'x' or Key == b'X':
            if Key == b'x':
                glRotated(5, 1, 0, 0)
            if Key == b'X':
                glRotated(-5, 1, 0, 0)

        elif Key == b'y' or Key == b'Y':
            if Key == b'y':
                glRotated(5, 0, 1, 0)
            if Key == b'Y':
                glRotated(-5, 0, 1, 0)

        elif Key == b'z' or Key == b'Z':
            if Key == b'z':
                glRotated(5, 0, 0, 1)
            if Key == b'Z':
                glRotated(-5, 0, 0, 1)

        elif Key == b's' or Key == b'S':
            if Key == b's':
                glScaled(1.05, 1.05, 1.05)
            if Key == b'S':
                glScaled(1/1.05, 1/1.05, 1/1.05)

        elif Key == b'f' or Key == b'b':
            if Key == b'f':
                # Hitting the "f" Key should move the eye toward the Look at point
                #  by 0.05 of the distance between the eye and look at point.
                print ("moving eye toward look at by 0.05 of the distance between eye and look at")
                """
                1)find look_at - eye
                diff_vector = sub(lookat - eye) == [lookat[0] - eye[0], lookat[1] - eye[1], lookat[2] - eye[2]]
                now normalize the difference vector
                2) normalized_diff_vector =  (1/sqrt(magnitude(diff_vector)) ) * [diff_vector]
                3) eye = eye + (0.05 % of normalized-diff_vector)

                """
            # newdist = [0, 0, 0, 0]
            normalized_vpn =[0, 0, 0]
            new_eye = [0, 0, 0]
            for co in camera_list:

                newd = co.distance * 0.05

                normalized_vpn[0] = newd*co.normalized_VPN[0]
                normalized_vpn[1] = newd*co.normalized_VPN[1]
                normalized_vpn[2] = newd*co.normalized_VPN[2]

                new_eye[0] = co.eye[0] + normalized_vpn[0]
                new_eye[1] = co.eye[1] + normalized_vpn[1]
                new_eye[2] = co.eye[2] + normalized_vpn[2]
                #print (new_eye) # I know this works
                co.eye = new_eye # set the camera objects eye to the new_eye that i calculated and display

            normalized_vpn =[0, 0, 0]
            new_eye = [0, 0, 0]
            if Key == b'b':
                #Hitting the "b" Key should move the eye away from the Look at point
                # by 0.05/1.05 of the distance between the eye and look at point.
                # print ("moving eye away from look at by 0.05/1.05 of the distance between eye and look at")
                newd = co.distance * (0.05 / 1.05)

                normalized_vpn[0] = newd* co.normalized_VPN[0]
                normalized_vpn[1] = newd* co.normalized_VPN[1]
                normalized_vpn[2] = newd* co.normalized_VPN[2]

                new_eye[0] = co.eye[0] + normalized_vpn[0]
                new_eye[1] = co.eye[1] + normalized_vpn[1]
                new_eye[2] = co.eye[2] + normalized_vpn[2]
                #print (new_eye) # I know this works
                co.eye = new_eye # set the new eye to be the camera objects eye


        elif Key == b'p': # perspective or parallel
            #Hitting the "p" key should switch the views between parallel and perspective projections
            if count % 2 == 0:
                print("Switching to parallel")
                for co in camera_list:                 # for camera object in the 2d camera_list
                    co.projection = "parallel"

            else:
                print("Switching to perspective")
                for co in camera_list:                 # for camera object in the 2d camera_list
                    co.projection = "perspective"

            count = count + 1

        elif Key == b'q' or Key == b'Q':
            print ("Bye")
            sys.exit()

        else:
            print ("Invalid Key ",Key)
        return

def special(key, x, y):
    if key == GLUT_KEY_UP:
        print("You pressed up")
        print ("moving the eye in the positive direction of the view coordinate v axis by 0.05 of the distance " \
              "between the eye and the look at point")
        #  Hitting the "up arrow" Key should move the eye in the positive direction of the view
        #  coordinate v axis by 0.05 of the distance between the eye and look at point.
        """
        1)find look_at - eye?
        diff_vector = sub(lookat - eye) == [lookat[0]  eye[0], lookat[1]  eye[1], lookat[2] - eye[2]] # because we want to move away
        now normalize the difference vector
        2) normalized_diff_vector =  (1/sqrt(magnitude(diff_vector)) ) * [diff_vector]
        3)cross product of vup and normalized vector #######
        4) move eye of x by 0.05 of cross product
        i.e : eyex = eyex + (0.05 % of cross product )
        """
        up = [0, 0, 0]
        new_eye = [0, 0, 0]
        for co in camera_list:# n is the normalized VPN
            u_prime = unit_vector(cross_product(co.normalized_VPN, co.vup)) # find the cross product of vp and vup and normalize it
            v_prime = unit_vector(cross_product(co.normalized_VPN, u_prime))
            n_prime = unit_vector(cross_product(co.normalized_VPN, v_prime)) # this one may be wrong. Professor might have said something else

            newd = co.distance * 0.05

            up[0] = v_prime[0] * newd
            up[1] = v_prime[1] * newd
            up[2] = v_prime[2] * newd

            new_eye[0] = up[0] + co.eye[0]
            new_eye[1] = up[1] + co.eye[1]
            new_eye[2] = up[2] + co.eye[2]

            co.eye = new_eye


    elif key == GLUT_KEY_DOWN:
        down = [0, 0, 0]
        new_eye = [0, 0, 0]
        print("You pressed down")
        print ("moving the eye in the negative direction of the view coordinate v axis by 0.05 of the distance " \
              "between the eye and the look at point")
        # Hitting the "down arrow" Key should move the eye in the negative direction of the view
        # coordinate v axis by 0.05 of the distance between the eye and look at point.
        for co in camera_list:# n is the normalized VPN
            u_prime = unit_vector(cross_product(co.normalized_VPN, co.vup)) # find the cross product of vp and vup and normalize it
            v_prime = unit_vector(cross_product(co.normalized_VPN, u_prime))
            n_prime = unit_vector(cross_product(co.normalized_VPN, v_prime)) # this one may be wrong. Professor might have said something else

            newd = co.distance * 0.05

            down[0] = v_prime[0] / newd
            down[1] = v_prime[1] / newd
            down[2] = v_prime[2] / newd

            new_eye[0] = down[0] + co.eye[0]
            new_eye[1] = down[1] + co.eye[1]
            new_eye[2] = down[2] + co.eye[2]

            co.eye = new_eye

    elif key == GLUT_KEY_LEFT:
        left = [0, 0, 0]
        new_eye = [0, 0, 0]
        print("You pressed left")
        print ("moving the eye in the positive direction of the view coordinate u axis by 0.05 of the distance " \
              "between the eye and the look at point")
        #Hitting the "left arrow" Key should move the eye in the positive direction
        # of the view coordinate u axis by 0.05 of the distance between the eye and look at point.
        for co in camera_list:# n is the normalized VPN
            u_prime = unit_vector(cross_product(co.normalized_VPN, co.vup)) # find the cross product of vp and vup and normalize it
            v_prime = unit_vector(cross_product(co.normalized_VPN, u_prime))
            n_prime = unit_vector(cross_product(co.normalized_VPN, v_prime)) # this one may be wrong. Professor might have said something else

            newd = co.distance * 0.05

            left[0] = u_prime[0] * newd
            left[1] = u_prime[1] * newd
            left[2] = u_prime[2] * newd

            new_eye[0] = left[0] + co.eye[0]
            new_eye[1] = left[1] + co.eye[1]
            new_eye[2] = left[2] + co.eye[2]

            co.eye = new_eye


    elif key == GLUT_KEY_RIGHT:
        right = [0, 0, 0]
        new_eye = [0, 0, 0]
        print("You pressed right")
        print ("moving the eye in the negative direction of the view coordinate u axis by 0.05 of the distance " \
              "between the eye and the look at point")
        #Hitting the "right arrow" Key should move the eye in the negative direction
        # of the view coordinate u axis by 0.05 of the distance between the eye and look at point.
        for co in camera_list:# n is the normalized VPN
            u_prime = unit_vector(cross_product(co.normalized_VPN, co.vup)) # find the cross product of vp and vup and normalize it
            v_prime = unit_vector(cross_product(co.normalized_VPN, u_prime))
            n_prime = unit_vector(cross_product(co.normalized_VPN, v_prime)) # this one may be wrong. Professor might have said something else

            newd = co.distance * 0.05

            right[0] = u_prime[0] / newd
            right[1] = u_prime[1] / newd
            right[2] = u_prime[2] / newd

            new_eye[0] = right[0] + co.eye[0]
            new_eye[1] = right[1] + co.eye[1]
            new_eye[2] = right[2] + co.eye[2]

            co.eye = new_eye
    else:
        return

def timer(dummy):
      display()
      glutTimerFunc(30, timer, 0)
      #glutPostRedisplay()

def reshape(w, h):
      #print ("Width=",w,"Height=",h)
      pass

def main():
    glutInit(sys.argv)                                                      # initialize glut
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)                    # initialize display mode
    #glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)  # initialize display mode
    glutInitWindowSize(800, 550)                                            # initialize the window size
    glutInitWindowPosition(100, 100)                                        # initialize the window position
    glutCreateWindow(b"Lab 5:Krishna Bhattarai")                                              # create a window with name b"name"
    glClearColor(1, 0, 1, 0)                                                # glClearColor (red, green, blue, alpha): specifies clear values for color buffers
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)                               # glPolygonMode(face,mode): Select a polygon rasterization mode. face = must be GL_Front_AND_BACK, mode = GL_POINT, GL_LINE, GL_FIL FILLS BOTHS FRONT AND BACK FACING POLYGONS
    glEnable(GL_DEPTH_TEST)                                                 # glEnable (GL_DEPTH_TEST): enable depth comparisons and update the depth buffer
    glDepthFunc(GL_LESS)                                                    # glDepthFunc(): specify the value used for depth buffer comparisons, Gl_LESS: passes if the incoming z value is less than the stored z value
    glutDisplayFunc(display)                                                # sets the display callback for the current window
    glutKeyboardFunc(keyHandler)                                            # glutKeyboardFunc sets the keyboard callback for the current window.
    glutSpecialFunc(special)
    glutTimerFunc(300, timer, 0)                                            # glutTimerFunc registers a timer callback to be triggered in a specified number of milliseconds.
    #glutReshapeFunc(reshape)                                                # glutReshapeFunc sets the reshape callback for the current window.
    glMatrixMode(GL_PROJECTION)                                             # glMatrixMode - Specify which matrix is the current matrix: params GL_MODELVIEW, GL_PROJECTION, GL_TEXTURE, GL_COLOR
    glLoadIdentity()                                                        # Replace the current matrix with the identity matrix
    glMatrixMode(GL_MODELVIEW)                                              # glMatrixMode - Specify which matrix is the current matrix: params GL_MODELVIEW, GL_PROJECTION, GL_TEXTURE, GL_COLOR
    glLoadIdentity()                                                        # Replace the current matrix with the identity matrix
    #glutIdleFunc(display)                                                   # draw all the time
    glutMainLoop()                                                          # enters the GLUT event processing loop. should be called only once

if __name__ == "__main__":
    main()