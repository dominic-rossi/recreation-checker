build:
	docker build -t recreation-image .

run: build
	docker run --rm -it --name recreation-checker recreation-image