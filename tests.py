# coding=utf-8
"""Tests that run once"""
import io
import os
import sys
import imp
import shutil
import tempfile
import subprocess
import contextlib
import datetime
import json

# Third-party dependency
import six


try:
    # Try importing assert_raises from nose.tools
    from nose.tools import assert_raises
except ImportError:
    # Fallback: Define assert_raises using unittest if the import fails
    import unittest

    def assert_raises(expected_exception, callable_obj=None, *args, **kwargs):
        """
        Custom implementation of assert_raises using unittest.

        Parameters:
        - expected_exception: The exception type that is expected to be raised.
        - callable_obj: The callable object that is expected to raise the exception.
        - *args, **kwargs: Arguments and keyword arguments to pass to the callable object.

        Usage example:
        with assert_raises(SomeException):
            function_that_raises_some_exception()
        """
        context = unittest.TestCase().assertRaises(expected_exception)

        # If callable_obj is provided, directly call the function with the context manager
        if callable_obj:
            with context:
                callable_obj(*args, **kwargs)
        else:
            # Otherwise, return the context manager to be used with a 'with' statement
            return context

PYTHON = sys.version_info[0]  # e.g. 2 or 3
IS_TOX = os.getenv("TOX_ENV_NAME") is not None

try:
    long
except NameError:
    # Python 3 compatibility
    long = int


def _pyside2_commit_date():
    """Return the commit date of PySide2"""

    import PySide2
    if hasattr(PySide2, '__build_commit_date__'):
        commit_date = PySide2.__build_commit_date__
        datetime_object = datetime.datetime.strptime(
            commit_date[: commit_date.rfind('+')], '%Y-%m-%dT%H:%M:%S'
        )
        return datetime_object
    else:
        # Returns None if no __build_commit_date__ is available
        return None


@contextlib.contextmanager
def captured_output():
    new_out, new_err = six.StringIO(), six.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def CustomWidget(parent=None):
    """
    Wrap CustomWidget class into a function to avoid global Qt import
    """
    from Qt import QtWidgets

    class Widget(QtWidgets.QWidget):
        pass

    return Widget(parent)


self = sys.modules[__name__]


qwidget_ui = u"""\
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>507</width>
    <height>394</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <layout class="QGridLayout" name="gridLayout">
   <item row="0" column="0">
    <widget class="QLineEdit" name="lineEdit"/>
   </item>
   <item row="1" column="0">
    <widget class="QLabel" name="label">
     <property name="text">
      <string>TextLabel</string>
     </property>
    </widget>
   </item>
   <item row="2" column="0">
    <widget class="QLineEdit" name="lineEdit_2"/>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections>
  <connection>
   <sender>lineEdit</sender>
   <signal>textChanged(QString)</signal>
   <receiver>label</receiver>
   <slot>setText(QString)</slot>
   <hints>
    <hint type="sourcelabel">
     <x>228</x>
     <y>23</y>
    </hint>
    <hint type="destinationlabel">
     <x>37</x>
     <y>197</y>
    </hint>
   </hints>
  </connection>
 </connections>
</ui>
"""


qmainwindow_ui = u"""\
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>238</width>
    <height>44</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QLineEdit" name="lineEdit"/>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


qdialog_ui = u"""\
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>186</width>
    <height>38</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Dialog</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <widget class="QLineEdit" name="lineEdit"/>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


qdockwidget_ui = u"""\
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>DockWidget</class>
 <widget class="QDockWidget" name="DockWidget">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>169</width>
    <height>60</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>DockWidget</string>
  </property>
  <widget class="QWidget" name="dockWidgetContents">
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QLineEdit" name="lineEdit"/>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


qcustomwidget_ui = u"""\
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>238</width>
    <height>44</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="CustomWidget" name="customwidget">
  </widget>
 </widget>
 <customwidgets>
  <customwidget>
   <class>CustomWidget</class>
   <extends>QWidget</extends>
   <header>tests.h</header>
  </customwidget>
 </customwidgets>
 <resources/>
 <connections/>
</ui>
"""


qpycustomwidget_ui = u"""\
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>238</width>
    <height>44</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="CustomWidget" name="customwidget">
  </widget>
 </widget>
 <customwidgets>
  <customwidget>
   <class>CustomWidget</class>
   <extends>QWidget</extends>
   <header>custom.customwidget.customwidget</header>
  </customwidget>
 </customwidgets>
 <resources/>
 <connections/>
