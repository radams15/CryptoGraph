import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class EntryDialog(Gtk.MessageDialog):
    def __init__(self, *args, hidden=False, **kwargs):
        if 'default_value' in kwargs:
            default_value = kwargs['default_value']
            del kwargs['default_value']
        else:
            default_value = ''
        super(EntryDialog, self).__init__(*args, **kwargs)
        entry = Gtk.Entry()
        if hidden:
            entry.set_visibility(False)
        entry.set_text(str(default_value))
        entry.connect("activate",
                      lambda ent, dlg, resp: dlg.response(resp),
                      self, Gtk.ResponseType.OK)
        self.vbox.pack_end(entry, True, True, 0)
        self.vbox.show_all()
        self.entry = entry
    def set_value(self, text):
        self.entry.set_text(text)
    def run(self):
        result = super(EntryDialog, self).run()
        if result == Gtk.ResponseType.OK:
            text = self.entry.get_text()
        else:
            text = None
        return text