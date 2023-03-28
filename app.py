from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods import media
from wordpress_xmlrpc.compat import xmlrpc_client

import argparse
import os

# replace with your own wordpress site url and credentials
wp = Client('http://your_wp_site.com/xmlrpc.php', 'admin', 'password')


def python_to_wp(folder, title, tags, category, slug=None):
    print('Creating post: ' + title)

    post = WordPressPost()
    post.title = title
    if slug:
        post.slug = slug
    post.content = ''
    prompt_txt_content = get_prompt_txt_content(folder)
    post.terms_names = {
        'post_tag': tags.split(','),
        'category': category.split(',')
    }

    post.excerpt = prompt_txt_content

    post.post_status = 'publish'

    images = get_folder_images(folder)

    has_cover = False

    for image in images:
        # upload image
        image_with_path = os.path.join(folder, image)
        image_uploaded = upload_image(image_with_path)
        image_url = image_uploaded['url']
        image_id = image_uploaded['id']
        image_name = image_uploaded['file']

        # add image to post content
        post.content += f'''<figure class="wp-block-image size-full"><img decoding="async" loading="lazy" src="{image_url}" alt="" ></figure>'''
        if not has_cover:
            post.thumbnail = image_id
            if image_name == 'cover.webp':
                has_cover = True

    wp.call(NewPost(post))
    print('Post created: ' + title)


def get_folder_images(folder):
    images = [f for f in os.listdir(
        folder) if os.path.isfile(os.path.join(folder, f))]
    images = [f for f in images if f.endswith('.webp')]
    return images


def upload_image(image):
    # get image name
    image_name = os.path.basename(image)

    # get image data
    data = {
        'name': image_name,
        'type': 'image/webp',
    }

    # open image
    with open(image, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())

    # upload image
    response = wp.call(media.UploadFile(data))

    return response


def get_prompt_txt_content(folder):
    prompt_file = os.path.join(folder, 'prompt.txt')
    if os.path.isfile(prompt_file):
        with open(prompt_file, 'r', encoding='utf8') as f:
            content = f.read()
            return content
    else:
        return ''


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', help='Choose Folder', required=True)
    parser.add_argument('-t', '--title', help='Post Title', required=True)
    parser.add_argument('-s', '--slug', help='Post Slug')
    parser.add_argument('-tags', '--tags', help='Post Tags', required=True)
    parser.add_argument('-cat', '--category',
                        default='妹子图', help='Post Category')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    python_to_wp(**vars(args))


if __name__ == '__main__':
    main()
