class Element:
    def __init__(self, screen, pos):
        self.screen = screen
        self.pos = pos
        self.state = 0
        self.wire_connectors = []
        self.input_wires = [] # List of wires that connect to this light
        self.deleted = False # Whether to delete the element next frame

    # Draw the element
    def draw(self):
        pass

    # Update the state of the element based on the input elements
    def update(self):
        pass

    # Set the position of the element
    def set_pos(self, pos):
        self.pos = pos

    # Return True if the element was clicked
    def handle_click(self, mouse_pos):
        return False
    
    # Handle the menu creation
    def handle_menu_create(self, mouse_pos):
        return None
    
    # Create a new element
    def create_new_element(self, mouse_pos):
        return None
    
    # Delete the element
    def delete(self):
        self.deleted = True
        # Try except since element may already be deleted
        try:
            self.input_wires.remove(self)
        except ValueError:
            pass