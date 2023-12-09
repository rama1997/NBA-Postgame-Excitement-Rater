import rumps
import webbrowser
import schedule
import time
import threading
import menu_app.output_helper_menu_app as output
from yt_api import get_recent_NBA_videos


class NBAMenuApp(rumps.App):
    def __init__(self):
        super(NBAMenuApp, self).__init__("NBA")
        self.menu = self.build_menu()
        self.update_menu_game()

        # Schedule the function to run every hour
        schedule.every(10).minutes.do(lambda: self.refresh_menu(self))

        # Start the scheduler in a separate thread
        schedule_thread = threading.Thread(target=self.run_schedule)
        schedule_thread.start()

    def run_schedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def build_menu(self):
        return ["Refresh"]

    def update_menu_game(self):
        self.add_menu_item(output.get_todays_date())
        games = output.get_games_to_rate()
        youtube_highlights = get_recent_NBA_videos()
        if games != []:
            for game in games:
                game_title = output.get_game_title(game)
                self.add_game_item(game_title, game)
                game_rating = output.get_game_rating(game)
                self.menu[game_title].add(game_rating)
                if "Worth" in game_rating:
                    url = output.get_highlight_video_url(game, youtube_highlights)
                    if url:
                        self.menu[game_title].add("Highlight video found.")
                        self.menu[game_title].add(url)
                    else:
                        self.menu[game_title].add("Can not find highlight video.")
                        self.menu[game_title].add("https://www.youtube.com/@NBA/videos")
        else:
            self.add_menu_item("No games today")

    def game_click(self, sender, game):
        for item in sender:
            if "youtube" in item:
                webbrowser.open(item)
                break

    def add_game_item(self, item_name, game):
        new_menu_item = rumps.MenuItem(
            item_name,
            callback=lambda sender, arg=game: self.game_click(sender, arg),
        )
        self.menu.insert_before("Refresh", new_menu_item)

    def menu_item_click(self, sender):
        pass

    def add_menu_item(self, item_name):
        new_menu_item = rumps.MenuItem(item_name)
        new_menu_item.set_callback(self.menu_item_click)
        self.menu.insert_before("Refresh", new_menu_item)

    @rumps.clicked("Refresh")
    def refresh_menu(self, sender):
        for item in self.menu:
            if item != "Refresh" and item != "Quit":
                self.menu.pop(item)
        self.update_menu_game()
