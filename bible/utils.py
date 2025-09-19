import re

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Verses


class Bible():
    all_books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']

    def __init__(self,book,chapter,verse1,verse2=0):
        self.book = book
        self.chapter = chapter
        self.verse1 = min(verse1,verse2) if verse2 else verse1
        self.verse2 = max(verse1,verse2)
        self.errors = []
    
    def confirm_book(self):
        t_book = self.book.title()
        if t_book in self.all_books:
            self.book_id = self.all_books.index(t_book) + 1
        else:
            raise ValidationError(f'{self.book} does not exist')

    def confirm_chapter(self):
        self.confirm_book()
        self.verse = Verses.objects.filter(
            book = self.book_id,
            chapter = self.chapter
        )
        self.num_verses = self.verse.count()
        
        if not self.verse:
            raise ValidationError(
                f'{self.book} does not have chapter {self.chapter}')


    def confirm_verses(self):
        self.confirm_chapter()
        if self.verse2:
            self.verse = self.verse.filter(
                Q(verse__gte=self.verse1),
                Q(verse__lte=self.verse2)
            ).order_by('verse')
        else:
            self.verse = self.verse.filter(Q(verse=self.verse1)).order_by('verse')
        
        if not self.verse or self.verse2 > self.num_verses:
            raise ValidationError(
                f'{self.book} chapter {self.chapter} does not have the verse')

    def format_verse(self,verse,detail):
        re_text = re.sub('\{.*?\}','',verse)
        formatted = f'{detail}. ' + re_text
        return formatted

    def get_bible_passage(self):
        self.confirm_verses()
        passages = []
        for verse in self.verse:
            detail = verse.verse
            passages.append(self.format_verse(verse.text,detail))
        return passages

    
    