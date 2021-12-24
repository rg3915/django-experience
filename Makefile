indenter:
	find backend -name "*.html" | xargs djhtml -t 2 -i

isort:
	isort -m 3 *

lint: indenter isort
