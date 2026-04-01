import sqlite3
from datetime import datetime
from pathlib import Path
import pygame


class Leaderboard:
    """
    Manages the game leaderboard using SQLite3 database.
    Handles score storage, retrieval, and leaderboard queries.
    """
    
    def __init__(self, db_name="leaderboard.db"):
        """Initialize the leaderboard database."""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.init_database()
    
    def init_database(self):
        """Create database and tables if they don't exist."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            
            # Create scores table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_id TEXT
                )
            ''')
            
            # Create index for faster queries
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_score 
                ON scores(score DESC)
            ''')
            
            self.cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_player_name 
                ON scores(player_name)
            ''')
            
            self.connection.commit()
            print(f"Database '{self.db_name}' initialized successfully.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    
    def save_score(self, player_name, score, session_id=None):
        """
        Save a player's score to the database.
        
        Args:
            player_name (str): Name of the player
            score (int): Score achieved
            session_id (str, optional): Unique session identifier
            
        Returns:
            int: The ID of the inserted record, or None if failed
        """
        try:
            self.cursor.execute('''
                INSERT INTO scores (player_name, score, session_id)
                VALUES (?, ?, ?)
            ''', (player_name, score, session_id))
            
            self.connection.commit()
            print(f"Score saved: {player_name} - {score}")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error saving score: {e}")
            return None
    
    def get_top_scores(self, limit=10):
        """
        Get the top scores from the leaderboard.
        
        Args:
            limit (int): Number of top scores to retrieve (default: 10)
            
        Returns:
            list: List of tuples (rank, player_name, score, date_played)
        """
        try:
            self.cursor.execute('''
                SELECT ROW_NUMBER() OVER (ORDER BY score DESC) as rank,
                       player_name, 
                       score, 
                       date_played
                FROM scores
                ORDER BY score DESC
                LIMIT ?
            ''', (limit,))
            
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error retrieving top scores: {e}")
            return []
    

    
    def clear_all_scores(self):
        """
        Clear all scores from the leaderboard (use with caution).
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cursor.execute('DELETE FROM scores')
            self.connection.commit()
            print("All scores cleared.")
            return True
        except sqlite3.Error as e:
            print(f"Error clearing scores: {e}")
            return False
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
    
    def __del__(self):
        """Ensure database is closed when object is destroyed."""
        self.close()


class LeaderboardUI:
    """
    Handles pygame rendering and scrolling UI for the leaderboard.
    """
    
    def __init__(self, screen, leaderboard, title_font, subtitle_font, x=50, y=480-240, width=540, height=500):
        """
        Initialize the leaderboard UI.
        
        Args:
            screen: Pygame screen object
            leaderboard: Leaderboard instance
            title_font: Pygame font for title
            subtitle_font: Pygame font for text
            x: X position of leaderboard on screen
            y: Y position of leaderboard on screen
            width: Width of leaderboard display area
            height: Height of leaderboard display area
        """
        self.screen = screen
        self.leaderboard = leaderboard
        self.title_font = title_font
        self.subtitle_font = subtitle_font
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Scrolling properties
        self.scroll_offset = 0  # pixels scrolled
        self.line_height = 40  # height of each entry
        self.max_visible_lines = height // self.line_height
        
        # Load scores
        self.scores = []
        self.total_lines = 0
        self.refresh_scores()
    
    def refresh_scores(self):
        """Fetch the latest scores from the leaderboard."""
        # Get many scores (adjust limit as needed)
        self.scores = self.leaderboard.get_top_scores(limit=50)
        self.total_lines = len(self.scores)
    
    def handle_scroll_up(self):
        """Scroll up (keyboard or mouse wheel)."""
        self.scroll_offset = max(0, self.scroll_offset - self.line_height * 2)
    
    def handle_scroll_down(self):
        """Scroll down (keyboard or mouse wheel)."""
        max_scroll = max(0, (self.total_lines * self.line_height) - self.height)
        self.scroll_offset = min(max_scroll, self.scroll_offset + self.line_height * 2)
    
    def handle_input(self, event):
        """
        Process input events for scrolling.
        Call this in your game loop with pygame events.
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Mouse wheel up
                self.handle_scroll_up()
            elif event.button == 5:  # Mouse wheel down
                self.handle_scroll_down()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.handle_scroll_up()
            elif event.key == pygame.K_DOWN:
                self.handle_scroll_down()
    
    def draw(self):
        """Draw the leaderboard with scrolling content."""
        # Draw background panel
        pygame.draw.rect(self.screen, (20, 20, 20), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.screen, (100, 100, 100), (self.x, self.y, self.width, self.height), 3)
        
        # Draw title
        title_text = self.title_font.render("LEADERBOARD", True, (255, 215, 0))
        title_rect = title_text.get_rect()
        title_rect.centerx = self.x + self.width // 2
        title_rect.top = self.y - 50
        self.screen.blit(title_text, title_rect)
        
        # Create clipping area for scrolling content
        clip_rect = pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 20)
        clip_surface = self.screen.subsurface(clip_rect)
        
        # Draw content within clipping area
        line_y = -self.scroll_offset
        
        for rank, player_name, score, date_played in self.scores:
            # Only draw if line is within visible bounds
            if line_y + self.line_height > 0 and line_y < self.height - 20:
                # Draw rank and name
                rank_text = f"#{rank} {player_name}"
                text_surface = self.subtitle_font.render(rank_text, True, (255, 255, 255))
                clip_surface.blit(text_surface, (10, line_y + 5))
                
                # Draw score on the right
                score_text = f"{score:,}"
                score_surface = self.subtitle_font.render(score_text, True, (0, 255, 100))
                score_rect = score_surface.get_rect()
                score_rect.right = self.width - 30
                score_rect.top = line_y + 5
                clip_surface.blit(score_surface, (score_rect.x - self.x - 10, line_y + 5))
                
                # Draw separator line
                pygame.draw.line(clip_surface, (50, 50, 50), (5, line_y + self.line_height - 2), 
                               (self.width - 25, line_y + self.line_height - 2), 1)
            
            line_y += self.line_height
        
        # Draw scrollbar
        self._draw_scrollbar()
        
        # Draw "no scores" message if empty
        if self.total_lines == 0:
            no_scores_text = self.subtitle_font.render("No scores yet", True, (150, 150, 150))
            no_scores_rect = no_scores_text.get_rect()
            no_scores_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
            self.screen.blit(no_scores_text, no_scores_rect)
    
    def _draw_scrollbar(self):
        """Draw a scrollbar on the right side of the leaderboard."""
        scrollbar_x = self.x + self.width - 15
        scrollbar_width = 8
        scrollbar_height = self.height - 20
        
        # Scrollbar background
        pygame.draw.rect(self.screen, (30, 30, 30), 
                        (scrollbar_x, self.y + 10, scrollbar_width, scrollbar_height))
        
        # Calculate scrollbar thumb position and size
        if self.total_lines > 0:
            total_content_height = self.total_lines * self.line_height
            thumb_height = max(20, (scrollbar_height / total_content_height) * scrollbar_height)
            thumb_y_ratio = self.scroll_offset / max(1, total_content_height - self.height)
            thumb_y = self.y + 10 + (thumb_y_ratio * (scrollbar_height - thumb_height))
            
            # Scrollbar thumb
            pygame.draw.rect(self.screen, (100, 100, 100), 
                           (scrollbar_x, thumb_y, scrollbar_width, thumb_height))
            pygame.draw.rect(self.screen, (150, 150, 150), 
                           (scrollbar_x, thumb_y, scrollbar_width, thumb_height), 1)

