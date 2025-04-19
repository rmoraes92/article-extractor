import unittest

from blog_post_extractor.extract_blog_post import (
    extract_blog_post,
    extract_page_title,
    extract_blog_post_title_tag,
    match_strings,
)


class BlogSpotExtractorTestCase(unittest.TestCase):

    def test_match_strings(self):
        ratio = match_strings(
            "Hello World! This is a test.",
            "Hello World! This is a test."
        )
        self.assertEqual(ratio, 1.0)

        ratio = match_strings(
            "Hello World! This is a test - Some Random Subtile",
            "Hello World! This is a test."
        )
        self.assertTrue(ratio >= 0.6)

    def test_extract_page_title(self):
        """
        The HTML page has a title tag
        """
        html_body = """
        <html>
            <head>
                <title>Test Title</title>
            </head>
            <body>
                <h1>Test Title</h1>
                <p>Some content here.</p>
            </body>
        </html>
        """
        self.assertEqual(extract_page_title(html_body), "Test Title")

    def test_text_extract_blog_post_title_tag(self):
        """
        The HTML page has a title tag
        """
        html_body = """
        <html>
            <head>
                <title>Test Title</title>
            </head>
            <body>
                <h1>Test Title</h1>
                <p>Some content here.</p>
            </body>
        </html>
        """
        tag = extract_blog_post_title_tag("Test Title", html_body)
        self.assertEqual(tag.string, "Test Title")
        self.assertEqual(tag.name, "h1")

    def test_extract_blog_post(self):
        """
        The HTML page has a title tag
        """
        html_body = """
        <html>
            <head>
                <title>Test Title</title>
            </head>
            <body>
                <h1>Test Title</h1>
                <p>Some content here.</p>
            </body>
        </html>
        """
        title_text, descendants_text_list = extract_blog_post(html_body)
        self.assertEqual(title_text, "Test Title")
        self.assertEqual(descendants_text_list, ["Test Title", "Some content here."])

        # Test with inner HTML tags
        # The function should ignore the inner HTML tags and return the text
        # content

        html_body = """
        <html>
            <head>
                <title>Test Title</title>
            </head>
            <body>
                <h1>Test Title</h1>
                <p>Some content here.</p>
                <p>Some content <b>there</b>.</p>
            </body>
        </html>
        """
        title_text, descendants_text_list = extract_blog_post(html_body)
        self.assertEqual(title_text, "Test Title")
        self.assertEqual(
            descendants_text_list,
            [
                "Test Title",
                "Some content here.",
                "Some content there.",
            ],
        )

        html_body = """
        <html>
            <head>
                <title>Test Title</title>
            </head>
            <body>
                <h1>Test Title</h1>
                <p>Some content here.</p>
                <p>Some content <b>there</b>.</p>
                <code>print("hello world!")</code>
                <p>Some content <i>there</i>.</p>
                <p>Some content <a href="#">there</a>.</p>
                <p>Some content <code>print("hello world!")</code>.</p>
            </body>
            <footer>
                <p>Footer content</p>
            </footer>
        </html>
        """
        title_text, descendants_text_list = extract_blog_post(html_body)
        self.assertEqual(title_text, "Test Title")
        self.assertEqual(
            descendants_text_list,
            [
                "Test Title",
                "Some content here.",
                "Some content there.",
                'print("hello world!")',
                "Some content there.",
                "Some content there.",
                'Some content print("hello world!").',
            ],
        )
