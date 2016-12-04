#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of nautilus-copypaste-images
#
# Copyright (C) 2016 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from gi.repository import Nautilus as FileManager
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
import urllib
import os
import locale
import gettext


def get_suported_extensions():
    temp = []
    for aformat in GdkPixbuf.Pixbuf.get_formats():
        tmp_extensions = aformat.get_extensions()
        temp.extend(tmp_extensions)
    extensions = []
    for extension in temp:
        extensions.append('.'+extension)
    return extensions

EXTENSIONS = get_suported_extensions()
SAVETO = ['.png', '.jpg', '.tif', '.ico', '.bmp']
SEPARATOR = u'\u2015' * 10
NAME = 'Nautilus'
LANGDIR = '/usr/share/locale-langpack'
APP = 'nautilus-copypaste-images'
ICON = 'image'
VERSION = '0.1.0-0extras15.10.0'

try:
    current_locale, encoding = locale.getdefaultlocale()
    language = gettext.translation(APP, '/usr/share/locale-langpack',
                                   [current_locale])
    language.install()
    _ = language.ugettext
except Exception as e:
    print(e)
    _ = str


def get_files(files_in):
    files = []
    for file_in in files_in:
        file_in = urllib.unquote(file_in.get_uri()[7:])
        fileName, fileExtension = os.path.splitext(file_in)
        if fileExtension.lower() in EXTENSIONS and os.path.isfile(file_in):
            files.append(file_in)
    return files


