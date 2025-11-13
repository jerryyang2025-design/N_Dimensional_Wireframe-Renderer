"""
Main module for the N-Dimensional Wireframe Renderer.

Initializes Pygame, sets up the display and runtime states, shows a welcome message,
and runs the main event loop. This is the entry point for the application.
"""

import data
import events
import panel
import pygame

def initialize():
    """Set up the display, fill background, and show welcome message."""
    # Initialize classes
    data.display.initialize_pygame()
    data.display.screen.fill(data.display.screen_color)
    
    # Welcome message
    print("\n" + "═" * 70)
    print("★  N-Dimensional Wireframe Renderer  ★".center(70))
    print("A geometric visualization tool for exploring higher dimensions".center(70))
    print("═" * 70)
    print()
    print("Welcome! Here are some quick tips to get started:")
    panel.actions()
    panel.command_options()
    
    text = data.display.font.render("Press '/' to open command panel",True,data.display.font_color)
    data.display.screen.blit(text,(data.display.spacing,data.display.side - 2 * data.display.spacing))

def main():
    """Run the main program loop until the user quits."""
    initialize()
    panel.panel()
    
    # Check for inputs
    while not data.states.quit:
        events.handle_events()
    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[ERROR] Unexpected error: " + str(e))
    finally:
        pygame.quit()