</ui>
"""


python_custom_widget = u'''
def CustomWidget(parent=None):
    """
    Wrap CustomWidget class into a function to avoid global Qt import
    """
    from Qt import QtWidgets

    class Widget(QtWidgets.QWidget):
        pass

    return Widget(parent)
'''


def setup():
    """Module-wide initialisation

    This function runs once, followed by teardown() below once
    all tests have completed.

    """
    self.tempdir = tempfile.mkdtemp()

    def saveUiFile(filename, ui_template):
        filename = os.path.join(self.tempdir, filename)
        with io.open(filename, "w", encoding="utf-8") as f:
            f.write(ui_template)
        return filename

    self.ui_qwidget = saveUiFile("qwidget.ui", qwidget_ui)
    self.ui_qmainwindow = saveUiFile("qmainwindow.ui", qmainwindow_ui)
    self.ui_qdialog = saveUiFile("qdialog.ui", qdialog_ui)
    self.ui_qdockwidget = saveUiFile("qdockwidget.ui", qdockwidget_ui)
    self.ui_qpycustomwidget = saveUiFile("qcustomwidget.ui", qcustomwidget_ui)


def setUpModule():
    """Module-wide initialisation

    This function runs once, followed by tearDownModule() below once
    all tests have completed.

    """
    setup()


def teardown():
    shutil.rmtree(self.tempdir)


def tearDownModule():
    teardown()


def binding(binding):
    """Isolate test to a particular binding

    When used, tests inside the if-statement are run independently
    with the given binding.

    Without this function, a test is run once for each binding.

    """

    return os.getenv("QT_PREFERRED_BINDING") == binding


def get_enum(cls, namespace, enum):
    """Get an enum from a fully qualified namespace

    Qt4 and older Qt5 don't support fully qualified enum names, this accounts
    for it.

    For example to access `Qt.QtCore.Qt.WindowState.WindowActive` using
    `get_enum(Qt.QtCore.Qt, "WindowState", "WindowActive")` returns
    `Qt.QtCore.Qt.WindowState.WindowActive` for newer Qt versions. For Qt
    versions that don't support fully qualified enum names it returns
    `Qt.QtCore.Qt.WindowActive`.

    Args:
        cls: The class that contains the enum.
        namespace(str): The namespace name in Qt6.
        enum(str): The name of the enum value.
    """
    if not hasattr(cls, namespace):
        # Legacy short enum name
        return getattr(cls, enum)
    namespace_cls = getattr(cls, namespace)
    if hasattr(namespace_cls, enum):
        # Return new fully qualified enum if possible
        return getattr(namespace_cls, enum)
    # Fallback to legacy short enum name if not using new enum classes
    return getattr(cls, enum)


@contextlib.contextmanager
def ignoreQtMessageHandler(msgs):
    """A context that ignores specific qMessages for all bindings

    Args:
        msgs: list of message strings to ignore
    """
    from Qt import QtCompat

    def messageOutputHandler(msgType, logContext, msg):
        if msg in msgs:
            return
        sys.stderr.write("{0}\n".format(msg))

    QtCompat.qInstallMessageHandler(messageOutputHandler)
    try:
        yield
    finally:
        QtCompat.qInstallMessageHandler(None)


def test_environment():
    """Tests require all bindings to be installed (except PySide on py3.5+)"""

    if sys.version_info < (3, 5):
        # PySide is not available for Python > 3.4
        imp.find_module("PySide")
    if sys.version_info >= (3, 9):
        # NOTE: Existing docker images don't support Qt6
        imp.find_module("PySide6")
        imp.find_module("PyQt6")
    elif IS_TOX:
        # Tox environments don't have access to Qt4
        imp.find_module("PySide2")
        imp.find_module("PyQt5")
    else:
        imp.find_module("PySide2")
        imp.find_module("PyQt4")
        imp.find_module("PyQt5")


def test_load_ui_returntype():
    """load_ui returns an instance of QObject"""

    import sys
    from Qt import QtWidgets, QtCore, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    obj = QtCompat.loadUi(self.ui_qwidget)
    assert isinstance(obj, QtCore.QObject)
    app.exit()


def test_load_ui_baseinstance():
    """Tests to see if the baseinstance loading loads a QWidget on properly"""
    import sys
    from Qt import QtWidgets, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    win = QtWidgets.QWidget()
    QtCompat.loadUi(self.ui_qwidget, win)
    assert hasattr(win, 'lineEdit'), "loadUi could not load instance to win"
    app.exit()


def test_load_ui_signals():
    """Tests to see if the baseinstance connects signals properly"""
    import sys
    from Qt import QtWidgets, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    win = QtWidgets.QWidget()
    QtCompat.loadUi(self.ui_qwidget, win)

    win.lineEdit.setText('Hello')
    assert str(win.label.text()) == 'Hello', "lineEdit signal did not fire"

    app.exit()


def test_load_ui_mainwindow():
    """Tests to see if the baseinstance loading loads a QMainWindow properly"""
    import sys
    from Qt import QtWidgets, QtCompat


    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    win = QtWidgets.QMainWindow()

    QtCompat.loadUi(self.ui_qmainwindow, win)

    assert hasattr(win, 'lineEdit'), \
        "loadUi could not load instance to main window"

    app.exit()


def test_load_ui_dialog():
    """Tests to see if the baseinstance loading loads a QDialog properly"""
    import sys
    from Qt import QtWidgets, QtCompat


    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    win = QtWidgets.QDialog()

    QtCompat.loadUi(self.ui_qdialog, win)

    assert hasattr(win, 'lineEdit'), \
        "loadUi could not load instance to main window"

    app.exit()


def test_load_ui_dockwidget():
    """Tests to see if the baseinstance loading loads a QDockWidget properly"""
    import sys
    from Qt import QtWidgets, QtCompat


    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    win = QtWidgets.QDockWidget()

    QtCompat.loadUi(self.ui_qdockwidget, win)

    assert hasattr(win, 'lineEdit'), \
        "loadUi could not load instance to main window"

    app.exit()


def test_load_ui_customwidget():
    """Tests to see if loadUi loads a custom widget properly"""
    import sys
    from Qt import QtWidgets, QtCompat


    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    win = QtWidgets.QMainWindow()

    QtCompat.loadUi(self.ui_qpycustomwidget, win)

    # Ensure that the derived class was properly created
    # and not the base class (in case of failure)
    custom_class_name = getattr(win, "customwidget", None).__class__.__name__
    excepted_class_name = CustomWidget(win).__class__.__name__
    assert custom_class_name == excepted_class_name, \
        "loadUi could not load custom widget to main window"

    app.exit()


def test_load_ui_pycustomwidget():
    """Tests to see if loadUi loads a custom widget properly"""
    import sys
    from Qt import QtWidgets, QtCompat

    # create a python file for the custom widget in a directory relative to the tempdir
    filename = os.path.join(
        self.tempdir,
        "custom",
        "customwidget",
        "customwidget.py"
    )
    os.makedirs(os.path.dirname(filename))
    with io.open(filename, "w", encoding="utf-8") as f:
        f.write(self.python_custom_widget)

    # Python 2.7 requires that each folder be a package
    with io.open(os.path.join(self.tempdir, "custom/__init__.py"), "w", encoding="utf-8") as f:
        f.write(u"")
    with io.open(os.path.join(self.tempdir, "custom/customwidget/__init__.py"), "w", encoding="utf-8") as f:
        f.write(u"")
    # append the path to ensure the future import can be loaded 'relative' to the tempdir
    sys.path.append(self.tempdir)


    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    win = QtWidgets.QMainWindow()

    QtCompat.loadUi(self.ui_qpycustomwidget, win)

    # Ensure that the derived class was properly created
    # and not the base class (in case of failure)
    custom_class_name = getattr(win, "customwidget", None).__class__.__name__
    excepted_class_name = CustomWidget(win).__class__.__name__
    assert custom_class_name == excepted_class_name, \
        "loadUi could not load custom widget to main window"

    app.exit()


def test_load_ui_invalidpath():
    """Tests to see if loadUi successfully fails on invalid paths"""
    import sys
    from Qt import QtWidgets, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    assert_raises(IOError, QtCompat.loadUi, 'made/up/path')
    app.exit()


def test_load_ui_invalidxml():
    """Tests to see if loadUi successfully fails on invalid ui files"""
    import sys
    invalid_xml = os.path.join(self.tempdir, "invalid.ui")
    with io.open(invalid_xml, "w", encoding="utf-8") as f:
        f.write(u"""
        <?xml version="1.0" encoding="UTF-8"?>
        <ui version="4.0" garbage
        </ui>
        """)

    from xml.etree import ElementTree
    from Qt import QtWidgets, QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    assert_raises(ElementTree.ParseError, QtCompat.loadUi, invalid_xml)
    app.exit()


def test_load_ui_existingLayoutOnDialog():
    """Tests to see if loading a ui onto a layout in a Dialog works"""
    import sys
    from Qt import QtWidgets, QtCompat

    msgs = 'QLayout: Attempting to add QLayout "" to QDialog ' \
        '"Dialog", which already has a layout'

    with ignoreQtMessageHandler([msgs]):

        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        win = QtWidgets.QDialog()
        QtWidgets.QComboBox(win)
        QtWidgets.QHBoxLayout(win)
        QtCompat.loadUi(self.ui_qdialog, win)
    app.exit()


def test_load_ui_existingLayoutOnMainWindow():
    """Tests to see if loading a ui onto a layout in a MainWindow works"""
    import sys
    from Qt import QtWidgets, QtCompat

    msgs = 'QLayout: Attempting to add QLayout "" to QMainWindow ' \
        '"", which already has a layout'

    with ignoreQtMessageHandler([msgs]):

        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        win = QtWidgets.QMainWindow()
        QtWidgets.QComboBox(win)
        QtWidgets.QHBoxLayout(win)
        QtCompat.loadUi(self.ui_qmainwindow, win)
    app.exit()


def test_load_ui_existingLayoutOnDockWidget():
    """Tests to see if loading a ui onto a layout in a DockWidget works"""
    import sys
    from Qt import QtWidgets, QtCompat

    msgs = 'QLayout: Attempting to add QLayout "" to QDockWidget ' \
        '"", which already has a layout'

    with ignoreQtMessageHandler([msgs]):

        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        win = QtWidgets.QDockWidget()
        QtWidgets.QComboBox(win)
        QtWidgets.QHBoxLayout(win)
        QtCompat.loadUi(self.ui_qdockwidget, win)
    app.exit()


def test_load_ui_existingLayoutOnWidget():
    """Tests to see if loading a ui onto a layout in a Widget works"""
    import sys
    from Qt import QtWidgets, QtCompat

    msgs = 'QLayout: Attempting to add QLayout "" to QWidget ' \
        '"Form", which already has a layout'

    with ignoreQtMessageHandler([msgs]):

        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        win = QtWidgets.QWidget()
        QtWidgets.QComboBox(win)
        QtWidgets.QHBoxLayout(win)
        QtCompat.loadUi(self.ui_qwidget, win)
    app.exit()


def test_preferred_none():
    """Preferring None shouldn't import anything"""

    current = os.environ["QT_PREFERRED_BINDING"]
    try:
        os.environ["QT_PREFERRED_BINDING"] = "None"
        import Qt
        assert Qt.__name__ == "Qt", Qt
    finally:
        os.environ["QT_PREFERRED_BINDING"] = current


