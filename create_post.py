from datetime import datetime
from textwrap import dedent


POST_TEMPLATE = dedent('''
    Title: {title}
    Date: {date}
    Modified: {modified}
    Category: {category}
    Tags: {tags}
    Slug: {slug}
    Authors: {authors}
    Summary: {summary}

    [TOC]

    ---
    <!--your content here-->
''')


AVAILABLE_CATEGORIES = [
    'announcement',
    'interview',
    'online-conference',
    'programs',
    'registration',
    'sponsors',
    'tutoiral',
    'visiting group',
]


def _input_date() -> str:
    default_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return input(f'Date (default: {default_time}): ') or default_time


def _input_category() -> str:
    print('Select a category:')
    for idx, cat in enumerate(AVAILABLE_CATEGORIES):
        print(f'{idx}. {cat}')

    selection = int(input('Your selection (default: 0): ') or 0)
    if selection < 0 or selection >= len(AVAILABLE_CATEGORIES):
        raise ValueError(f'Numbers should be within 0~{len(AVAILABLE_CATEGORIES) - 1}')

    return AVAILABLE_CATEGORIES[selection]


def _input_tags() -> str:
    print('Type any number of tags. Enter "!" to finish\n')
    tags = []
    while (tag := input('-> ')) != '!':
        tags.append(tag)
    return ', '.join(tags)


def _input_authors() -> str:
    print('Specify any number of authors. Enter "!" to finish\n')
    authors = []
    while (author := input('-> ')) != '!':
        authors.append(author)
    return ', '.join(authors)


def main():
    print('Create a new post to pycontw-blog\n'.title())

    title = input('Title of the post: ')
    date = modified = _input_date()
    category = _input_category()
    tags = _input_tags()
    authors = _input_authors()

    slug_title = '-'.join(title.lower().split())
    slug_date = datetime.now().strftime('%Y-%m-%d')
    slug = f'{slug_date}-{slug_title}'
    summary = input('Summary: ')

    rendered_template = POST_TEMPLATE.format(
        title=title,
        date=date,
        modified=modified,
        category=category,
        tags=tags,
        authors=authors,
        slug=slug,
        summary=summary,
    )
    file_path = f'content/posts/{slug}.md'
    with open(file_path, 'w') as out:
        out.write(rendered_template)

    print(f'\nFile has already been written to {file_path}.')
    print('Please open the file to continue editing the content. Have a nice day~')


if __name__ == '__main__':
    main()
