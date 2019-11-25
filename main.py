from common import *
from html2latex import html_to_console_style


class MyTerminal(gtk.Window):

    def __init__(self):
        super(gtk.Window, MyTerminal).__init__(self)
        self._init_terminal()
        self._init_object()
        self._init_binding()
        self._init_context_menu()

    def _init_terminal(self):
        envs = ['{}={}'.format(a, b) for a, b in os.environ.items()]
        # initialize vte terminal
        self.terminal = vte.Terminal()
        self.terminal.spawn_sync(
            vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ['/bin/bash'],
            envs,
            glib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,)
        self.add(self.terminal)

    def _init_object(self):
        self.cmenu = gtk.Menu.new()
        self.clipboard = gtk.Clipboard.get(gdk.SELECTION_CLIPBOARD)

    def _init_binding(self):
        self.connect('delete-event', gtk.main_quit)
        self.connect('button-press-event', self._evt_global_click)

    def _evt_global_click(self, widget, event):
        if event.type == gdk.EventType.BUTTON_PRESS and event.button == 3:
            self.cmenu.popup_at_pointer()

        return True

    def _evt_menuitem_copy(self, event):
        self.terminal.copy_clipboard()

    def _evt_menuitem_paste(self, event):
        self.terminal.paste_clipboard()


    def _evt_menuitem_copy_html(self, event):
        self.terminal.copy_clipboard_format(vte.Format.HTML)

    def _evt_menuitem_copy_latex(self, event):
        self.terminal.copy_clipboard_format(vte.Format.HTML)
        copied = self._get_clipboard_text()
        if copied is not None:
            try:
                latex = html_to_console_style(copied)
                self._set_clipboard_text(latex)
            except Exception as e:
                print('error occurred during HTML to LaTeX conversion: \n', e, file=sys.stderr)

    def _get_clipboard_text(self):
        text = self.clipboard.wait_for_text()
        return text

    def _set_clipboard_text(self, text):
        self.clipboard.set_text(text, -1)

    def _init_context_menu(self):
        menuSpec = [
            ('Copy', self._evt_menuitem_copy),
            ('Paste', self._evt_menuitem_paste),
            'sep',
            ('Copy HTML', self._evt_menuitem_copy_html),
            ('Copy LaTeX', self._evt_menuitem_copy_latex)
        ]
        for item in menuSpec:
            if isinstance(item, tuple):
                cmItem = gtk.MenuItem.new_with_label(item[0])
                cmItem.connect('activate', item[1])
                self.cmenu.append(cmItem)
            elif isinstance(item, str):
                if item == 'sep':
                    cmItem = gtk.SeparatorMenuItem.new()
                    self.cmenu.append(cmItem)
        self.cmenu.show_all()


if __name__ == '__main__':
    window = MyTerminal()
    window.show_all()
    gtk.main()