def test_vendoring():
    """Qt.py may be bundled along with another library/project

    Create toy project

    from project.vendor import Qt  # Absolute
    from .vendor import Qt         # Relative

    project/
        vendor/
            __init__.py
        __init__.py

    """

    project = os.path.join(self.tempdir, "myproject")
    vendor = os.path.join(project, "vendor")

    os.makedirs(vendor)

    # Make packages out of folders
    with open(os.path.join(project, "__init__.py"), "w") as f:
        f.write("from .vendor.Qt import QtWidgets")

    with open(os.path.join(vendor, "__init__.py"), "w") as f:
        f.write("\n")

    # Copy real Qt.py into myproject
    shutil.copy(os.path.join(os.path.dirname(__file__), "Qt.py"),
                os.path.join(vendor, "Qt.py"))

    # Copy real Qt.py into the root folder
    shutil.copy(os.path.join(os.path.dirname(__file__), "Qt.py"),
                os.path.join(self.tempdir, "Qt.py"))

    print("Testing relative import..")
    assert subprocess.call(
        [sys.executable, "-c", "import myproject"],
        cwd=self.tempdir,
        stdout=subprocess.PIPE,  # With nose process isolation, buffer can
        stderr=subprocess.STDOUT,  # easily get full and throw an error.
    ) == 0

    print("Testing absolute import..")
    assert subprocess.call(
        [sys.executable, "-c", "from myproject.vendor.Qt import QtWidgets"],
        cwd=self.tempdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) == 0

    print("Testing direct import..")
    assert subprocess.call(
        [sys.executable, "-c", "import myproject.vendor.Qt"],
        cwd=self.tempdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) == 0

    #
    # Test invalid json data
    print("Testing invalid json data..")
    env = os.environ.copy()
    env["QT_PREFERRED_BINDING_JSON"] = '{"Qt":["PyQt5","PyQt4"],}'

    cmd = "import myproject.vendor.Qt;"
    cmd += "import Qt;"
    cmd += "assert myproject.vendor.Qt.__binding__ != None, 'vendor';"
    cmd += "assert Qt.__binding__ != None, 'Qt';"

    popen = subprocess.Popen(
        [sys.executable, "-c", cmd],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=self.tempdir,
        env=env
    )

    out, err = popen.communicate()

    if popen.returncode != 0:
        print(out)
        msg = "An exception was raised"
        assert popen.returncode == 0, msg

    error_check = b"Qt.py [warning]:"
    assert err.startswith(error_check), err

    print('out------------------')
    print(out)

    print('err ------------------')
    print(err)

    # Check QT_PREFERRED_BINDING_JSON works as expected
    print("Testing QT_PREFERRED_BINDING_JSON is respected..")
    cmd = "import myproject.vendor.Qt;"
    # Check that the "None" binding was set for `import myproject.vendor.Qt`
    cmd += "assert myproject.vendor.Qt.__binding__ == 'None', 'vendor';"
    cmd += "import Qt;"
    # Check that the "None" binding was not set for `import Qt`.
    # This should be PyQt5 or PyQt4 depending on the test environment.
    cmd += "assert Qt.__binding__ != 'None', 'Qt'"

    # If the module name is "Qt" use PyQt5 or PyQt4, otherwise use None binding
    env = os.environ.copy()
    env["QT_PREFERRED_BINDING_JSON"] = json.dumps(
        {
            "Qt": ["PySide6", "PyQt5", "PyQt4"],
            "default": ["None"]
        }
    )

    assert subprocess.call(
        [sys.executable, "-c", cmd],
        stdout=subprocess.PIPE,
        cwd=self.tempdir,
        env=env
    ) == 0

    print("Testing QT_PREFERRED_BINDING_JSON and QT_PREFERRED_BINDING work..")
    env["QT_PREFERRED_BINDING_JSON"] = '{"Qt":["PySide6","PyQt5","PyQt4"]}'
    env["QT_PREFERRED_BINDING"] = "None"
    assert subprocess.call(
        [sys.executable, "-c", cmd],
        stdout=subprocess.PIPE,
        cwd=self.tempdir,
        env=env
    ) == 0


