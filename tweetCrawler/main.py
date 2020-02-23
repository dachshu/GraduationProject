import click
import TweetCrawler

@click.command()
@click.argument('account')
@click.option('-u', '--update', is_flag=True, help="Update the account's tweets")
@click.option('-c', '--crawl_from', type=click.DateTime(formats=('%Y-%m',)), help="Do crawling from the specified date.")
@click.option('-f', '--filter', type=click.Choice(['text','time', 'time_text']), help="Filter to this format.")
def main(account, update, crawl_from, filter):
    tweetCrawler = TweetCrawler.TweetCrawelr()
    if update:
        tweetCrawler.update(account)
    if crawl_from is not None:
        tweetCrawler.crawling(account, crawl_from.year, crawl_from.month)
    if filter is not None:
        tweetCrawler.filtering(account, filter)




if __name__ == '__main__':
    main()
