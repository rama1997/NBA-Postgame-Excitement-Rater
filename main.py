import nba_api_helpers as nba
import output_helper
from menu_app.app import NBAMenuApp
import argparse

# Create an argument parser
ap = argparse.ArgumentParser()

# Add optional argument to run as menu app
ap.add_argument(
    "--menu",
    action="store_true",
    help="Option to user as a menu app",
)


def main():
    output_helper.print_output()


if __name__ == "__main__":
    args = ap.parse_args()
    if args.menu:
        app = NBAMenuApp()
        app.run()

    else:
        main()