def test_convert_simple():
    """python -m Qt --convert works in general"""
    before = """\
from PySide2 import QtCore, QtGui, QtWidgets

class Ui_uic(object):
    def setupUi(self, uic):
        self.retranslateUi(uic)

    def retranslateUi(self, uic):
        self.pushButton_2.setText(
            QtWidgets.QApplication.translate("uic", "NOT Ok", None, -1))
"""

    after = """\
from Qt import QtCore, QtGui, QtWidgets
from Qt import QtCompat

class Ui_uic(object):
    def setupUi(self, uic):
        self.retranslateUi(uic)

    def retranslateUi(self, uic):
        self.pushButton_2.setText(
            QtCompat.translate("uic", "NOT Ok", None, -1))
"""

    fname = os.path.join(self.tempdir, "simple.py")
    with open(fname, "w") as f:
        f.write(before)

    from Qt import QtCompat

    current_dir = os.getcwd()
    os.chdir(self.tempdir)
    QtCompat._cli(args=["--convert", "simple.py"])

    with open(fname) as f:
        assert f.read() == after

    # Prevent windows file lock PermissionError issues when testing on windows.
    os.chdir(current_dir)

def test_convert_5_15_2_format():
    before = """\
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Ui_uic(object):
    def setupUi(self, uic):
        self.retranslateUi(uic)

    def retranslateUi(self, uic):
        self.pushButton_2.setText(
            QCoreApplication.translate("uic", "NOT Ok", None, -1))
    """

    after = """\
from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *
from Qt import QtCompat

class Ui_uic(object):
    def setupUi(self, uic):
        self.retranslateUi(uic)

    def retranslateUi(self, uic):
        self.pushButton_2.setText(
            QtCompat.translate("uic", "NOT Ok", None, -1))
    """

    fname = os.path.join(self.tempdir, "5_15_2_uic.py")
    with open(fname, "w") as f:
        f.write(before)

    from Qt import QtCompat

    current_dir = os.getcwd()
    os.chdir(self.tempdir)
    QtCompat._cli(args=["--convert", "5_15_2_uic.py"])

    with open(fname) as f:
        assert f.read() == after

    # Prevent windows file lock PermissionError issues when testing on windows.
    os.chdir(current_dir)

def test_convert_idempotency():
    """Converting a converted file produces an identical file"""
    before = """\
from PySide2 import QtCore, QtGui, QtWidgets

class Ui_uic(object):
    def setupUi(self, uic):
        self.retranslateUi(uic)

    def retranslateUi(self, uic):
        self.pushButton_2.setText(
            QtWidgets.QApplication.translate("uic", "NOT Ok", None, -1))
"""

    after = """\
from Qt import QtCore, QtGui, QtWidgets
from Qt import QtCompat

class Ui_uic(object):
    def setupUi(self, uic):
        self.retranslateUi(uic)

    def retranslateUi(self, uic):
        self.pushButton_2.setText(
            QtCompat.translate("uic", "NOT Ok", None, -1))
"""

    fname = os.path.join(self.tempdir, "idempotency.py")
    with open(fname, "w") as f:
        f.write(before)

    from Qt import QtCompat

    current_dir = os.getcwd()
    os.chdir(self.tempdir)
    QtCompat._cli(args=["--convert", "idempotency.py"])

    with open(fname) as f:
        assert f.read() == after

    QtCompat._cli(args=["--convert", "idempotency.py"])

    with open(fname) as f:
        assert f.read() == after

    # Prevent windows file lock PermissionError issues when testing on windows.
    os.chdir(current_dir)


