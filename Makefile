export LOG_LEVEL=DEBUG
run:
	poetry run blog_post_extractor extract \
		--url $(url)
		--output "blog_post.txt"
