from PyQt4.QtCore import Qt
from PyQt4.QtCore import QByteArray
from PyQt4.QtCore import QBuffer
from PyQt4.QtCore import QIODevice, QFile
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QImage
from PyQt4.QtGui import QPainter
from PyQt4.QtSvg import QSvgRenderer
from PyQt4.QtGui import QApplication

import sys, os

app = QApplication(sys.argv)

svg = QSvgRenderer()
current = os.getcwd()
os.chdir(os.path.dirname(sys.argv[1]))
svg.load(os.path.basename(sys.argv[1]))
size = svg.defaultSize()
size.scale(600, 800, Qt.KeepAspectRatio)
image = QImage(size, QImage.Format_ARGB32_Premultiplied)
image.fill(QColor("white").rgb())
painter = QPainter(image)
svg.render(painter)
painter.end()
os.chdir(current)
f = QFile(sys.argv[2])
f.open(QIODevice.WriteOnly)
image.save(f, 'PNG')
