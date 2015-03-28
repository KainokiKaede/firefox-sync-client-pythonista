import os
import ui
import json
import console
import webbrowser
from updatebookmarks import update_bookmarks


class BookmarkData(object):
    def __init__(self):
        self.filepath = os.path.join(os.environ['HOME'],'Documents','bookmarks.json')
        try:
            self.reset()
        except IOError:
            self.update()
            self.reset()

    def reset(self):
        with open(self.filepath) as in_file:
            bookmarks = json.load(in_file)
        self.bookmarks_dict = dict([[item[u'id'], item] for item in bookmarks])

    def update(self):
        update_bookmarks(self.filepath)
        self.reset()

bookmarkdata = BookmarkData()


class BookmarkItem(object):
    def __init__(self, item):
        self.item = item

    def isdir(self):
        if self.item.get(u'type') == u'folder': return True
        else: return False

    def isseparator(self):
        if self.item.get(u'type') == u'separator': return True
        else: return False

    def isbookmark(self):
        if self.item.get(u'type') == u'bookmark': return True
        else: return False

    def set_icon(self):
        if self.isdir(): filename = 'ionicons-ios7-folder-24'
        elif self.isbookmark(): filename = 'ionicons-ios7-bookmarks-outline-24'
        elif self.isseparator(): filename = ''
        else: filename = ''
        self.icon = ui.Image.named(filename)

    def as_cell(self):
        # Create a ui.TableViewCell for use with BookmarkDataSource
        cell = ui.TableViewCell("subtitle")
        cell.text_label.text = self.item.get(u'title', u'')
        self.set_icon()
        cell.image_view.image = self.icon
        cell.accessory_type = 'disclosure_indicator' if self.isdir() else 'none'
        return cell


class BookmarkDataSource(object):
    # ui.TableView data source that lists bookmarks
    def __init__(self, id):
        self.bookmarks = [[BookmarkItem(bookmarkdata.bookmarks_dict[item]) for item in bookmarkdata.bookmarks_dict[id].get(u'children', [])]]

    def tableview_number_of_sections(self, tableview):
        # Return the number of sections (defaults to 1)
        return 1

    def tableview_number_of_rows(self, tableview, section):
        # Return the number of rows in the section
        assert section == 0
        return len(self.bookmarks[section])

    def tableview_cell_for_row(self, tableview, section, row):
        # Create and return a cell for the given section/row
        assert section == 0
        return self.bookmarks[section][row].as_cell()

    # def tableview_title_for_header(self, tableview, section):
    #     # Return a title for the given section.
    #     # If this is not implemented, no section headers will be shown.
    #     return 'Some Section'

    def tableview_can_delete(self, tableview, section, row):
        # Return True if the user should be able to delete the given row.
        return False

    def tableview_can_move(self, tableview, section, row):
        # Return True if a reordering control should be shown for the given row (in editing mode).
        return False

    def tableview_delete(self, tableview, section, row):
        # Called when the user confirms deletion of the given row.
        pass

    def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
        # Called when the user moves a row with the reordering control (in editing mode).
        pass

    @ui.in_background
    def tableview_did_select(self, tableview, section, row):
        # Called when the user selects a row
        assert section == 0
        if not tableview.editing:
            item = self.bookmarks[section][row]
            if item.isdir():
                console.show_activity()
                nav.push_view(make_file_list(item.item[u'id']))
                console.hide_activity()
            elif item.isbookmark():
                webbrowser.open(u'safari-'+item.item[u'bmkUri'])
            elif item.isseparator():
                pass

def close_proxy():
    # Returns a function that closes the main view
    def _close(sender):
        nav.close()
    return _close

def update_proxy(parent):
    # Returns a function that updates bookmarks dictionary
    def _update(sender):
        sendertitletmp = sender.title
        sender.title = 'Updating...'
        console.show_activity()
        bookmarkdata.update()
        console.hide_activity()
        sender.title = sendertitletmp
        nav.push_view(make_file_list())
    return _update

def make_file_list(id=u'menu'):
    # Create a ui.TableView containing a directory listing of path
    lst = ui.TableView(flex="WH")
    lst.allows_selection = True
    lst.allows_multiple_selection = False
    lst.allows_selection_during_editing = False
    lst.allows_multiple_selection_during_editing = False
    lst.background_color = 1.0
    lst.data_source = lst.delegate = BookmarkDataSource(id)
    lst.name = "Bookmarks" if id==u'menu' else bookmarkdata.bookmarks_dict[id].get(u'title', '')
    lst.right_button_items = ui.ButtonItem(title="Update", action=update_proxy(lst)),
    lst.left_button_items = ui.ButtonItem(image=ui.Image.named("ionicons-close-24"), action=close_proxy()),
    return lst

def run(mode="popover"):
    # Run the main UI application
    global nav

    lst = make_file_list()
    nav = ui.NavigationView(lst)
    nav.navigation_bar_hidden = False
    nav.flex = "WH"
    if mode == "popover":
        nav.height = 1000
    nav.present(mode, hide_title_bar=True)

if __name__ == "__main__":
    run()
