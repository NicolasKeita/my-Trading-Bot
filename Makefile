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

SRC		=	bot/__main__.py

LN		=	ln -s

$(NAME)	:
	$(LN) $(SRC) $(NAME)

all	:	
	$(MAKE) $(NAME) --no-print-directory

tests_run :
	python3 -m unittest discover tests/

fclean	:	clean
	$(RM) $(NAME)

clean	:
	$(RM) -r $(PYCACHE)

re	:	fclean all

.PHONY	: all fclean clean re tests_run