def test_convert_backup():
    """Converting produces a backup"""

    fname = os.path.join(self.tempdir, "idempotency.py")
    with open(fname, "w") as f:
        f.write("")

    from Qt import QtCompat

    current_dir = os.getcwd()
    os.chdir(self.tempdir)
    QtCompat._cli(args=["--convert", "idempotency.py"])

    assert os.path.exists(
        os.path.join(self.tempdir, "%s_backup%s" % os.path.splitext(fname))
    )

    # Prevent windows file lock PermissionError issues when testing on windows.
    os.chdir(current_dir)


def test_import_from_qtwidgets():
    """Fix #133, `from Qt.QtWidgets import XXX` works"""
    from Qt.QtWidgets import QPushButton
    assert QPushButton.__name__ == "QPushButton", QPushButton


def test_import_from_qtcompat():
    """ `from Qt.QtCompat import XXX` works """
    from Qt.QtCompat import loadUi
    assert loadUi.__name__ == "_loadUi", loadUi


def test_i158_qtcore_direct_import():
    """import Qt.QtCore works on all bindings

    This addresses issue #158

    """

    import Qt.QtCore
    assert hasattr(Qt.QtCore, "Signal")


def test_translate_arguments():
    """Arguments of QtCompat.translate are correct

    QtCompat.translate is a shim over the PySide, PyQt4 and PyQt5
    equivalent with an interface like the one found in PySide2.

    Reference: https://doc.qt.io/qt-5/qcoreapplication.html#translate

    """

    import Qt

    # This will run on each binding
    result = Qt.QtCompat.translate("CustomDialog",  # context
                                   "Status",  # sourceText
                                   None,  # disambiguation
                                   -1)  # n
    assert result == u'Status', result


def test_binding_and_qt_version():
    """Qt's __binding_version__ and __qt_version__ populated"""

    import Qt

    assert Qt.__binding_version__ != "0.0.0", ("Binding version was not "
                                               "populated")
    assert Qt.__qt_version__ != "0.0.0", ("Qt version was not populated")


def test_binding_states():
    """Tests to see if the Qt binding enum states are set properly"""
    import Qt
    assert Qt.IsPySide == binding("PySide")
    assert Qt.IsPySide2 == binding("PySide2")
    assert Qt.IsPySide6 == binding("PySide6")
    if sys.version_info >= (3, 9):
        # NOTE: Existing docker images don't support Qt6
        assert Qt.IsPyQt6 == binding("PyQt6")
    assert Qt.IsPyQt5 == binding("PyQt5")
    assert Qt.IsPyQt4 == binding("PyQt4")


def test_qtcompat_base_class():
    """Tests to ensure the QtCompat namespace object works as expected"""
    import sys
    import Qt
    from Qt import QtWidgets
    from Qt import QtCompat

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    # suppress `local variable 'app' is assigned to but never used`
    app
    header = QtWidgets.QHeaderView(
        get_enum(Qt.QtCore.Qt, "Orientation", "Horizontal")
    )

    # Spot check compatibility functions
    QtCompat.QHeaderView.setSectionsMovable(header, False)
    assert QtCompat.QHeaderView.sectionsMovable(header) is False
    QtCompat.QHeaderView.setSectionsMovable(header, True)
    assert QtCompat.QHeaderView.sectionsMovable(header) is True

    # Verify that the grab function actually generates a non-null image
    button = QtWidgets.QPushButton('TestImage')
    pixmap = QtCompat.QWidget.grab(button)
    assert not pixmap.isNull()


def test_cli():
    """Qt.py is available from the command-line"""
    env = os.environ.copy()
    env.pop("QT_VERBOSE")  # Do not include debug messages

    popen = subprocess.Popen(
        [sys.executable, "Qt.py", "--help"],
        stdout=subprocess.PIPE,
        env=env
    )

    out, err = popen.communicate()
    assert out.startswith(b"usage: Qt.py"), "\n%s" % out


def test_membership():
    """Common members of Qt.py exist in all bindings, excl exceptions"""
    import Qt

    common_members = Qt._common_members.copy()

    if os.environ.get('VFXPLATFORM') == '2017':
        # For CY2017, skip the following
        common_members['QtGui'].remove('QDesktopServices')
        common_members.pop('QtOpenGL', None)
        common_members.pop('QtMultimedia', None)

    missing = list()
    for module, members in common_members.items():
        missing.extend(
            member for member in members
            if not hasattr(getattr(Qt, module), member)
        )

    binding = Qt.__binding__
    assert not missing, (
        "Some members did not exist in {binding}\n{missing}".format(
            **locals())
    )


def test_missing():
    """Missing members of Qt.py have been defined with placeholders"""
    import Qt

    missing_members = Qt._missing_members.copy()

    missing = list()
    for module, members in missing_members.items():

        mod = getattr(Qt, module)
        missing.extend(
            member for member in members
            if not hasattr(mod, member) or
            not isinstance(getattr(mod, member), Qt.MissingMember)
        )

    binding = Qt.__binding__
    assert not missing, (
        "Some members did not exist in {binding} as "
        "a Qt.MissingMember type\n{missing}".format(**locals())
    )


def test_unicode_error_messages():
    """Test if unicode error messages with non-ascii characters
    throw the error reporter off"""
    import Qt
    unicode_message = u"DLL load failed : le module spécifié est introuvable."
    str_message = "DLL load failed : le module"

    with captured_output() as out:
        stdout, stderr = out
        Qt._warn(text=unicode_message)
        assert str_message in stderr.getvalue()


def test_enum_value():
    """Test QtCompat.enumValue returns an int value."""
    from Qt import QtCompat, QtGui
    from Qt.QtCore import Qt

    # Get the enum objects to test with
    enum_window_active = get_enum(Qt, "WindowState", "WindowActive")
    enum_demi_bold = get_enum(QtGui.QFont, "Weight", "DemiBold")

    if binding("PySide6") or binding("PyQt6"):
        window_active_check = enum_window_active.value
        # Note: Both int and .value work for this enum
        demi_bold_check = enum_demi_bold.value
    else:
        window_active_check = int(enum_window_active)
        demi_bold_check = int(enum_demi_bold)

    assert QtCompat.enumValue(enum_window_active) == window_active_check
    assert QtCompat.enumValue(enum_demi_bold) == demi_bold_check
    assert isinstance(QtCompat.enumValue(enum_window_active), int)
    assert isinstance(QtCompat.enumValue(enum_demi_bold), int)


