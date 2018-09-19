# main.py
#
# Copyright 2018 Romain F. T.
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

import sys
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GLib, Gdk

from .window import DynamicWallpaperEditorWindow

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.github.maoschanz.DynamicWallpaperEditor',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        GLib.set_application_name('Dynamic Wallpaper Editor')
        GLib.set_prgname('com.github.maoschanz.DynamicWallpaperEditor')

        self.register(None)
        menu = self.build_app_menu()
        if self.prefers_app_menu():
            self.set_app_menu(menu)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = DynamicWallpaperEditorWindow(application=self)
        win.present()

    def build_app_menu(self):
        builder = Gtk.Builder()
        builder.add_from_resource("/com/github/maoschanz/DynamicWallpaperEditor/menus.ui")
        menu = builder.get_object("app-menu")

        new_window_action = Gio.SimpleAction.new("new_window", None)
        new_window_action.connect("activate", self.on_new_window_activate)
        self.add_action(new_window_action)

        shortcuts_action = Gio.SimpleAction.new("shortcuts", None)
        shortcuts_action.connect("activate", self.on_shortcuts_activate)
        self.add_action(shortcuts_action)

        help_action = Gio.SimpleAction.new("help", None)
        help_action.connect("activate", self.on_help_activate)
        self.add_action(help_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_activate)
        self.add_action(about_action)

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action)

        self.set_accels_for_action("app.new_window", ["<Ctrl>n"])
        self.set_accels_for_action("app.quit", ["<Ctrl>q"])
        self.set_accels_for_action("win.save", ["<Ctrl>s"])
        self.set_accels_for_action("win.open", ["<Ctrl>o"])
        self.set_accels_for_action("win.add", ["<Ctrl>a"])
        self.set_accels_for_action("win.set_as_wallpaper", ["<Ctrl>w"])

        return menu

    def on_about_activate(self, *args):
        self.build_about_dialog()
        self.about_dialog.show()

    def on_help_activate(self, *args):
        Gtk.show_uri(None, "help:dynamic-wallpaper-editor", Gdk.CURRENT_TIME)

    def on_quit(self, *args):
        self.quit()

    def on_new_window_activate(self, *args):
        win = DynamicWallpaperEditorWindow(application=self)
        win.present()

    def on_shortcuts_activate(self, *args):
        builder = Gtk.Builder().new_from_resource('/com/github/maoschanz/DynamicWallpaperEditor/shortcuts.ui')
        self.shortcuts_window = builder.get_object('shortcuts')
        self.shortcuts_window.present()

    def build_about_dialog(self):
        self.about_dialog = Gtk.AboutDialog.new()
        self.about_dialog.set_version('1.7') # TODO
        self.about_dialog.set_comments(_("Create or edit dynamic wallpapers for GNOME."))
        self.about_dialog.set_authors(['Romain F. T.'])
        self.about_dialog.set_copyright('© 2018 Romain F. T.')
        self.about_dialog.set_license_type(Gtk.License.GPL_3_0)
        self.about_dialog.set_logo_icon_name('com.github.maoschanz.DynamicWallpaperEditor')
        self.about_dialog.set_website('https://github.com/maoschanz/dynamic-wallpaper-editor')
        self.about_dialog.set_website_label(_("Report bugs or ideas"))
        self.about_dialog.set_translator_credits(_("translator-credits"))

def main(version):
    app = Application()
    return app.run(sys.argv)
