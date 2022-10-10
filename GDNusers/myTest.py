from operator import mod
from pyexpat import model
from models import Products

def main():
    print(list(Products.objects.all()))

if __name__ == '__main__':
    main()