def test_qfont_from_string():
    import Qt
    enum_weight_normal = get_enum(Qt.QtGui.QFont, "Weight", "Normal")
    enum_weight_bold = get_enum(Qt.QtGui.QFont, "Weight", "Bold")

    in_font = "Arial,7,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
    # PyQt5 for Python 3.7 requires creating a QApplication to init a QFont
    if binding("PyQt5"):
        if not Qt.QtWidgets.QApplication.instance():
            app = Qt.QtWidgets.QApplication(sys.argv)
        else:
            app = Qt.QtWidgets.QApplication.instance()
    try:
        font = Qt.QtGui.QFont()
        Qt.QtCompat.QFont.fromString(font, in_font)
        assert font.family() == "Arial"
        assert font.pointSizeF() == 7.0
        assert font.weight() == enum_weight_normal
        font.setWeight(enum_weight_bold)
        if binding("PySide6") or binding("PyQt6"):
            # In Qt6 the full string is returned with OpenType weight of 700
            out_font = "Arial,7,-1,5,700,0,0,0,0,0,0,0,0,0,0,1"
            assert font.toString() == out_font
        else:
            # In previous bindings the shorter version is returned. Also the bold
            # weight is 75 instead of 700
            assert font.toString() == "Arial,7,-1,5,75,0,0,0,0,0"
    finally:
        if binding("PyQt5"):
            app.exit()


if sys.version_info < (3, 5):
    # PySide is not available for Python > 3.4
    # Shiboken(1) doesn't support Python 3.5
    # https://github.com/PySide/shiboken-setup/issues/3

    def test_wrapInstance():
        """Tests .wrapInstance cast of pointer to explicit class

        Note:
            sip.wrapInstance will ignore the explicit class if there is a more
            suitable type available.

        """
        from Qt import QtCompat, QtWidgets

        app = QtWidgets.QApplication(sys.argv)

        try:
            button = QtWidgets.QPushButton("Hello world")
            button.setObjectName("MySpecialButton")
            pointer = QtCompat.getCppPointer(button)
            widget = QtCompat.wrapInstance(long(pointer),
                                           QtWidgets.QWidget)

            assert widget.objectName() == button.objectName()

            if binding("PyQt4") or binding("PyQt5"):
                # Even when we explicitly pass QWidget we will get QPushButton
                assert type(widget) is QtWidgets.QPushButton, widget
            else:
                assert type(widget) is QtWidgets.QWidget, widget

            # IMPORTANT: this differs across sip and shiboken.
            if binding("PySide") or binding("PySide2"):
                assert widget != button
            else:
                assert widget == button

        finally:
            app.exit()

    def test_implicit_wrapInstance_for_base_types():
        """Tests .wrapInstance implicit cast of `Foo` pointer to `Foo` object

        Testing is based upon the following parameters:

        1. The `base` argument has a default value.
        2. `Foo` is a standard Qt class.

        """
        from Qt import QtCompat, QtWidgets

        app = QtWidgets.QApplication(sys.argv)

        try:
            button = QtWidgets.QPushButton("Hello world")
            button.setObjectName("MySpecialButton")
            pointer = QtCompat.getCppPointer(button)
            widget = QtCompat.wrapInstance(long(pointer))

            assert widget.objectName() == button.objectName()
            assert type(widget) is QtWidgets.QPushButton, widget

            if binding("PySide"):
                assert widget != button
            elif binding("PySide2") and _pyside2_commit_date() is None:
                assert widget != button
            elif binding("PySide2") and \
                    _pyside2_commit_date() <= datetime.datetime(
                        2017, 8, 25):
                assert widget == button
            else:
                assert widget == button

        finally:
            app.exit()

    def test_implicit_wrapInstance_for_derived_types():
        """Tests .wrapInstance implicit cast of `Foo` pointer to `Bar` object

        Testing is based upon the following parameters:

        1. The `base` argument has a default value.
        2. `Bar` is a standard Qt class.
        3. `Foo` is a strict subclass of `Bar`, separated by one or more levels
           of inheritance.
        4. `Foo` is not a standard Qt class.

        Note:
            For sip usage, implicit cast of `Foo` pointer always results in a
            `Foo` object.

        """
        from Qt import QtCompat, QtWidgets

        app = QtWidgets.QApplication(sys.argv)

        try:
            class A(QtWidgets.QPushButton):
                pass

            class B(A):
                pass

            button = B("Hello world")
            button.setObjectName("MySpecialButton")
            pointer = QtCompat.getCppPointer(button)
            widget = QtCompat.wrapInstance(long(pointer))

            assert widget.objectName() == button.objectName()

            if binding("PyQt4") or binding("PyQt5"):
                assert type(widget) is B, widget
            else:
                assert type(widget) is QtWidgets.QPushButton, widget

            if binding("PySide") or binding("PySide2"):
                assert widget != button
            else:
                assert widget == button

        finally:
            app.exit()

    def test_implicit_wrapInstance_expectations():
        """Tests expectations for implicit usage of .wrapInstance

        This includes testing whether the QtCore and QtWidgets namespaces have
        any overlapping QObject subclass names.

        """
        import inspect
        from Qt import QtCore, QtWidgets

        core_class_names = set([attr for attr, value in QtCore.__dict__.items()
                                if inspect.isclass(value) and
                                issubclass(value, QtCore.QObject)])
        widget_class_names = set([attr for attr, value in
                                  QtWidgets.__dict__.items()
                                  if inspect.isclass(value) and
                                  issubclass(value, QtCore.QObject)])
        intersecting_class_names = core_class_names & widget_class_names
        assert not intersecting_class_names

    def test_isValid():
        """.isValid and .delete work in all bindings"""
        from Qt import QtCompat, QtCore, QtWidgets

        app = QtWidgets.QApplication(sys.argv)

        try:
            obj = QtCore.QObject()
            assert QtCompat.isValid(obj)
            QtCompat.delete(obj)
            assert not QtCompat.isValid(obj)

            # Graphics Item
            item = QtWidgets.QGraphicsItemGroup()
            assert QtCompat.isValid(item)
            QtCompat.delete(item)
            assert not QtCompat.isValid(item)

        finally:
            app.exit()


