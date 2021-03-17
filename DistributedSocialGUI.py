import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from Profile import Profile, Post
from NaClProfile import NaClProfile
import ds_client
import ds_messenger




"""
A subclass of tk.Frame that is responsible for drawing the user selection panel 
"""
class Body(tk.Frame):
    def __init__(self, root, select_callback=None, set_new_text=None):
        # initialize tkinter objects
        tk.Frame.__init__(self, root) 
        self.root = root
        
        # declare a callback to attempt to send the message in the user chatbox
        self._select_callback = select_callback
        # declare a callback to change the text in the user chatbox
        self._new_text_callback = set_new_text

        # a list of the users available to contact through the gui
        self._users = []
        # stored index of the current selection (to properly be able to send to the proper user)
        self.chat_user = None
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()

    """
    Sets the text to be displayed in the entry_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """
    def set_text_entry(self, text:str):
        self.entry_editor.delete(0.0, 'end')
        self.entry_editor.insert(0.0, text)
        pass

    def get_text_entry(self) -> str:
        return self.entry_editor.get('1.0', 'end').rstrip()
    
    """
    Update the entry_editor with the selected user's messages when the corresponding node in the posts_tree
    is selected.
    """
    def node_select(self, event):
        index = int(self.users_tree.selection()[0])-1 #selections are not 0-based, so subtract one.
        print(index)
        print(self._users)
        self.chat_user = self._users[index]

        if self._new_text_callback != None:
            self._new_text_callback()
    
    """
    Populates the self._posts attribute with posts from the active DSU file.
    """
    def set_users(self, users:list):
        self._users = users
        for id, users in enumerate(self._users):
            self._insert_users_tree(id + 1, users)

    """
    Inserts a single post to the post_tree widget.
    """
    def insert_user(self, user:str):
        self._users.append(user)
        self._insert_users_tree(len(self._users), user)

    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """
    def reset_ui(self):
        self.users = []
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

    """
    Inserts a post entry into the posts_tree widget.
    """
    def _insert_users_tree(self, id, user:str):
        self.users_tree.insert('', id, id, text=user)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        users_frame = tk.Frame(master=self, width=250)
        users_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.users_tree = ttk.Treeview(users_frame)
        self.users_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.users_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        receipt_frame = tk.Frame(master=self)
        receipt_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=[0,5])


        # create text frame with scrollbar bound above the footer
        frame_within_below =tk.Frame(master=receipt_frame, bg='green')
        frame_within_below.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False, padx=5, pady=5)

        self.entry_editor = tk.Text(frame_within_below, )
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        scroll_frame_chat = tk.Frame(master=frame_within_below)
        scroll_frame_chat.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame_chat, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

        # create short frame divider to keep distance between frames constant
        frame_within_hidden = tk.Frame(master=receipt_frame, height=5, bg='blue')
        frame_within_hidden.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False)

        # create a 'label' (subject to ve 
        frame_within_above = tk.Frame(master=receipt_frame, bg='red', padx=5, pady=5)
        frame_within_above.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False)

        self.body_label = tk.Label(master=frame_within_above, text="wowww\n\n\n", relief='groove')
        self.body_label.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
##
##        scroll_frame_display = tk.Frame(master=frame_within_above, bg="blue")
##        scroll_frame_display.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
##
##        body_label_scrollbar = tk.Scrollbar(master=scroll_frame_display, command=self.body_label.yview)
##        self.body_label['yscrollcommand'] = body_label_scrollbar.set
##        body_label_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)




"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""

class Footer(tk.Frame):
    def __init__(self, root, save_callback=None, add_callback=None):
        # initialize tk elements
        tk.Frame.__init__(self, root)
        self.root = root
        
        # callback to send
        self._save_callback = save_callback
        # callback to add
        self._add_callback = add_callback

        # draw elements
        self._draw()
    

    """
    Calls the callback function specified in the save_callback class attribute, if
    available, when the save_button has been clicked.
    """
    def save_click(self):
        if self._save_callback is not None:
            self._save_callback()

    """
    Calls the other callback function specified in the add_callback class attribute, if
    available, when the add_button has been clicked.
    """
    def add_click(self):
        if self._add_callback is not None:
            self._add_callback()
    """
    Updates the text that is displayed in the footer_label widget
    """

    def set_status(self, message):
        self.footer_label.configure(text=message)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=10, bg='blue')
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=[0,5], pady=5)

        add_button = tk.Button(master=self, text="Add User", width=11, bg='blue')
        add_button.configure(command=self.add_click)
        add_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=[69,0], pady=5)

        

##        self.footer_label = tk.Label(master=self, text="Ready.") #think about making this display the status of the most recent message; ie 'sent!' or 'failed to send!'
##        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=False)


"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the NaClProfile class.
"""
class MainApp(tk.Frame):
    def __init__(self, root, _is_online=False, _profile_filename=None):
        tk.Frame.__init__(self, root)
        self.root = root
        
        self._profile_filename = _profile_filename
        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile = NaClProfile()

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        
    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()


    def refresh_ui(self):
        #if self.body_user.chat_user != None:

            #take elements of retrieve all/retrieve new and return DirectMessage objects with .name == chat_user
            #order the list            

        # use the list to create a string of  text (appropriately split by lines by message ordered by time)

        # append entry to the text body
        
        self.body.set_text_entry("")


    def add_user(self):
        addeduser = tk.simpledialog.askstring("User entry:", "Recipient to chat with:") #change title to edit keys, prompt to include current keys as a lines
        self.body.insert_user(addeduser)
        self.refresh_ui()

    
    """
    Saves the text currently in the entry_editor widget to the active DSU file.
    """
    def send_message(self):
        message_to_send = self.body.get_text_entry()
        user_recipient = self.body.chat_user

        

        

        
        # send message to recipient, catch errors


    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        # The Body and Footer classes must be initialized and packed into the root window.
        self.footer = Footer(self.root, save_callback=self.send_message, add_callback=self.add_user)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
        
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)



        # set initial conditions for testing:
        testusers = ['mary', 'shelly', 'hegel']
        for item in testusers:
            self.body.insert_user(item)
        usermessages = [{'name': 'mary', 'message': 'wow!!', 'timestamp':''}, {'name': 'shelly', 'message': 'wow1!!'}, {'name': 'shelly', 'message': 'wow2!!'}, {'name': 'mary', 'message': 'wow3!!'}]



if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Demo")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()
