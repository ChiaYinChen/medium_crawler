"""Medium Crawler Command Line Tools."""
import argparse
import logging
from typing import List

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import sessionmaker
from twisted.internet import reactor

from models import Rule, create_new_table, db_connect
from utils import timer

launch_logger = logging.getLogger('launch_crawlers_logger')
settings = get_project_settings()
configure_logging(settings)


def process_command() -> argparse.Namespace:
    """Create the crawler parser.

    Returns:
        argparse.Namespace: argparse object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--spider',
                        help='Please input the scrapy spider name',
                        type=str,
                        required=True)
    return parser.parse_args()


def start_crawlers(spider_name: str, rules: List[Rule]) -> None:
    """Start specified spiders from cmd with scrapy core api.

    Args:
        spider_name (str): scrapy spider name
        rules (List[Rule]): pass arguments for spider from database
    """
    runner = CrawlerRunner(settings)
    crawlers = runner.spider_loader.list()
    crawlers = [c for c in crawlers if c.__contains__(spider_name)]
    if crawlers:
        for rule in rules:
            runner.crawl(crawlers[0], rule=rule)
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        launch_logger.debug('all finished.')
    else:
        launch_logger.warning('provide the right spider name.')


@timer
def main():
    """Execute."""
    engine = db_connect()
    create_new_table(engine=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    rules = session.query(Rule).filter_by(enable=1).all()
    session.close()

    arg = vars(process_command())
    if rules:
        start_crawlers(spider_name=arg.get('spider'), rules=rules)
    else:
        launch_logger.warning('no rule need to be crawled.')


if __name__ == '__main__':
    main()