class CopyPasteImagesMenuProvider(GObject.GObject, FileManager.MenuProvider):
    """Implements the 'Replace in Filenames' extension to the FileManager
    right-click menu"""

    def __init__(self):
        """FileManager crashes if a plugin doesn't implement the __init__
        method"""
        atom = Gdk.atom_intern('CLIPBOARD', True)
        self.clipboard = Gtk.Clipboard.get(atom)
        pass

    def all_files_are_images(self, items):
        for item in items:
            fileName, fileExtension = os.path.splitext(item.get_uri()[7:])
            if fileExtension.lower() not in EXTENSIONS:
                return False
        return True

    def about(self, menu):
        ad = Gtk.AboutDialog()
        ad.set_name(APP)
        ad.set_icon_name(ICON)
        ad.set_version(VERSION)
        ad.set_copyright('Copyrignt (c) 2013-2014\nLorenzo Carbonell')
        ad.set_comments(_('Tools to copy and paste images'))
        ad.set_license(
            """
This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
""")
        ad.set_website('http://www.atareao.es')
        ad.set_website_label('http://www.atareao.es')
        ad.set_authors([
            'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
        ad.set_documenters([
            'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
        ad.set_program_name(APP)
        ad.set_logo_icon_name(ICON)
        ad.run()
        ad.destroy()

    def get_file_items(self, window, sel_items):
        """
        Adds the 'Replace in Filenames' menu item to the FileManager
        right-click menu, connects its 'activate' signal to the 'run' method
        passing the selected Directory/File
        """
        # if not self.all_files_are_images(sel_items):
        #    return
        top_menuitem = FileManager.MenuItem(
            name='CopyPasteImagesMenuProvider::Gtk-image-tools',
            label=_('CopyPaste Images'),
            tip=_('Tools to copy and paste images'),
            icon='Gtk-find-and-replace')
        submenu = FileManager.Menu()
        top_menuitem.set_submenu(submenu)
        if self.all_files_are_images(sel_items):
            sub_menuitem01 = FileManager.MenuItem(
                name='CopyPasteImagesMenuProvider::Gtk-copy-image',
                label='Copy image',
                tip='Copy image to clipboard')
            sub_menuitem01.connect('activate', self.copy_image, sel_items)
            submenu.append_item(sub_menuitem01)
        if self.clipboard.wait_is_image_available():
            sub_menuitem02 = FileManager.MenuItem(
                name='CopyPasteImagesMenuProvider::Gtk-paste-image',
                label='Paste image',
                tip='Paste image from the clipboard')
            sub_menuitem02.connect('activate', self.paste_image)
            submenu.append_item(sub_menuitem02)
        sub_menuitem_98 = FileManager.MenuItem(
            name='CopyPasteImagesMenuProvider::Gtk-none',
            label=SEPARATOR)
        submenu.append_item(sub_menuitem_98)
        sub_menuitem_99 = FileManager.MenuItem(
            name='CopyPasteImagesMenuProvider::Gtk-document-converter-99',
            label=_('About'),
            tip=_('About'),
            icon='Gtk-find-and-replace')
        sub_menuitem_99.connect('activate', self.about)
        submenu.append_item(sub_menuitem_99)
        return top_menuitem,

    def get_background_items(self, window, file):
        top_menuitem = FileManager.MenuItem(
            name='CopyPasteImagesMenuProvider::Gtk-image-tools',
            label=_('CopyPaste Images'),
            tip=_('Tools to copy and paste images'),
            icon='Gtk-find-and-replace')
        submenu = FileManager.Menu()
        top_menuitem.set_submenu(submenu)
        if self.clipboard.wait_is_image_available():
            sub_menuitem02 = FileManager.MenuItem(
                name='CopyPasteImagesMenuProvider::Gtk-paste-image',
                label='Paste image',
                tip='Paste image from the clipboard')
            sub_menuitem02.connect('activate', self.paste_image)
            submenu.append_item(sub_menuitem02)
        sub_menuitem_98 = FileManager.MenuItem(
            name='CopyPasteImagesMenuProvider::Gtk-none',
            label=SEPARATOR)
        submenu.append_item(sub_menuitem_98)
        sub_menuitem_99 = FileManager.MenuItem(
            name='CopyPasteImagesMenuProvider::Gtk-document-converter-99',
            label=_('About'),
            tip=_('About'),
            icon='Gtk-find-and-replace')
        sub_menuitem_99.connect('activate', self.about)
        submenu.append_item(sub_menuitem_99)
        return top_menuitem,

    def copy_image(self, menu, files):
        files = get_files(files)
        if len(files) > 0:
            afile = files[0]
            if not os.path.exists(afile):
                md = Gtk.MessageDialog(parent=None,
                                       flags=Gtk.DialogFlags.MODAL |
                                       Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                       type=Gtk.MessageType.ERROR,
                                       buttons=Gtk.ButtonsType.OK,
                                       message_format='No existe el archivo')
                md.run()
                exit(-1)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(afile)
            # atom = Gdk.atom_intern('CLIPBOARD', True)
            # clipboard = Gtk.Clipboard.get(atom)
            self.clipboard.set_image(pixbuf)
            self.clipboard.store()

    def paste_image(self, menu):
        # atom = Gdk.atom_intern('CLIPBOARD', True)
        # clipboard = Gtk.Clipboard.get(atom)
        pixbuf = self.clipboard.wait_for_image()
        if pixbuf is not None:
            dialog = Gtk.FileChooserDialog('Guardar la imagen del\
                                            portapapeles como ...',
                                           None,
                                           Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_CANCEL,
                                            Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN,
                                            Gtk.ResponseType.OK))
            dialog.set_default_response(Gtk.ResponseType.OK)
            dialog.set_do_overwrite_confirmation(True)
            dialog.set_current_folder(os.getenv('HOME'))
            dialog.set_filename('from_copy_paste.png')
            filter = Gtk.FileFilter()
            filter.set_name('Imagenes')
            filter.add_mime_type('image/png')
            filter.add_mime_type('image/jpeg')
            filter.add_mime_type('image/tiff')
            filter.add_mime_type('image/ico')
            filter.add_mime_type('image/bmp')
            filter.add_pattern('*.png')
            filter.add_pattern('*.jpg')
            filter.add_pattern('*.tif')
            filter.add_pattern('*.ico')
            filter.add_pattern('*.bmp')
            dialog.add_filter(filter)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                filename = dialog.get_filename()
                dialog.destroy()
                print filename
                jpeg”, “png”, “tiff”, “ico” or “bmp”
                if filename[-4:].lower() in SAVETO:
                    pixbuf.savev(filename, filename[-3:].lower(), (), ())
                else:
                    filename = filename + '.png'
                    pixbuf.savev(filename, 'png', (), ())

if __name__ == '__main__':
    '''
    atom = Gdk.atom_intern('CLIPBOARD', True)
    clipboard = Gtk.Clipboard.get(atom)
    print(clipboard.wait_is_image_available())
    afile = '/home/lorenzo/Escritorio/ejemplo/5647177212_30a527c038_b.jpg'
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(afile)
    # atom = Gdk.atom_intern('CLIPBOARD', True)
    # clipboard = Gtk.Clipboard.get(atom)
    clipboard.set_image(pixbuf)
    clipboard.store()
    print(clipboard.wait_is_image_available())
    '''
