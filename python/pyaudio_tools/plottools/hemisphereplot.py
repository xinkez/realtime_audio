import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pa_tools.constants as consts
from realtimeplot import RealtimePlot

class HemispherePlot(RealtimePlot):
  """
  Class for plotting in a 3d hemisphere
  """
  def __init__(self):
    RealtimePlot.__init__(self)
    self._setup_figure()

  def _setup_figure(self):
    RealtimePlot._setup_figure(self, projection='3d')
    self._plot_limit = 1.2
    self._ax.set_xlim(-self._plot_limit, self._plot_limit)
    self._ax.set_ylim(-self._plot_limit, self._plot_limit)
    self._ax.set_zlim(0, self._plot_limit)
    self._setup_wireframe()

  def _setup_wireframe(self):
    self._n_azimuth = 30
    self._azimuth = np.linspace(0, 2*np.pi, self._n_azimuth)
    self._n_zenith = 30
    self._zenith = np.linspace(0, np.pi / 2, self._n_zenith)
    # Array of all combinations. 1st row = azimuth, 2nd = zenith
    azi, zen = np.meshgrid(self._azimuth, self._zenith)
    x = np.sin(zen)*np.cos(azi)
    y = np.sin(zen)*np.sin(azi)
    z = np.cos(zen)
    self._wireframe = self._ax.plot_wireframe(x, y, z, color='gray', lw=.2)
