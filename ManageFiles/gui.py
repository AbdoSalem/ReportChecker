from gi.repository import Gtk, Gio

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Stack Demo")
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Browse students"
        self.set_titlebar(hb)
        
        self.set_border_width(10)
        self.set_default_size(1000, 700)        
        
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        
        self.student_section_grid = Gtk.Table(1, 8, False)
        
        self.hbox = Gtk.Box()
        
        self.vbox.pack_start(self.student_section_grid, True, True, 0)
        self.vbox.pack_start(self.hbox, True, False, 0)
        
        self.section_entry = Gtk.Entry()
        self.section_label = Gtk.Label()
        self.section_label.set_text('Section: ')
        
        self.student_entry = Gtk.Entry()
        self.student_label = Gtk.Label()
        self.student_label.set_text('Student: ')
        
        self.student_section_grid.attach(self.section_label, 0, 1, 0, 1)
        self.student_section_grid.attach(self.section_entry, 1, 3, 0, 1)
        
        self.student_section_grid.attach(self.student_label, 5, 6, 0, 1)
        self.student_section_grid.attach(self.student_entry, 6, 8, 0, 1)
        
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
        
        
        self.SectionsTable = Gtk.Table(3, 3, False)
        
        self.section_date_label = Gtk.Label()
        self.section_date_label.set_text("Section Date:")
        self.section_absence_label = Gtk.Label()
        self.section_absence_label.set_text("The student ")
        self.section_date = Gtk.Calendar()
        self.section_absence = Gtk.CheckButton("Came") 
        
        self.SectionsTable.attach(self.section_date_label, 0, 1, 0, 1)
        self.SectionsTable.attach(self.section_date, 1, 3, 0, 2)
        self.SectionsTable.attach(self.section_absence_label, 0, 1, 2, 3)
        self.SectionsTable.attach(self.section_absence, 1, 2, 2, 3)
        
        stack.add_titled(self.SectionsTable, "Section", "Section")
        
        self.ReportsTable = Gtk.Table(3, 4, False)
        
        self.report_label = Gtk.Label()
        self.report_label.set_text("Report Name:")
        self.report_name = Gtk.Entry()
        self.report_file_label = Gtk.Label()
        self.report_file_label.set_text("Path:  ")
        hbox = Gtk.Box(spacing=6)
        self.report_file_entry = Gtk.Entry()
        self.report_file_browse = Gtk.Button("...") 
        self.report_file_browse.connect("clicked", self.browse)
        
        self.ReportsTable.attach(self.report_label, 0, 1, 0, 1)
        self.ReportsTable.attach(self.report_name, 1, 2, 0, 1)
        hbox.pack_start(self.report_file_label, False, False, 0)
        hbox.pack_start(self.report_file_entry, False, False, 0)
        hbox.pack_start(self.report_file_browse, False, False, 0)
        self.ReportsTable.attach(self.report_file_label , 0, 1, 1, 2)
        self.ReportsTable.attach(hbox , 0, 4, 1, 2)
        
        
        stack.add_titled(self.ReportsTable, "Reports", "Reports")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        self.vbox.pack_start(stack_switcher, True, True, 0)
        self.vbox.pack_start(stack, True, True, 0)
       
        self.treeview = Gtk.TreeView()
        self.vbox.pack_end(self.treeview, True, True, 0)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        self.left_button = Gtk.Button()
        self.left_button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(self.left_button)
        self.left_button.connect("clicked", self.previous_student)

        self.right_button = Gtk.Button()
        self.right_button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(self.right_button)
        self.right_button.connect("clicked", self.next_student)
        
        hb.pack_start(box)
        
    def next_student(self, widget):
        print 'next'

    def previous_student(self, widget):
        print 'previous'
    
    def browse(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
    
    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

        dialog.destroy()

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
