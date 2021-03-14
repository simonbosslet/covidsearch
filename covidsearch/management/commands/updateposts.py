from django.core.management.base import BaseCommand, CommandError
import covidsearch.makingposts as makeposts

class Command(BaseCommand):
    help = 'Updates database with posts from Hoosier Covid-19 Page.'
    
    def handle(self, *args, **kwargs):
        makeposts.updateposts()
        