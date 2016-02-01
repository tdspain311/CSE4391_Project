//"use strict";
//class Camera
//{
//    constructor(camera_name, projection_type, eye, look_at, vup, vrc, viewport, distance)
//    {
//        this.camera_name = camera_name;
//        this.projection_type = projection_type;
//        this.eye = eye;
//        this.look_at = look_at;
//        this.vup = vup;
//        this.vrc = [-1, 1, -1, 1, -1, 1];       //view volume VRC [<umin><umax><vmin><vnax><nmin><nmax>]
//        this.viewport = [0.1, 0.1, 0.9, 0.9];   //Define viewport (normalized coordinates)
//
//
//        // parallel projection
//        // glrotho(umin, umax, vmin, vmax, nmin, nmax)
////        glOrtho(co.vrc[0], co.vrc[1], co.vrc[2], co.vrc[3], co.vrc[4], co.vrc[5])
//
//        // perspective projection
//          //glFrustum (umin, umax, vmin, vmax, nmin, nmax)
////        glFrustum(co.vrc[0], co.vrc[1], co.vrc[2], co.vrc[3], co.vrc[4], co.vrc[5])
//
//           // Calculate the look at
//        //  gluLookAt(eye0, eye1, eye2, look_at0, look_at1, look_at2, vup0, vup1, vup2)
////        gluLookAt(co.eye[0], co.eye[1], co.eye[2], co.look_at[0], co.look_at[1], co.look_at[2], co.vup[0], co.vup[1], co.vup[2] )
////
//        // calculate the viewport
//        //glViewport(int(w * co.viewport[0]), int(h * co.viewport[1]), int(w *(co.viewport[2] - co.viewport[0])), int(h *(co.viewport[3] - co.viewport[1])))
//
//    }
//
//}