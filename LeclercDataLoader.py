import os
import xml.etree.ElementTree as ET
import re


def read_leclerc_dataset(train_directory_path):
    products = list()
    files = os.listdir(train_directory_path)
    for file in files:

        print("reading file : " + file)
        tree = ET.parse(os.path.join(train_directory_path, file))
        items = tree.getroot()
        # Each item represents a product
        for item in items:
            product = {}
            product['categories'] = read_categories(item)
            product['text'] = str(read_metadata(item)) + " " + str(read_properties(item))
            products.append(product.copy())

    return products


def read_metadata(item):
    """read metadata (title, description, suplier, universalName ) for each item (product)."""
    metadata = " "
    clean = re.compile('<.*?>')

    title = item.find("./title")
    if title is not None and title.text is not None:
        metadata += " " + re.sub(clean, ' ', str(title.text))

    subtitle = item.find("./subtitle")
    if subtitle is not None and subtitle.text is not None:
        metadata += " " + re.sub(clean, ' ', str(subtitle.text))

    description = item.find("./description")
    if description is not None and description.text is not None:
        metadata += " " + re.sub(clean, ' ', str(description.text))

    suplier = item.find("./suplier")
    if suplier is not None and suplier.text is not None:
        metadata += " " + re.sub(clean, ' ', str(suplier.text))

    universe_name = item.find("./universe/name")
    if universe_name is not None and universe_name.text is not None:
        metadata += " " + re.sub(clean, ' ', str(universe_name.text))

    return metadata


def read_properties(item):
    """read properties"""
    properties = item.findall("./properties/property")
    clean = re.compile('<.*?>')
    content_properties = " "

    for property in properties:
        if property is not None:
            content_properties += " " + re.sub(clean, ' ', str(property.get('name')))
            content_properties += " " + re.sub(clean, ' ', str(property.text))
    return content_properties


def read_categories(item):
    categories = list()
    category1 = item.find("./categories/category_1")
    category2 = item.find("./categories/category_2")
    category3 = item.find("./categories/category_3")

    if category1 is not None and category1.text is not None:
        categories.append(category1.text)
    if category2 is not None and category2.text is not None:
        categories.append(category2.text)
    if category3 is not None and category3.text is not None:
        categories.append(category3.text)

    return categories
