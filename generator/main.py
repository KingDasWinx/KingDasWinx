"""Entry point for the Galaxy Profile README generator."""

import argparse
import logging
import os
import sys

import requests
import yaml

from generator.config import ConfigError, validate_config
from generator.github_api import GitHubAPI
from generator.svg_builder import SVGBuilder

logger = logging.getLogger(__name__)

DEMO_STATS = {"commits": 1847, "stars": 342, "prs": 156, "issues": 89, "repos": 42}
DEMO_LANGUAGES = {
    "Python": 450000,
    "TypeScript": 380000,
    "JavaScript": 120000,
    "Go": 95000,
    "Rust": 45000,
    "Shell": 30000,
    "Dockerfile": 15000,
    "CSS": 10000,
}
DEMO_CONTRIBUTIONS = {
    "days": [5, 8, 12, 0, 3, 15, 18, 20, 0, 9, 12, 15, 18, 22, 0, 0, 10, 14, 17, 19, 21, 0, 7, 11, 13, 16, 19, 22, 25, 0, 8, 12, 15, 18, 0, 0, 9, 11, 14, 17, 20, 23, 25, 0, 6, 10, 13, 16, 19, 22, 0, 0, 8, 11, 14, 17, 20, 23, 26, 0, 7, 10, 13, 16, 19, 0, 0, 9, 12, 15, 18, 21, 24, 27, 0, 6, 9, 12, 15, 18, 21, 0, 0, 8, 11, 14, 17, 20, 23, 26, 0, 7, 10, 13, 16, 19, 22, 0, 0, 10, 13, 16, 19, 22, 25, 28, 0, 8, 11, 14, 17, 20, 0, 0, 9, 12, 15, 18, 21, 24, 27, 0, 7, 10, 13, 16, 19, 22, 0, 0, 11, 14, 17, 20, 23, 26, 29, 0, 9, 12, 15, 18, 21, 0, 0, 10, 13, 16, 19, 22, 25, 28, 0, 8, 11, 14, 17, 20, 23, 0, 0, 9, 12, 15, 18, 21, 24, 27, 0, 8, 11, 14, 17, 20, 0, 0, 10, 13, 16, 19, 22, 25, 28, 0, 9, 12, 15, 18, 21, 24, 0, 0, 11, 14, 17, 20, 23, 26, 29, 0, 9, 12, 15, 18, 21, 0, 0, 10, 13, 16, 19, 22, 25, 28, 0, 8, 11, 14, 17, 20, 23, 0, 0, 9, 12, 15, 18, 21, 24, 27, 0, 8, 11, 14, 17, 20, 0, 0, 10, 13, 16, 19, 22, 25, 28, 0, 9, 12, 15, 18, 21, 24, 0, 0, 11, 14, 17, 20, 23, 26, 29, 0, 9, 12, 15, 18, 21, 0, 0, 10, 13, 16, 19, 22, 25, 28, 0, 8, 11, 14, 17, 20, 23, 0, 0, 9, 12, 15, 18, 21, 24, 27, 0, 8, 11, 14, 17, 20, 0, 0, 10, 13, 16, 19, 22, 25, 0, 9, 12, 15, 18, 21, 24, 0, 0, 11, 14, 17, 20, 23, 26, 0, 9, 12, 15, 18, 21, 0, 0, 10, 13, 16, 19, 22, 25, 0, 8, 11, 14, 17, 20, 23, 0, 0, 9, 12, 15, 18, 21, 24, 0, 8, 11, 14, 17, 20],
    "total": 4523,
    "streak": 5,
}


def generate(args):
    """Generate SVGs from config (existing behavior extracted into a function)."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    demo = getattr(args, "demo", False)

    # Load config
    if demo:
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.example.yml")
    else:
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.yml")

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        if demo:
            logger.error("config.example.yml not found.")
        else:
            logger.error("config.yml not found. Copy config.example.yml to config.yml and edit it.")
        sys.exit(1)

    try:
        config = validate_config(config)
    except ConfigError as e:
        logger.error("Invalid config: %s", e)
        sys.exit(1)

    username = config["username"]

    logger.info("Generating profile SVGs for @%s...", username)

    if demo:
        logger.info("Demo mode: using hardcoded stats, languages, and contributions.")
        stats = DEMO_STATS
        languages = DEMO_LANGUAGES
        contributions = DEMO_CONTRIBUTIONS
    else:
        # Fetch GitHub data
        api = GitHubAPI(username)

        logger.info("Fetching stats...")
        try:
            stats = api.fetch_stats()
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            logger.warning("Could not fetch stats (%s). Using defaults.", e)
            stats = {"commits": 0, "stars": 0, "prs": 0, "issues": 0, "repos": 0}

        logger.info("Fetching languages...")
        try:
            languages = api.fetch_languages()
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            logger.warning("Could not fetch languages (%s). Using defaults.", e)
            languages = {}

        logger.info("Fetching contributions...")
        try:
            contributions = api.fetch_contributions()
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            logger.warning("Could not fetch contributions (%s). Using defaults.", e)
            contributions = {"weeks": [], "total": 0, "streak": 0}

    logger.info("Stats: %s", stats)
    logger.info("Languages: %d found", len(languages))
    logger.info("Contributions: %d total, %d day streak", contributions.get("total", 0), contributions.get("streak", 0))

    # Build SVGs
    builder = SVGBuilder(config, stats, languages, contributions)
    output_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "generated")
    os.makedirs(output_dir, exist_ok=True)

    svgs = {
        "galaxy-header.svg": builder.render_galaxy_header(),
        "stats-card.svg": builder.render_stats_card(),
        "tech-stack.svg": builder.render_tech_stack(),
        "projects-constellation.svg": builder.render_projects_constellation(),
        "contributions-heatmap.svg": builder.render_contributions_heatmap(),
    }

    for filename, content in svgs.items():
        path = os.path.join(output_dir, filename)
        with open(path, "w") as f:
            f.write(content)
        logger.info("Wrote %s", path)

    logger.info("Done! 5 SVGs generated.")


def main():
    parser = argparse.ArgumentParser(description="Generate Galaxy Profile SVGs")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: init
    subparsers.add_parser("init", help="Interactive setup wizard to create config.yml")

    # Subcommand: generate
    gen_parser = subparsers.add_parser("generate", help="Generate SVGs from config")
    gen_parser.add_argument(
        "--demo",
        action="store_true",
        help="Generate SVGs with demo data (no API calls, uses config.example.yml)",
    )

    # Top-level --demo for backward compatibility (python -m generator.main --demo)
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Generate SVGs with demo data (no API calls, uses config.example.yml)",
    )

    args = parser.parse_args()

    if args.command == "init":
        from generator.cli_init import run_init
        run_init()
    else:
        # Default behavior: generate (supports both `generate --demo` and `--demo`)
        generate(args)


if __name__ == "__main__":
    main()