if binding("PyQt4"):
    def test_preferred_pyqt4():
        """QT_PREFERRED_BINDING = PyQt4 properly forces the binding"""
        import Qt
        assert Qt.__binding__ == "PyQt4", (
            "PyQt4 should have been picked, "
            "instead got %s" % Qt.__binding__)

    def test_sip_api_qtpy():
        """Preferred binding PyQt4 should have sip version 2"""

        __import__("Qt")  # Bypass linter warning
        import sip
        assert sip.getapi("QString") == 2, (
            "PyQt4 API version should be 2, "
            "instead is %s" % sip.getapi("QString"))

    if PYTHON == 2:
        def test_sip_api_already_set():
            """Raise ImportError with sip was set to 1 with no hint, default"""
            __import__("PyQt4.QtCore")  # Bypass linter warning
            import sip
            sip.setapi("QString", 1)
            assert_raises(ImportError, __import__, "Qt")

        # A sip API hint of any kind bypasses ImportError
        # on account of it being merely a hint.
        def test_sip_api_1_1():
            """sip=1, hint=1 == OK"""
            import sip
            sip.setapi("QString", 1)
            os.environ["QT_SIP_API_HINT"] = "1"
            __import__("Qt")  # Bypass linter warning

        def test_sip_api_2_1():
            """sip=2, hint=1 == WARNING"""
            import sip
            sip.setapi("QString", 2)
            os.environ["QT_SIP_API_HINT"] = "1"

            with captured_output() as out:
                __import__("Qt")  # Bypass linter warning
                stdout, stderr = out
                assert stderr.getvalue().startswith("Warning:")

        def test_sip_api_1_2():
            """sip=1, hint=2 == WARNING"""
            import sip
            sip.setapi("QString", 1)
            os.environ["QT_SIP_API_HINT"] = "2"

            with captured_output() as out:
                __import__("Qt")  # Bypass linter warning
                stdout, stderr = out
                assert stderr.getvalue().startswith("Warning:")

        def test_sip_api_2_2():
            """sip=2, hint=2 == OK"""
            import sip
            sip.setapi("QString", 2)
            os.environ["QT_SIP_API_HINT"] = "2"
            __import__("Qt")  # Bypass linter warning


if binding("PyQt6"):
    def test_preferred_pyqt6():
        """QT_PREFERRED_BINDING = PyQt6 properly forces the binding"""
        import Qt
        assert Qt.__binding__ == "PyQt6", (
            "PyQt6 should have been picked, "
            "instead got %s" % Qt.__binding__)


if binding("PyQt5"):
    def test_preferred_pyqt5():
        """QT_PREFERRED_BINDING = PyQt5 properly forces the binding"""
        import Qt
        assert Qt.__binding__ == "PyQt5", (
            "PyQt5 should have been picked, "
            "instead got %s" % Qt.__binding__)


if binding("PySide"):
    def test_preferred_pyside():
        """QT_PREFERRED_BINDING = PySide properly forces the binding"""
        import Qt
        assert Qt.__binding__ == "PySide", (
            "PySide should have been picked, "
            "instead got %s" % Qt.__binding__)


if binding("PySide2"):
    def test_preferred_pyside2():
        """QT_PREFERRED_BINDING = PySide2 properly forces the binding"""
        import Qt
        assert Qt.__binding__ == "PySide2", (
            "PySide2 should have been picked, "
            "instead got %s" % Qt.__binding__)

    def test_coexistence():
        """Qt.py may be use alongside the actual binding"""

        from Qt import QtCore
        import PySide2.QtGui

        # Qt remaps QStringListModel
        assert QtCore.QStringListModel

        # But does not delete the original. Older versions of PySide2 had this
        # on QtGui instead of QtCore
        assert hasattr(PySide2.QtCore, "QStringListModel") or hasattr(
            PySide2.QtGui, "QStringListModel"
        )


if binding("PySide6"):
    def test_preferred_pyside6():
        """QT_PREFERRED_BINDING = PySide6 properly forces the binding"""
        import Qt
        assert Qt.__binding__ == "PySide6", (
            "PySide6 should have been picked, "
            "instead got %s" % Qt.__binding__)

    def test_coexistence():
        """Qt.py may be use alongside the actual binding"""

        from Qt import QtCore
        import PySide6.QtCore

        # Qt remaps QStringListModel
        assert QtCore.QStringListModel

        # But does not delete the original
        assert PySide6.QtCore.QStringListModel


if IS_TOX and (binding("PyQt5") or binding("PyQt6") and sys.version_info < (3, 11)):
    # Tox testing only supports PyQt5 and PyQt6. If using python 3.11+ PyQt5 is
    # not available.
    def test_multiple_preferred():
        """QT_PREFERRED_BINDING = more than one binding excludes others"""

        # PySide is the more desirable binding
        current = os.environ["QT_PREFERRED_BINDING"]
        try:
            os.environ["QT_PREFERRED_BINDING"] = os.pathsep.join(
                ["PyQt5", "PyQt6"])
            import Qt

            assert Qt.__binding__ == "PyQt5", (
                "PyQt5 should have been picked, "
                "instead got %s" % Qt.__binding__)
        finally:
            os.environ["QT_PREFERRED_BINDING"] = current


