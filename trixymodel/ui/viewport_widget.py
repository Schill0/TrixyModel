from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
import math

class ViewportWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.display_mode = "Shaded"
        self.objects = []
        self.zoom = -10.0
        self.rot_x = 30
        self.rot_y = -45
        self.pan_x = 0
        self.pan_y = 0
        self.last_mouse_pos = None
        self.pan_mode = False
        self.spawn_point = [0, 0, 0]
        self.selected_object = None
        self.object_list_widget = None
        self.object_counter = 1

    def set_object_list_widget(self, widget):
        self.object_list_widget = widget

    def add_primitive(self, primitive_type):
        name = f"{primitive_type}_{self.object_counter}"
        self.object_counter += 1
        obj = {
            'name': name,
            'type': primitive_type,
            'position': list(self.spawn_point),
            'selected': False
        }
        self.objects.append(obj)
        if self.object_list_widget:
            self.object_list_widget.addItem(name)
        self.update()

    def select_object_by_name(self, name):
        for obj in self.objects:
            obj['selected'] = (obj['name'] == name)
            if obj['selected']:
                self.selected_object = obj
        self.update()

    def set_display_mode(self, mode):
        self.display_mode = mode
        self.update()

    def initializeGL(self):
        glClearColor(0.15, 0.15, 0.15, 1.0)
        glEnable(GL_DEPTH_TEST)
        glPointSize(5)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h != 0 else 1
        gluPerspective(45.0, aspect, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslatef(self.pan_x, -self.pan_y, self.zoom)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)

        self.draw_grid()
        self.draw_axes()
        self.draw_cursor()

        for obj in self.objects:
            glPushMatrix()
            glTranslatef(*obj['position'])
            if obj['selected']:
                glColor3f(1.0, 0.5, 0.0)
            else:
                glColor3f(1.0, 1.0, 1.0)
            self.draw_primitive(obj['type'])
            glPopMatrix()

    def draw_axes(self):
        glBegin(GL_LINES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-1000.0, 0.0, 0.0)
        glVertex3f(1000.0, 0.0, 0.0)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, -1000.0, 0.0)
        glVertex3f(0.0, 1000.0, 0.0)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, -1000.0)
        glVertex3f(0.0, 0.0, 1000.0)
        glEnd()

    def draw_grid(self):
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_LINES)
        for i in range(-20, 21):
            glVertex3f(i, 0, -20)
            glVertex3f(i, 0, 20)
            glVertex3f(-20, 0, i)
            glVertex3f(20, 0, i)
        glEnd()

    def draw_cursor(self):
        glColor3f(1.0, 0.0, 1.0)
        glBegin(GL_LINES)
        for i in range(3):
            axis = [0, 0, 0]
            axis[i] = 0.2
            glVertex3f(*self.spawn_point)
            glVertex3f(*(self.spawn_point[j] + axis[j] for j in range(3)))
        glEnd()

    def draw_primitive(self, primitive_type):
        if self.display_mode == "Wireframe":
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif self.display_mode == "Vertices":
            glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        if primitive_type == "cube":
            self.draw_cube()
        elif primitive_type == "plane":
            self.draw_plane()
        elif primitive_type == "sphere":
            self.draw_sphere()

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw_cube(self):
        vertices = [
            [-1, -1, -1], [ 1, -1, -1],
            [ 1,  1, -1], [-1,  1, -1],
            [-1, -1,  1], [ 1, -1,  1],
            [ 1,  1,  1], [-1,  1,  1],
        ]
        faces = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [2, 3, 7, 6],
            [1, 2, 6, 5],
            [3, 0, 4, 7],
        ]
        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

    def draw_plane(self):
        glBegin(GL_QUADS)
        glVertex3f(-2, 0, -2)
        glVertex3f( 2, 0, -2)
        glVertex3f( 2, 0,  2)
        glVertex3f(-2, 0,  2)
        glEnd()

    def draw_sphere(self):
        stacks, slices, radius = 10, 10, 1.0
        for i in range(stacks):
            lat0 = math.pi * (-0.5 + float(i) / stacks)
            z0 = math.sin(lat0)
            zr0 =  math.cos(lat0)
            lat1 = math.pi * (-0.5 + float(i+1) / stacks)
            z1 = math.sin(lat1)
            zr1 = math.cos(lat1)

            glBegin(GL_QUAD_STRIP)
            for j in range(slices+1):
                lng = 2 * math.pi * float(j) / slices
                x = math.cos(lng)
                y = math.sin(lng)
                glVertex3f(x * zr0 * radius, y * zr0 * radius, z0 * radius)
                glVertex3f(x * zr1 * radius, y * zr1 * radius, z1 * radius)
            glEnd()

    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y() * 0.001
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        self.last_mouse_pos = event.position()
        self.pan_mode = event.modifiers() == Qt.KeyboardModifier.ShiftModifier and event.buttons() & Qt.MouseButton.LeftButton

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.last_mouse_pos is None:
            return
        dx = event.position().x() - self.last_mouse_pos.x()
        dy = event.position().y() - self.last_mouse_pos.y()
        if event.buttons() & Qt.MouseButton.MiddleButton:
            self.rot_x += dy
            self.rot_y += dx
        elif self.pan_mode:
            self.pan_x += dx * 0.01
            self.pan_y += dy * 0.01
        self.last_mouse_pos = event.position()
        self.update()
