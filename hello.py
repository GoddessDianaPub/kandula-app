import click

@click.command()
def hello():
	click.echo('Hello Click!')
	
if __name__ == ' _main__':
	hello()