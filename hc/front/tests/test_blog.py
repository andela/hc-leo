from hc.test import BaseTestCase
from hc.front.models import Category, Blog
from hc.front.forms import CreateCategoryForm, AddBlogPostForm
from django.urls import reverse


class BlogTestCase(BaseTestCase):
    def test_blog_page(self):
        """Test blog page is rendered"""
        r = self.client.get("/blog/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "You don\'t have any posts yet.")

    def test_create_blog_post(self):
        cat = Category(name="technology")
        cat.save()
        self.client.login(username="alice@example.org", password="password")

        initial_blog_count = Blog.objects.count()
        form = {
            "title": "this is a title",
            "body": "this is a body",
            "category": 2
        }

        abc = AddBlogPostForm(form)
        abc.save()

        blog_count = Blog.objects.count()

        self.assertEqual(blog_count - initial_blog_count, 1)

    def test_read_blog_post(self):
        Category(name="technology").save()
        blog = Blog(title="HELLO WORLD",
                    body="THIS IS WHERE EVERYTHING ELSE GOES",
                    category=Category.objects.first(),
                    user=self.alice)
        blog.save()

        url = reverse("hc-blog")
        r = self.client.get(url)
        self.assertContains(r, "HELLO WORLD")

    def test_delete_blog_post(self):
        self.client.login(username="alice@example.org", password="password")

        Category(name="technology").save()
        Blog(title="blog to delete",
                    body="delete this one",
                    category=Category.objects.first(),
                    user=self.alice).save()
        blog = Blog.objects.get(title="blog to delete")
        url = reverse("hc-delete_blog", kwargs={ 'pk': blog.id })

        r = self.client.delete(url)

        assert Blog.objects.count() == 0

        self.assertRedirects(r, reverse("hc-blog"))


class BlogFormTestCase(BaseTestCase):
    def test_form_validations(self):
        Category(name="technology").save()

        catForm = CreateCategoryForm({"name": "cat1"})
        self.assertTrue(catForm.is_valid())

        blogForm = AddBlogPostForm({
            "title": "title1",
            "body": "body1",
            "category": 1
        })
        self.assertTrue(blogForm.is_valid())
