from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame, pygame.image
from pygame.locals import *
import numpy


width, height = 1000, 747


def set_projection_from_camera(K):
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()

  fx = K[0, 0]
  fy = K[1, 1]
  fovy = 2 * numpy.arctan(0.5 * height / fy) * 180 / numpy.pi
  aspect = (width * fy) / (height * fx)

  near, far = 0.1, 100
  gluPerspective(fovy, aspect, near, far)
  glViewport(0, 0, width, height)


def set_modelview_from_camera(Rt):
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()

  # Rotate 90 deg around x, so that z is up.
  Rx = numpy.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

  # Remove noise from rotation, make sure it's a pure rotation.
  R = Rt[:, :3]
  U, S, V = numpy.linalg.svd(R)
  R = numpy.dot(U, V)
  R[0, :] = -R[0, :]  # Change sign of x axis.

  t = Rt[:, 3]

  M = numpy.eye(4)
  M[:3, :3] = numpy.dot(R, Rx)
  M[:3, 3] = t

  m = M.T.flatten()
  glLoadMatrixf(m)


def setup():
  pygame.init()
  pygame.display.set_mode((width, height), OPENGL | DOUBLEBUF)
  pygame.display.set_caption('Look, an OpenGL window!')


setup()
K = numpy.array([[1, 0], [0, 1]])  # FIXME
set_projection_from_camera(K)
Rt = numpy.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])  # FIXME
set_modelview_from_camera(Rt)

while True:
  event = pygame.event.poll()
  if event.type in (QUIT, KEYDOWN):
    break
  pygame.display.flip()
