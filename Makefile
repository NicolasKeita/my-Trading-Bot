##
## EPITECH PROJECT, 2018
## Makefile
## File description:
## Makefile for trade project
##

MAKE	=	make

PYCACHE	=	__pycache__/

RM		=	rm -f

NAME	=	trade

all	:
	ln -s __main__.py $(NAME)

tests_run :
	python3 -m unittest discover tests/

fclean	:	clean
	$(RM) $(NAME)

clean	:
	$(RM) -r $(PYCACHE)

re	:	fclean all

.PHONY	: all fclean clean re tests_run