if not IS_TOX and (binding("PyQt4") or binding("PyQt5")):
    # If not using tox, then only PyQt4 and PyQt5 are available to test with.
    def test_multiple_preferred():
        """QT_PREFERRED_BINDING = more than one binding excludes others"""

        # PySide is the more desirable binding
        os.environ["QT_PREFERRED_BINDING"] = os.pathsep.join(
            ["PyQt4", "PyQt5"])

        import Qt
        assert Qt.__binding__ == "PyQt4", (
            "PyQt4 should have been picked, "
            "instead got %s" % Qt.__binding__)


enum_file_1 = u"""
# a comment Qt.WindowActive with an enum. This file uses enums from super-classes
if QAbstractItemView.Box:
    print(QTreeWidget.Box)
    print(QFrame.Box)
"""


enum_file_2 = u"""
# a comment QStyle.CC_ComboBox that has a enum in it
print(QFrame.Box)
"""


enum_check = r"""'__init__.py': Replace 'Qt.WindowActive' => 'Qt.WindowState.WindowActive' (1)
'__init__.py': Replace 'QAbstractItemView.Box' => 'QAbstractItemView.Shape.Box' (1)
'__init__.py': Replace 'QFrame.Box' => 'QFrame.Shape.Box' (1)
'__init__.py': Replace 'QTreeWidget.Box' => 'QTreeWidget.Shape.Box' (1)
'api{slash}example.py': Replace 'QFrame.Box' => 'QFrame.Shape.Box' (1)
'api{slash}example.py': Replace 'QStyle.CC_ComboBox' => 'QStyle.ComplexControl.CC_ComboBox' (1)
"""
enum_check = enum_check.format(slash=os.sep)


if binding("PySide2") and sys.version_info >= (3, 7):
    # Qt_convert_enum.py only runs in python 3.7 or higher
    def test_convert_enum():
        """Test the output of running Qt_convert_enum.py."""

        code_path = os.path.join(os.path.dirname(__file__), "Qt_convert_enum.py")
        old_code_dir = os.path.join(self.tempdir, "enum_convert")
        api_dir = os.path.join(old_code_dir, "api")
        init_file = os.path.join(old_code_dir, "__init__.py")
        example_file = os.path.join(api_dir, "example.py")
        os.makedirs(api_dir)

        # Test the dry run mode text output
        with open(init_file, "w") as fle:
            fle.write(enum_file_1)

        with open(example_file, "w") as fle:
            fle.write(enum_file_2)

        cmd = [sys.executable, code_path, old_code_dir]
        output = subprocess.check_output(cmd, cwd=self.tempdir, universal_newlines=True)

        assert enum_check in output

        # Test actually updating the files.
        cmd.append("--write")
        output = subprocess.check_output(cmd, cwd=self.tempdir, universal_newlines=True)
        assert enum_check in output

        check = enum_file_1.replace("WindowActive", "WindowState.WindowActive")
        check = check.replace("Box", "Shape.Box")
        with open(init_file) as fle:
            assert fle.read() == check

        check = enum_file_2.replace("CC_ComboBox", "ComplexControl.CC_ComboBox")
        check = check.replace("QFrame.Box", "QFrame.Shape.Box")
        with open(example_file) as fle:
            assert fle.read() == check

    def test_convert_enum_map():
        """Test enum map generation for conversion from short to long enums"""
        code_path = os.path.join(os.path.dirname(__file__), "Qt_convert_enum.py")
        cmd = [sys.executable, code_path, "--show", "map"]
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            check=True,
            stderr=subprocess.DEVNULL,
            cwd=self.tempdir,
            universal_newlines=True,
        )

        data = json.loads(proc.stdout)
        assert data['Qt.WindowActive'] == 'Qt.WindowState.WindowActive'
        assert data['QAbstractItemView.Box'] == 'QAbstractItemView.Shape.Box'
        assert data['QFrame.Box'] == 'QFrame.Shape.Box'
        assert data['QTreeWidget.Box'] == 'QTreeWidget.Shape.Box'
        assert data['QFrame.Box'] == 'QFrame.Shape.Box'
        assert data['QStyle.CC_ComboBox'] == 'QStyle.ComplexControl.CC_ComboBox'

    def test_convert_enum_modules():
        """Test enum map generation modules data structure"""
        code_path = os.path.join(os.path.dirname(__file__), "Qt_convert_enum.py")
        cmd = [sys.executable, code_path, "--show", "modules"]
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            check=True,
            stderr=subprocess.DEVNULL,
            cwd=self.tempdir,
            universal_newlines=True,
        )

        data = json.loads(proc.stdout)
        assert data['QtCore']['Qt.WindowActive'] == ['Qt.WindowState.WindowActive']
        assert data['QtWidgets']['QAbstractItemView.Box'] == ['QAbstractItemView.Shape.Box']
        assert data['QtWidgets']['QFrame.Box'] == ['QFrame.Shape.Box']
        assert data['QtWidgets']['QTreeWidget.Box'] == ['QTreeWidget.Shape.Box']
        assert data['QtWidgets']['QFrame.Box'] == ['QFrame.Shape.Box']
        assert data['QtWidgets']['QStyle.CC_ComboBox'] == ['QStyle.ComplexControl.CC_ComboBox']


if binding("PySide6") and sys.version_info >= (3, 7):
    # Qt_convert_enum.py only runs in python 3.7 or higher
    def test_convert_enum_duplicates():
        """Tests using PySide6 to show enums with duplicate short names"""
        code_path = os.path.join(os.path.dirname(__file__), "Qt_convert_enum.py")
        cmd = [sys.executable, code_path, "--show", "dups"]
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            check=True,
            stderr=subprocess.DEVNULL,
            cwd=self.tempdir,
            universal_newlines=True,
        )

        data = json.loads(proc.stdout)

        # Test some know duplicate enum values
        assert "PySide6" in data["BINDING_INFO"]
        assert data["QtGui"]["QColorSpace"]["AdobeRgb"] == [
            "NamedColorSpace.AdobeRgb, 3",
            "Primaries.AdobeRgb, 2",
        ]
