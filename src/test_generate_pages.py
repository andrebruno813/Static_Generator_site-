import os
import tempfile
import unittest

from main import generate_pages


class TestGeneratePages(unittest.TestCase):
    def test_generate_pages_from_content_directory(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            content_dir = os.path.join(tmp_dir, "content")
            public_dir = os.path.join(tmp_dir, "public")
            blog_dir = os.path.join(content_dir, "blog", "example")
            os.makedirs(blog_dir)

            template_path = os.path.join(tmp_dir, "template.html")
            with open(template_path, "w") as template_file:
                template_file.write("<html><head><title>{{ Title }}</title></head><body><a href=\"/\">Home</a>{{ Content }}</body></html>")

            with open(os.path.join(content_dir, "index.md"), "w") as index_file:
                index_file.write("# Home Page\n\nHello from home.")

            with open(os.path.join(blog_dir, "index.md"), "w") as blog_file:
                blog_file.write("# Example Post\n\nThis is a blog post.")

            generate_pages(content_dir, template_path, public_dir, "/Static_Generator_site/")

            self.assertTrue(os.path.exists(os.path.join(public_dir, "index.html")))
            self.assertTrue(os.path.exists(os.path.join(public_dir, "blog", "example", "index.html")))

            with open(os.path.join(public_dir, "index.html"), "r") as f:
                index_html = f.read()
            self.assertIn("Home Page", index_html)
            self.assertIn("Hello from home.", index_html)
            self.assertIn('href="/Static_Generator_site/"', index_html)

            with open(os.path.join(public_dir, "blog", "example", "index.html"), "r") as f:
                blog_html = f.read()
            self.assertIn("Example Post", blog_html)
            self.assertIn("This is a blog post.", blog_html)


if __name__ == "__main__":
    unittest.main()
