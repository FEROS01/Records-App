from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Verses


class Bible():
    all_books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']

    def __init__(self,book,chapter,verse1,verse2=None,multiple=False):
        self.book = book
        self.chapter = chapter
        self.verse1 = verse1
        self.verse2 = verse2
        self.multiple = multiple
        self.errors = []
    
    def confirm_book(self):
        t_book = self.book.title()
        if t_book in self.all_books:
            self.book_id = self.all_books.index(t_book) + 1
        raise ValidationError(f'{self.book} does not exist')

    def confirm_chapter(self):
        chapter_exists = Verses.objects.exists(
            book = self.book_id,
            chapter = self.chapter
        )
        
        if not chapter_exists:
            raise ValidationError(
                f'{self.book} does not have chapter {self.chapter}')


    def confirm_verses(self):
        pass

    def confirm_passage(self):
        return all()

    def get_bible_passage(self):
        pass