[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# PyCon Taiwan Blog

## Getting Started

### Prerequisites
* [Python 3.10](https://www.python.org/downloads/)
* [pipenv](https://pipenv.pypa.io/en/latest/)


### Environment Setup

1. Fork [pycontw/pycontw-blog](https://github.com/pycontw/pycontw-blog)
2. Clone the repository from your GitHub. (i.e., your-user-name/pycontw-blog)
3. Setup development environment through the following command

    ```sh
    pipenv install --dev
    ```

4. Setup [pre-commit](https://pre-commit.com/) hooks which check common errors when you do certain types of git commits

    ```sh
    pipenv run pre-commit install --hook-type commit-msg --hook-type pre-push --hook-type pre-commit
    ```

### Write a new article

1. Create a file in markdown or reStructuredText format inside the `content` directory. The following section will detail how we organized the `content` directory. Your filename should be the English title of your article. You'll have to translate it if there's no English title. The following is a minimal example of an article.
    * In markdown
        ```markdown
        Title: My super post
        Date: 2010-12-03 10:20
        Modified: 2010-12-05 19:30
        Category: Python
        Tags: pelican, publishing
        Slug: my-super-post
        Authors: Alexis Metaireau, Conan Doyle
        Summary: Short version for index and feeds

        This is the content of my super blog post.
        ```
    * In reStructuredText
        ```reStructuredText
        My super post
        ##############

        :date: 2010-10-03 10:20
        :modified: 2010-10-04 18:40
        :tags: thats, awesome
        :category: yeah
        :slug: my-super-post
        :authors: Alexis Metaireau, Conan Doyle
        :summary: Short version for index and feeds
        ```

        Please read [Writing content](https://docs.getpelican.com/en/latest/content.html) section in pelican documentation for format detail.
2. After you finish a new article, you can run `pipenv run inv livereload`. It will build our current content into web pages, serve it on `http://localhost:8000/`, and open your default browser.
3. If everything looks good, use the following command to add the new article to this repository.

    ```sh
    git add <your new article>

    # use commitizen to do git commit
    # choose the "new post" type if you're adding a new article
    pipenv run cz commit

    git push origin <your feature branch>
    ```
4. Create a pull request to [pycontw/pycontw-blog](https://github.com/pycontw/pycontw-blog).

### How do we organize our data in the `content` directory?
TBD

## Authors
Wei Lee <weilee.rx@gmail.com>
